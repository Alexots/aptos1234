from selenium.webdriver.common.action_chains import ActionChains
import requests, time
from selenium import webdriver
import random
from multiprocessing import Process
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


ident_follow = ['CharlesXAdkins', 'rgelash', 'dport_apt', 'rpranav', 'alinush407', 'aptoskent', 'wintertoro', 'sherry_apt', 'aptosnames', 'PetraWallet', 'AptosLabs', 'SashaSpiegelman', 'jdhodgkins', 'wgrieskamp', 'rustielin', 'bowen_aptos', 'david_wolinsky', 'neilhar_', 'maxpunger', 'austinvirts', 'Greg_Nazario', 'capcap_max', 'AveryChing', 'moshaikhs', 'aptAlix', 'sitalkedia', 'HC_Xie__', 'aptos_ape', 'zacharyr0th', 'aptosmatt', 'valebrent']


with open('profiles.txt') as file:
    profiles_ads = file.readlines()

if len(profiles_ads) == 0:
    raise Exception('profiles are empty')

for i,v in enumerate(profiles_ads):
    profiles_ads[i] = profiles_ads[i].replace('\n','')
    # profiles_ads[i] = v.replace('\n', ' ')
    # profiles_ads[i] = v.replace(' ','')

print(profiles_ads)




#settings

sleep_from = 10
sleep_to = 20

link_to_go = 'https://twitter.com/intent/follow?screen_name='

button_follow_selector = str("""#layers > div:nth-child(2) > div > div > div > div > div > div.css-1dbjc4n.r-1awozwy.r-1kihuf0.r-18u37iz.r-1pi2tsx.r-1777fci.r-1pjcn9w.r-xr3zp9.r-1xcajam.r-ipm5af.r-9dcw1g > div.css-1dbjc4n.r-z6ln5t.r-14lw9ot.r-1867qdf.r-1jgb5lz.r-pm9dpa.r-1ye8kvj.r-1rnoaur.r-494qqr.r-13qz1uu > div.css-1dbjc4n.r-eqz5dr.r-1hc659g.r-1n2ue9f.r-11c0sde.r-13qz1uu > div.css-18t94o4.css-1dbjc4n.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-16y2uox.r-6gpygo.r-peo1c.r-1ps3wis.r-1ny4l3l.r-1udh08x.r-1guathk.r-1udbk01.r-o7ynqc.r-6416eg.r-lrvibr.r-3s2u2q > div > span > span""")

def start(profile):
    try:
        int(profile)
        dolphin = True
    except:
        dolphin = False
    bad = []
    if dolphin == False:
        try:
            open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + profile
            resp = requests.get(open_url).json()
            service = Service(executable_path=resp["data"]["webdriver"])
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            print("Не могу подключиться к ads и достать driver")

    elif dolphin == True:
        try:
            req_url = f'http://localhost:3001/v1.0/browser_profiles/{profile}/start?automation=1'
            data = requests.get(req_url)
            response_json = data.json()
            print(response_json)
            port = str(response_json['automation']['port'])
            # self.port = port
            options = webdriver.ChromeOptions()
            options.debugger_address = f'127.0.0.1:{port}'
            service = Service(executable_path='chromedriver111/chromedriver/chromedriver-win-x64.exe')
            driver = webdriver.Chrome(service=service, options=options)
            print("Chrome WebDriver setup successful...")
        except:
            raise Exception(f'Error while connecting to dolphin profile {profile}')


    time.sleep(10)
    driver.get('https://galxe.com/aptoslabs/campaign/GCa1NU4Gha')
    window_height = driver.execute_script("return window.innerHeight")

    time.sleep(10)
    window_now = driver.current_window_handle
    # fnd = False
    xpth_list = ["//button[@data-v-4fea166a and @type='button' and @class='v-expansion-panel-header']","//button[@type='button' and @class='v-expansion-panel-header']","//button[@class='v-expansion-panel-header']"]
    for ind in xpth_list:
        try:
            elems = driver.find_elements(By.XPATH,ind)
            break
        except:
            continue
    ch = 0
    time.sleep(10)
    for i in elems:
        dd = True
        ch = ch + 1
        while dd == True:
            try:
            # if True:
                driver.switch_to.window(window_now)
                if driver.current_url.upper() != 'https://galxe.com/aptoslabs/campaign/GCa1NU4Gha'.upper():
                    driver.get('https://galxe.com/aptoslabs/campaign/GCa1NU4Gha')
                    time.sleep(10)

                element_location_y = i.location['y']
                scroll_offset = element_location_y - (window_height / 2)
                driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_offset)
                actions = ActionChains(driver)
                actions.move_to_element(i).perform()

                time.sleep(5)
                i.click()
                time.sleep(random.randint(sleep_from,sleep_to))
                driver.switch_to.window(driver.window_handles[-1])
                if driver.current_url.upper() != 'https://galxe.com/aptoslabs/campaign/GCa1NU4Gha'.upper():
                    driver.close()
                dd = False
            except:
                bad.append(ch)
                try:
                    print('can not follow ' + str(ch))
                except:
                    print('')
                time.sleep(random.randint(sleep_from,sleep_to))

    try:
        print(f'Followed all {len(ident_follow)} except {str(*bad)}')
    except:
        print(ch)

process = []
if __name__ == '__main__':
    print(profiles_ads)
    for name_profile in profiles_ads:
        print(name_profile)
        p = Process(target=start,args=[name_profile])
        p.start()
        time.sleep(3)
        print('Done')

