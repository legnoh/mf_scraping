import os
import json
import yaml
from datetime import datetime, timedelta, timezone
from selenium import webdriver
import chromedriver_binary
import lib.moneyforward_action as mf

with open('config.yml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

now = datetime.now(timezone(timedelta(hours=+9), 'JST'))
now_format = now.isoformat()

driver = webdriver.Chrome()
email = os.environ['MF_EMAIL']
password = os.environ['MF_PASSWORD']

mf_driver = mf.login(driver, email, password)

# get Monthly balance
elements = mf_driver.find_elements_by_css_selector(config['balance']['css_selector'])
budget = {
    'income': mf.format_balance(elements[0].text),
    'expense': mf.format_balance(elements[1].text),
    'balance': mf.format_balance(elements[2].text)
}

# get portfolio
mf_driver.get(config['portfolio']['url'])
portfolio = {
    'total_amount': mf.format_balance(
        mf_driver.find_element_by_css_selector(config['portfolio']['total_amount']['css_selector']).text
    ),
    'genre': {}
}
for genre in config['portfolio']['genre']['css_selector']:
    title = mf_driver.find_element_by_css_selector(genre['root'] + genre['title']).text
    amount = mf.format_balance(
        mf_driver.find_element_by_css_selector(genre['root'] + genre['amount']).text
    )
    accounts = mf.table_to_dict(
        mf_driver.find_element_by_css_selector(genre['root'] + genre['table'])
    )
    portfolio['genre'][title] = {
        'amount': amount,
        'accounts': accounts
    }

# get liabilities
mf_driver.get(config['liability']['url'])
liability = {
    'total_amount': mf.format_balance(
        mf_driver.find_element_by_css_selector(config['liability']['total_amount']['css_selector']).text
    ),
    'accounts': mf.table_to_dict(
        mf_driver.find_element_by_css_selector(config['liability']['accounts']['css_selector']['table'])
    )
}
mf_driver.quit()

results_json = json.dumps({
    'time': now_format,
    'budget': budget,
    'portfolio': portfolio,
    'liability': liability
})

with open('moneyforward.json', 'w') as stream:
    data = stream.write(results_json)

print("scraping account is successfull!")
