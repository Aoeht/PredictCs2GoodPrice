import re
import pandas as pd
def csv_process_sell_price(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价
    prices = re.findall(r'出售价(\d{3,4})', content)

    # 在售数
    volumes = re.findall(r'在售数(\d{1,3})', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，售价 {len(prices)} 个，在售数 {len(volumes)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(prices), len(volumes))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price = prices[i]
        volume = volumes[i]


        data.append([date, price, volume])

    df = pd.DataFrame(data, columns=['日期', '出售价', '在售数'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_buy_price(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    prices = re.findall(r'求购价(\d{3,4})', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，求购价 {len(prices)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(prices))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price = prices[i]
        # 判断涨跌符号


        data.append([date, price])

    df = pd.DataFrame(data, columns=['日期', '求购价'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_buy_num(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    buy_num = re.findall(r'求购数量(\d+)', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，求购 {len(buy_num)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(buy_num))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price = buy_num[i]
        data.append([date, price])

    df = pd.DataFrame(data, columns=['日期', '求购数量'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_short_lease_price(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_price = re.findall(r'短租租金([01]\.\d{1,2})', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，短租租金{len(short_lease_price)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_price))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price = short_lease_price[i]

        data.append([date, price])

    df = pd.DataFrame(data, columns=['日期', '短租租金'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_lease_annual(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_annual = re.findall(r'短租收益率(\d{1,2}\.\d{1,2}%)', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，短租收益率{len(short_lease_annual)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_annual))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        data.append([dates[i], short_lease_annual[i]])

    df = pd.DataFrame(data, columns=['日期', '短租收益率'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_long_lease_annual(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')
    print(content, "\n")
    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)
    print(dates, "\n", type(dates), "\n")
    # 出售价、环比变化（允许小数）
    short_lease_annual = re.findall(r'长租收益率(\d{1,2}\.\d{1,2}%)', content)
    print(short_lease_annual, "\n")
    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，长租收益率{len(short_lease_annual)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_annual))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        data.append([dates[i], short_lease_annual[i]])

    df = pd.DataFrame(data, columns=['日期', '长租收益率'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_long_lease_price(origin_csv,processed_csv):

    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    long_lease_price = re.findall(r'长租租金([01]\.\d{1,2})', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，长租租金{len(long_lease_price)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(long_lease_price))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price = long_lease_price[i]
        # 判断涨跌符号


        data.append([date, price])

    df = pd.DataFrame(data, columns=['日期', '长租租金'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_lease_num(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_num = re.findall(r'在租数量(\d{1,3})', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，在租数量{len(short_lease_num)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_num))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price= short_lease_num[i]
        data.append([date, price])

    df = pd.DataFrame(data, columns=['日期', '在租数量'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_transfer_price(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_annual = re.findall(r'租赁过户价(\d{0,4}\b)', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，租赁过户价{len(short_lease_annual)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_annual))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price= short_lease_annual[i]
        # 判断涨跌符号

        data.append([date, price])

    df = pd.DataFrame(data, columns=['日期', '租赁过户价'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

