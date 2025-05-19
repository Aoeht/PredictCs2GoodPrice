import csv_procession
# from csv_procession import csv_process_buy_price as process_buy
# from csv_procession import csv_process_sell_price as process_sell
# from csv_procession import csv_process_buy_num as process_buy_num
# process_sell("./dataset/UrsusKnifeVioletFieldTested_sell_price.csv","./dataset/UrsusKnifeVioletFieldTested_sell_price_re.csv")
# process_buy("./dataset/UrsusKnifeVioletFieldTested_buy_price.csv","./dataset/UrsusKnifeVioletFieldTested_buy_price_re.csv")
# process_buy_num("./dataset/UrsusKnifeVioletFieldTested_buy_num.csv","./dataset/UrsusKnifeVioletFieldTested_buy_num_re.csv")
# csv_procession.csv_process_transfer_price("./dataset/UrsusKnifeVioletFieldTested_transfer_price.csv","./dataset/UrsusKnifeVioletFieldTested_transfer_price_re.csv")
# csv_procession.csv_process_lease_num("./dataset/UrsusKnifeVioletFieldTested_lease_num.csv","./dataset/UrsusKnifeVioletFieldTested_lease_num_re.csv")
# csv_procession.csv_process_lease_annual("./dataset/GutAutomaticFieldTested_lease_annual.csv","./dataset/GutAutomaticFieldTested_lease_annual_re.csv")
# csv_procession.csv_process_long_lease_annual("./dataset/UrsusKnifeVioletFieldTested_long_lease_annual.csv","./dataset/UrsusKnifeVioletFieldTested_long_lease_annual_re.csv")
# csv_procession.csv_process_long_lease_price("./dataset/UrsusKnifeVioletFieldTested_long_lease_price.csv","./dataset/UrsusKnifeVioletFieldTested_long_lease_price_re.csv")
# csv_procession.csv_process_short_lease_price("./dataset/UrsusKnifeVioletFieldTested_short_lease_price.csv","./dataset/UrsusKnifeVioletFieldTested_short_lease_price_re.csv")
import re

with open("./dataset/GutAutomaticFieldTested_lease_annual.csv", 'r', encoding='utf-8') as f:
    content = f.read()
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
df.to_csv("./dataset/GutAutomaticFieldTested_lease_annual_re.csv", index=False, encoding='utf-8-sig')