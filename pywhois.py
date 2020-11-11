# author: @navalmonga
import whois
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from logger import log
from menu import print_menu

whois_tlds = ['wiki', 'is_is', 'co', 'cn', 'ninja', 'cl', 'cc', 'ca', 'ir', 'it', 'rest', 'cz', 'ar', 'video', 'at', 'ac_uk', 'edu', 'download', 'tel', 'education', 'id', 'ru', 'in_', 'pw', 'space', 'tv', 'eu', 'nz', 'pharmacy', 'lv', 'lt', 'online', 'nyc', 'net', 'nu', 'store', 'website', 'be', 'fr', 'io', 'club', 'tickets', 'org', 'de', 'jp', 'site', 'me', 'co_jp', 'ru_rf', 'biz', 'br', 'press', 'fi', 'info', 'mobi', 'name', 'uz', 'xyz', 'theatre', 'us', 'kr', 'sh', 'tech', 'pl', 'uk', 'kz', 'security', 'com', 'mx', 'se']

chrome_options = Options()  
chrome_options.add_argument("--headless") 
browser = webdriver.Chrome(chrome_options=chrome_options)
url = 'https://vercel.com/domains?q='
qLimit = '&limit=24'
browser.get(url + qLimit)

def conduct_login_steps(b):
  time.sleep(1)
  github_auth = b.find_element_by_xpath('/html/body/div/div/div/div[4]/div[1]/div[2]/div/div/span[2]/button').click()
  time.sleep(1)
  github_username = b.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[1]').send_keys('navalmonga')
  github_password = b.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[2]').send_keys('Sg4ap@1214')
  github_signin = b.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[12]').click()
  time.sleep(1)

conduct_login_steps(browser)


def get_who_is(domain):
  try:
    domain_query = whois.query(domain)
    if domain_query:
      if domain_query.registrar and domain_query.registrar != '':
        return domain_query.registrar
      else:
        return ''
    else:
      log("ERROR", "Invalid domain entered, please try again")
  except whois.exceptions.UnknownTld:
    log("ERROR", "(Supported WHOIS TLDs: {})".format(whois_tlds))
    log("ERROR", "> Invalid TLD for domain entered, please try again.")
    return ''

def main():
  log("INFO", "> STARTING whois.py")
  # starting domain search loop
  while True:
    domain_name = raw_input("Enter domain name to search: ").strip()
    log("INFO", "> WHOIS CHECK: " + domain_name)
    
    try:
      # browser.get(url + domain_name + qLimit)
      # wait = WebDriverWait(browser, 10)
      browser.get(url + qLimit)
      time.sleep(1)
      enter_domain = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/form/div/div/div/div[1]/div/div/input').send_keys(domain_name)
      time.sleep(1)
      available = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div/div/ul/li/div/button').get_attribute('class') # == 'INTERNAL_AVAILABLE'
      print(available)
      if 'INTERNAL_AVAILABLE' in available:
        log("SUCCESS", "> SUCCESS: Domain ({}) was found and is available!".format(domain_name))
      if 'INTERNAL_UNAVAILABLE' in browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div/div/ul/li/div/button').get_attribute('class'):
        log("WARN", "> WARN: Domain ({}) was found but is owned by ({})".format(domain_name, get_who_is(domain_name)))
    except:
      if 'INTERNAL_UNAVAILABLE' in browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div/div/ul/li/div/button').get_attribute('class'):
        log("WARN", "> WARN: Domain ({}) was found but is owned by ({})".format(domain_name, get_who_is(domain_name)))
      log("ERROR", "> ERROR: Domain ({}) was not found.".format(domain_name))
    print_menu(domain_name)
    menu_choice = raw_input(': ').strip()
    menu_choice = int(menu_choice.strip('.'))
    if menu_choice == 1:
      new_browser = webdriver.Chrome()
      new_browser.get(url + domain_name + qLimit)
      conduct_login_steps(new_browser)
      continue
    if menu_choice == 2:
      continue
    if menu_choice == 3:
      log('INFO', "Have a great day :)")
      sys.exit()

if __name__ == "__main__":
  main()