from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

mc_range_start = 0 
mc_range_end = 0
while True:
    mc_range = input('Enter MC Range(Ex: 0000000-9999999): ')
    if '-' not in mc_range:
        print('Invalid MC Range')
        continue
    mc_range = mc_range.split('-')
    if len(mc_range) != 2:
        print('Invalid MC Range')
        continue
    
    mc_range_start = mc_range[0]
    if not mc_range_start.isdigit():
        print('Invalid Start Value')
        continue
    mc_range_end = mc_range[1]
    if not mc_range_end.isdigit():
        print('Invalid End Value')
        continue
    mc_range_start = int(mc_range_start)
    mc_range_end = int(mc_range_end)
    if mc_range_start > mc_range_end:
        print('Invalid Range')
        continue
    break

chromium = webdriver.ChromiumEdge()
# MC = 1425443
for MC in range(mc_range_start, mc_range_end+1):
    print('\n\n')
    print(f'MC: {MC}'.center(50, '*'))
    chromium.get("https://safer.fmcsa.dot.gov/CompanySnapshot.aspx")
    mc_button = chromium.find_element(By.XPATH,"//input[@id='2']")
    mc_button.click()
    mc_input = chromium.find_element(By.XPATH,"//input[@id='4']")
    mc_input.send_keys(str(MC))
    mc_button = chromium.find_element(By.XPATH,"//input[@type='SUBMIT']")
    mc_button.click()

    try:
        entity_type = WebDriverWait(chromium, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[2]/td"))
        )
        print(f'{entity_type.text.strip()}'.center(50, '*'))
        if 'CARRIER' in entity_type.text.strip() and 'BROKERAGE' not in entity_type.text.strip():
            operating_status = chromium.find_element(By.XPATH,"/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[3]/td[1]")
            # print(f'{operating_status.text.strip()}'.center(50, '*'))
            if operating_status.text.strip() != 'NOT AUTHORIZED':
                print('Authorized'.center(50, '*'))
                mc_date = chromium.find_element(By.XPATH,"/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[12]/td[1]")
                print(f'{mc_date.text.strip()}'.center(50, '*'))
                sms_result = chromium.find_element(By.XPATH,"/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/font/a")
                sms_result.click()
                carrier_registration_dets_button = WebDriverWait(chromium, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="CarrierRegistration"]/a[1]'))
                )
                carrier_registration_dets_button.click()
                legal_name = WebDriverWait(chromium, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="regBox"]/ul[1]/li[1]/span'))
                )
                print(f'{legal_name.text.strip()}'.center(50, '*'))
                address = chromium.find_element(By.XPATH, '//*[@id="regBox"]/ul[1]/li[4]/span')
                print('{}'.format(str(address.text).replace("\n", "").strip()).center(50, '*'))
                phone_number = chromium.find_element(By.XPATH, '//*[@id="regBox"]/ul[1]/li[5]/span')
                print(f'{phone_number.text.strip()}'.center(50, '*'))
                email = chromium.find_element(By.XPATH, '//*[@id="regBox"]/ul[1]/li[7]/span')   
                print(f'{email.text.strip()}'.center(50, '*'))
    except Exception as e:
        print(f'MC not Active: {MC}'.center(50, '*'))
        # print(e)
time.sleep(5)
chromium.quit()

print('COMPLETED')