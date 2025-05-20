from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import time
import csv
from translate_good_name import translate_good_name as translate
import re
import csv_procession
import glob

import pandas as pd
import os
#定义cs2饰品这个类
class CsGood:
    def __init__(self,url):
        '''
        url:该饰品的网址
        '''
        self.url=url
        self.name=""

    def crawldata(self,steps=150,delay=0.5):
        GOOD_DATA_KIND = ["sell_price", "buy_price", "short_lease_price", "lease_annual", "long_lease_price",
                          "long_lease_annual", "buy_num", "lease_num", "transfer_price"]
        driver = webdriver.Edge()
        try:
            # 打开csqaq熊刀致命紫罗兰的页面
            driver.get(self.url)
            time.sleep(1)  # 暂时允许页面缓冲
            driver.maximize_window()
            # 打开选择市场渠道
            button_channel = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tool___zRHK7:nth-child(2)")))
            time.sleep(0.5)  # 可选暂时延迟
            driver.execute_script("arguments[0].click();", button_channel)
            time.sleep(1)

            # 获取饰品名字
            good_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".scope_summery___3R1Bq > div:nth-child(4) > h3:nth-child(1)"))).text
            # 存放饰品数据的名字
            self.name= translate(good_name)
            # 选择uu的数据（默认出售价）
            youyou_choice = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ant-dropdown-menu-item:nth-child(2)")))
            youyou_choice.click()
            time.sleep(1)  # 可选暂时延迟

            # 打开时间跨度的选择
            button_intervals = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-dropdown-trigger:nth-child(3)")))
            button_intervals.click()
            time.sleep(1)  # 可选暂时延迟
            # 选择近1年
            oneyear_choice = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ant-dropdown-menu-item:nth-child(6)")))
            oneyear_choice.click()
            time.sleep(1)

            for j in range(len(GOOD_DATA_KIND)):
                print(f'''获取{GOOD_DATA_KIND[j]}中''')
                price_button_css = "li[role='menuitem'][value='" + GOOD_DATA_KIND[j] + "']"
                file_path = "./dataset/" + translate(good_name) + "_" + GOOD_DATA_KIND[j] + ".csv"

                csv_processed_path="./dataset_processed/" + translate(good_name) + "_" + GOOD_DATA_KIND[j] + ".csv"

                data_choice = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.dropdown_right___PeSeO:nth-child(1)")))
                driver.execute_script("arguments[0].click()", data_choice)

                price_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, price_button_css)))
                time.sleep(1)
                driver.execute_script("arguments[0].click()", price_button)

                # 等待canvas元素出现
                canvas = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    "#rc-tabs-0-panel-null > div > div > div > div.ant-col.ant-col-16 > div > div > div > div > div > div.echarts-for-react > div:nth-child(1) > canvas"))
                )
                print("加载图表成功")
                # 获取canvas元素矩形长宽
                canvas_rect = canvas.rect
                width = int(canvas_rect['width'])

                results = []
                visited = set()

                for i in range(0, -steps, -1):
                    x_offset = int(0.5 * width * i / steps)

                    # 将鼠标指针平移到canvas元素的中心点offset的位置
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(canvas, x_offset, 0).perform()
                    tooltip_sale = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '[style*="box-shadow"][style*="z-index"]'))
                    )
                    time.sleep(delay)

                    tooltip_sale_text = tooltip_sale.get_attribute('innerText').strip()

                    if tooltip_sale_text and tooltip_sale_text not in visited:
                        visited.add(tooltip_sale_text)
                        results.append(tooltip_sale_text)
                # 将悬浮的标签数据取出来
                for k in range(steps):
                    x_offset = int(0.5 * width * k / steps)

                    # 将鼠标指针平移到canvas元素的中心点offset的位置
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(canvas, x_offset, 0).perform()
                    tooltip_sale = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '[style*="box-shadow"][style*="z-index"]'))
                    )
                    time.sleep(delay)

                    tooltip_sale_text = tooltip_sale.get_attribute('innerText').strip()

                    if tooltip_sale_text and tooltip_sale_text not in visited:
                        visited.add(tooltip_sale_text)
                        results.insert(0, tooltip_sale_text)

                print(f'''获取{GOOD_DATA_KIND[j]}完成''')
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(results)
                func_name="csv_process_"+GOOD_DATA_KIND[j]
                getattr(csv_procession,func_name)(file_path,csv_processed_path)



        except Exception as e:
            print(f"发生错误: {e}")
            traceback.print_exc()
            time.sleep(5)  # 让用户有机会查看页面
        finally:
            driver.quit()

    def convert2csv(self):
        if not os.path.exists("./data"):
            os.mkdir("./data")
        output_path = "./data/" + self.name + ".csv"
        # 获取文件夹中所有CSV文件的路径
        csv_files = glob.glob('./dataset_processed/*.csv')
        # 创建一个空的DataFrame用于合并数据
        merged_df = pd.DataFrame()

        # 读取每个CSV文件并进行合并
        for file in csv_files:
            df = pd.read_csv(file)

            # 确保日期列为 datetime 类型，并指定日期格式
            df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')

            # 如果是第一个文件，初始化 merged_df，否则合并
            if merged_df.empty:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on='日期', how='outer')  # 使用 'outer' 合并，确保所有日期都有数据

        merged_df = merged_df.replace("", pd.NA)
        # 将合并后的DataFrame保存为一个新的CSV文件

        merged_df.to_csv(output_path, index=False)


butcher_automatic=CsGood("https://csqaq.com/goods/7041")
butcher_automatic.crawldata(steps=300,delay=0.15)
butcher_automatic.convert2csv()

