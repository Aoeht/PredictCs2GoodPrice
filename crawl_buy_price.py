from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import time
import csv
from translate_good_name import translate_good_name as translate

def crawl_buy_price(url,steps=10,delay=1):
    driver = webdriver.Firefox()
    try:
        # 打开csqaq熊刀致命紫罗兰的页面
        driver.get(url)
        time.sleep(1)  # 暂时允许页面缓冲
        driver.maximize_window()
        # 打开选择市场渠道
        button_channel = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tool___zRHK7:nth-child(2)")))
        time.sleep(0.5)  # 可选暂时延迟

        # button_channel.click()
        driver.execute_script("arguments[0].click();", button_channel)
        time.sleep(1)

        good_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".scope_summery___3R1Bq > div:nth-child(4) > h3:nth-child(1)"))).text
        #存放饰品数据的名字
        file_path= "./dataset/"+translate(good_name) + "_sale_price.csv"

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
        # 选择三年
        threeyear_choice = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.ant-dropdown-menu-item:nth-child(7)")))
        threeyear_choice.click()
        time.sleep(1)
        # 打开数据类型的选择
        price_button_css = "li[role='menuitem'][value='" + "sell_price" + "']"
        data_choice = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.dropdown_right___PeSeO:nth-child(1)")))
        driver.execute_script("arguments[0].click()", data_choice)
        time.sleep(1)
        beg_price = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, price_button_css)))
        time.sleep(1)
        driver.execute_script("arguments[0].click()", beg_price)
        print("we chose the beg_price")
        # 等待canvas元素出现
        canvas = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            ".echarts-for-react > div:nth-child(1) > canvas:nth-child(1)"))
        )

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
                    (By.XPATH, "//div[contains(@style,'z-index') and contains(@style,'box-shadow')]"))
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
                    (By.XPATH, "//div[contains(@style,'z-index') and contains(@style,'box-shadow')]"))
            )
            time.sleep(delay)

            tooltip_sale_text = tooltip_sale.get_attribute('innerText').strip()

            if tooltip_sale_text and tooltip_sale_text not in visited:
                visited.add(tooltip_sale_text)
                results.insert(0, tooltip_sale_text)

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(results)

    except Exception as e:
        print(f"发生错误: {e}")
        traceback.print_exc()
        time.sleep(5)  # 让用户有机会查看页面
    finally:
        driver.quit()




