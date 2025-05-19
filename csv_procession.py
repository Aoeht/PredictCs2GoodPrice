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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    prices = re.findall(r'出售价(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 在售数、环比变化
    volumes = re.findall(r'在售数(\d+)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，售价 {len(prices)} 个，在售数 {len(volumes)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(prices), len(volumes))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = prices[i]
        volume, volume_change = volumes[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        volume_change_str = '-' + volume_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'出售价{price}\([-+]{price_change}%\)', content)
        raw_volume_match = re.search(f'在售数{volume}\([-+]{volume_change}%\)', content)
        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'
        if raw_volume_match and '+' in raw_volume_match.group(0):
            volume_change_str = '+' + volume_change + '%'

        data.append([date, price, price_change_str, volume, volume_change_str])

    df = pd.DataFrame(data, columns=['日期', '出售价', '出售价环比变化', '在售数', '在售数环比变化'])

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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    prices = re.findall(r'求购价(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，求购价 {len(prices)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(prices))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = prices[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'

        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'求购价{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '求购价', '求购价环比变化', ])

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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    buy_num = re.findall(r'求购数量(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，求购 {len(buy_num)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(buy_num))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = buy_num[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'求购数量  {price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '求购数量', '求购数量环比变化'])

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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_price = re.findall(r'短租租金(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，短租租金{len(short_lease_price)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_price))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = short_lease_price[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'短租租金{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '短租租金', '短租租金环比变化'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_lease_annual(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_annual = re.findall(r'短租收益率(\d+(?:\.\d+)?)%\(([-+])(\d+(?:\.\d+)?)%\)', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，短租收益率{len(short_lease_annual)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_annual))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = short_lease_annual[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'短租收益率{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '短租收益率', '短租收益率环比变化'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

def csv_process_long_lease_annual(origin_csv,processed_csv):
    # 1. 读取原始字符流文件
    with open(origin_csv, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 还原被拆开的字符：去掉逗号、空格、无用字符
    content = content.replace(',', '').replace('　', '').replace('"', '').replace('\n', '')

    # 3. 正则提取 日期、出售价、出售价环比、在售数、在售数环比

    # 日期：形如 2025-04-17
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    long_lease_annual = re.findall(r'长租收益率(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，长租收益率{len(long_lease_annual)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(long_lease_annual))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = long_lease_annual[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'长租收益率{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '长租收益率', '长租收益率环比变化'])

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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    long_lease_price = re.findall(r'长租租金(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，长租租金{len(long_lease_price)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(long_lease_price))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = long_lease_price[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'长租租金{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '长租租金', '长租租金环比变化'])

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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_num = re.findall(r'在租数量(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，在租数量{len(short_lease_num)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_num))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = short_lease_num[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'在租数量{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '在租数量', '在租数量环比变化'])

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
    dates = re.findall(r'2\d{3}-\d{2}-\d{2}', content)

    # 出售价、环比变化（允许小数）
    short_lease_annual = re.findall(r'租赁过户价(\d+(?:\.\d+)?)[(][-+](\d+(?:\.\d+)?)%[)]', content)

    # 4. 安全检查匹配数量
    print(f'匹配到 日期 {len(dates)} 个，租赁过户价{len(short_lease_annual)} 个')

    # 5. 数据整合，防止越界
    min_len = min(len(dates), len(short_lease_annual))

    # 6. 生成DataFrame
    data = []
    for i in range(min_len):
        date = dates[i]
        price, price_change = short_lease_annual[i]
        # 判断涨跌符号
        price_change_str = '-' + price_change + '%'
        # 这里根据文件内容来，+号出现在volume_change时要判断
        # 检查原始匹配内容
        raw_price_match = re.search(f'租赁过户价{price}\([-+]{price_change}%\)', content)

        if raw_price_match and '+' in raw_price_match.group(0):
            price_change_str = '+' + price_change + '%'


        data.append([date, price, price_change_str])

    df = pd.DataFrame(data, columns=['日期', '租赁过户价', '租赁过户价环比变化'])

    # 7. 保存为标准CSV
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')