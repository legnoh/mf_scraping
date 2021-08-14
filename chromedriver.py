import time
import os
from selenium import webdriver

driver = webdriver.Chrome()

email = os.environ['MF_EMAIL']
password = os.environ['MF_PASSWORD']

# access to money forward login page
driver.get('https://id.moneyforward.com/sign_in/email/');
print(driver.title)
time.sleep(5)
email_box = driver.find_element_by_name('mfid_user[email]')
email_box.send_keys(email)
email_box.submit()
time.sleep(5)

# password page
print(driver.title)
password_box = driver.find_element_by_name('mfid_user[password]')
password_box.send_keys(password)
password_box.submit()
time.sleep(5)

# move to money forward top page
driver.get('https://moneyforward.com/sign_in/');
time.sleep(5)
print(driver.title)
driver.find_element_by_class_name('submitBtn').click()
time.sleep(10)

# get accounts
print(driver.title)
manual_accounts = driver.find_element_by_id('registered-manual-accounts')
registered_accounts = driver.find_element_by_id('registered-accounts')

print(manual_accounts.text)
print(registered_accounts.text)

driver.quit()
