from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import numpy as  np

driver = webdriver.Edge()

try:
    # 直接导航到百度页面并等待至多20秒，直到某个关键页面元素加载完成
    driver.get("https://rewards.bing.com/")
    time.sleep(1)  # 暂时允许页面缓冲
    driver.maximize_window()
    main_window = driver.current_window_handle
    #加载并点击卡片1


    current_size = driver.get_window_size()
    body_height = current_size['height']

    # 计算要滚动的位置，这里乘以系数可以让代码更加灵活地应对不同的需求
    target_offset = int(1*body_height)
    script = f"window.scrollTo(0, {target_offset})"

    driver.execute_script(script)
    print("翻页成功")
    time.sleep(2)
    card1=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"mee-card-group.ng-scope:nth-child(7) > div:nth-child(1) > mee-card:nth-child(2) > div:nth-child(1) > card-content:nth-child(1) > mee-rewards-daily-set-item-content:nth-child(1) > div:nth-child(1) > a:nth-child(1)")))
    print("中间的卡片点击成功")

    card1.click()
    driver.switch_to.window(main_window)
    time.sleep(2)
    card2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "mee-card-group.ng-scope:nth-child(7) > div:nth-child(1) > mee-card:nth-child(1) > div:nth-child(1) > card-content:nth-child(1) > mee-rewards-daily-set-item-content:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(4) > span:nth-child(1)")))
    # 找入输入框：显性等待确保KW存在
    print("左边的卡片点击成功")
    driver.switch_to.window(main_window)
    time.sleep(2)
    # card3 = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR,
    #                                     "mee-card-group.ng-scope:nth-child(7) > div:nth-child(1) > mee-card:nth-child(3) > div:nth-child(1) > card-content:nth-child(1) > mee-rewards-daily-set-item-content:nth-child(1) > div:nth-child(1) > a:nth-child(1)")))
    # print("右边的卡片点击成功")
    # driver.switch_to.window(main_window)
    # time.sleep(2)

    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "rewards-suggestedSearch-searchbox"))
    )
    time.sleep(0.5)  # 可选，但不推荐依赖此


    # 输入搜索关键词
    index = {
        1:"dark",
        2:"constellation",
        3:"The Seed of the Sacred Fig",
        4:"true detective",
        5:"tenet",
        6:"strange things",
        7:"breaking bad",
        8:"better call saul",
        9:"The End of the Fucking World",
        10:"black story",
    }  # 示例关键词
    for i in index.keys():
        index[i]=index[i]+str(np.random.randn(1))
        search.send_keys(index[i])
        print("输入成功。")

    # 找出搜索按钮，并点击
        button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#rewards-suggestedSearch-searchbox-form > div > div")))
        time.sleep(0.5)  # 可选暂时延迟
        button.click()
        print("点击搜索成功。")
        time.sleep(1)  # 可选暂时延迟

        driver.switch_to.window(main_window)
    # 等待搜索结果加载完成，并打印一下操作信息
    # WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.result"))
    # )
        search.clear()
        time.sleep(1)  # 可选暂时延迟
        print("等待搜索结果页面加载完毕。")


except Exception as e:
    print(f"发生错误: {e}")
    traceback.print_exc()
    time.sleep(5)  # 让用户有机会查看页面
finally:
    driver.quit()  # 确保释放资源，关闭浏览器窗口，无论是否成功或失败





