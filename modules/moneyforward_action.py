def login(driver, email, password):
    driver.get('https://id.moneyforward.com/sign_in/email/');
    driver.implicitly_wait(10);
    email_box = driver.find_element_by_name('mfid_user[email]')
    email_box.send_keys(email)
    email_box.submit()

    print("access to password page....")
    password_box = driver.find_element_by_name('mfid_user[password]')
    password_box.send_keys(password)
    password_box.submit()

    print("access to top page....")
    driver.get('https://moneyforward.com/sign_in/')
    driver.find_element_by_class_name('submitBtn').click()
    return driver

def judge_column_type(column_name):
    if column_name == '残高':
        return 'int'
    elif column_name == '保有数':
        return 'int'
    elif column_name == '平均取得単価':
        return 'int'
    elif column_name == '基準価額':
        return 'int'
    elif column_name == '評価額':
        return 'int'
    elif column_name == '前日比':
        return 'int'
    elif column_name == '評価損益':
        return 'int'
    elif column_name == '評価損益率':
        return 'float'
    elif column_name == '取得価額':
        return 'int'
    elif column_name == '現在価値':
        return 'int'
    elif column_name == 'ポイント・マイル数':
        return 'int'
    elif column_name == '換算レート':
        return 'float'
    elif column_name == '現在の価値':
        return 'int'
    elif column_name == None:
        return 'int'
    else:
        return 'str'

def format_balance(string_price, key_name=None):
    string_price = string_price.strip()
    needles = ['資産総額', '負債総額', '合計', '：', ',', '円', 'ポイント', '%', 'マイル']
    for needle in needles:
        string_price = string_price.replace(needle, '')
    column_type = judge_column_type(key_name)
    if column_type == 'int':
        if string_price == '':
            return 0
        elif string_price == '-':
            return 0
        return int(string_price)
    elif column_type == 'float':
        if string_price == '':
            return 0.0
        elif string_price == '-':
            return 0.0
        return float(string_price)
    else:
        return string_price

def table_to_dict(table):
    results = []
    rows = table.find_elements_by_tag_name('tr')
    keys = rows[0].find_elements_by_tag_name('th')
    rows.pop(0)
    
    for tr in rows:
        account = tr.find_elements_by_tag_name('td')
        result = {}
        for i in range(len(keys)):
            result[keys[i].text] = format_balance(account[i].text, keys[i].text)
        results.append(result)
    return results
