import re
FLOAT_LIST=["FactoryNew","MinimalWar","FieldTested","WellWorn","BattleScarred"]
FLOAT_LIST_CN=["崭新出厂","略有磨损","久经沙场","破损不堪","战痕累累"]
NAME_LIST=["Ursus_Knife","Bowie_Knife","Nomad_Knife","Flip_Knife","jisheng_Knife","Huntsman_Knife","SealKnife","Gut"]
NAME_LIST_CN=["熊刀","鲍伊猎刀","流浪者匕首","折叠刀","系绳匕首","猎杀者匕首","海豹短刀","穿肠刀"]
SKIN_LIST=["Violet","beifang_senlin","senlin_ddpat","Dama","Automatic","rengong_ranse","Freedom","Blue_Steel","Legend","Clean_Water","Black_Laminate"]
SKIN_LIST_CN=["致命紫罗兰","北方森林","森林 DDPAT","大马士革钢","自动化","人工染色","自由之手","蓝钢","传说","澄澈之水","黑色层压板"]
def translate_good_name(good_name):
    for en, cn in zip(FLOAT_LIST, FLOAT_LIST_CN):
        if cn in good_name:  # 如果中文部分在 good_name 中出现
            good_name = good_name.replace(cn, en)  # 替换为英文

    for en, cn in zip(NAME_LIST, NAME_LIST_CN):
        if cn in good_name:  # 如果中文部分在 good_name 中出现
            good_name = good_name.replace(cn, en)  # 替换为英文

    for en, cn in zip(SKIN_LIST, SKIN_LIST_CN):
        if cn in good_name:  # 如果中文部分在 good_name 中出现
            good_name = good_name.replace(cn, en)  # 替换为英文
    good_name_new=re.sub(r'[^a-zA-Z0-9]', '', good_name)
    return good_name_new
