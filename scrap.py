import os
import json
import yaml
from datetime import datetime, timedelta, timezone
from selenium import webdriver
import chromedriver_binary
import modules.moneyforward_action as mf

with open('config.yml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

now = datetime.now(timezone(timedelta(hours=+9), 'JST'))
now_format = now.isoformat()

driver = webdriver.Chrome()
email = os.environ['MF_EMAIL']
password = os.environ['MF_PASSWORD']

mf_driver = mf.login(driver, email, password)

# get Monthly balance
elements = mf_driver.find_elements_by_css_selector(config['monthly_total']['css_selector'])
monthly_total = {
    '当月収入': mf.format_balance(elements[0].text),
    '当月支出': mf.format_balance(elements[1].text),
    '当月収支': mf.format_balance(elements[2].text)
}

# get portfolio
mf_driver.get(config['portfolio']['url'])
portfolio = {
    '資産総額': mf.format_balance(
        mf_driver.find_element_by_css_selector(config['portfolio']['total_amount']['css_selector']).text
    ),
    '内訳': {}
}
for genre in config['portfolio']['genre']['css_selector']:
    title = mf_driver.find_element_by_css_selector(genre['root'] + genre['title']).text
    amount = mf.format_balance(
        mf_driver.find_element_by_css_selector(genre['root'] + genre['amount']).text
    )
    accounts = mf.table_to_dict(
        mf_driver.find_element_by_css_selector(genre['root'] + genre['table'])
    )
    portfolio['内訳'][title] = {
        '合計': amount,
        '口座情報': accounts
    }

# get liabilities
mf_driver.get(config['liability']['url'])
liability = {
    '負債総額': mf.format_balance(
        mf_driver.find_element_by_css_selector(config['liability']['total_amount']['css_selector']).text
    ),
    '内訳': mf.table_to_dict(
        mf_driver.find_element_by_css_selector(config['liability']['accounts']['css_selector']['table'])
    )
}
mf_driver.quit()

results_json = json.dumps({
    'time': now_format,
    'monthly_total': monthly_total,
    'portfolio': portfolio,
    'liability': liability
})

with open('moneyforward.json', 'w') as stream:
    data = stream.write(results_json)

print("scraping account is successfull!")
