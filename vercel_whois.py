# author: @navalmonga
import os
import time
import sys
import json
import whois
from dotenv import load_dotenv
load_dotenv()
from pyfiglet import figlet_format
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from logger import log
from menu import print_menu

# supported tlds
whois_tlds = ['wiki', 'is_is', 'co', 'cn', 'ninja', 'cl', 'cc', 'ca', 'ir', 'it', 'rest', 'cz', 'ar', 'video', 'at', 'ac_uk', 'edu', 'download', 'tel', 'education', 'id', 'ru', 'in_', 'pw', 'space', 'tv', 'eu', 'nz', 'pharmacy', 'lv', 'lt', 'online', 'nyc', 'net', 'nu', 'store', 'website', 'be', 'fr', 'io', 'club', 'tickets', 'org', 'de', 'jp', 'site', 'me', 'co_jp', 'ru_rf', 'biz', 'br', 'press', 'fi', 'info', 'mobi', 'name', 'uz', 'xyz', 'theatre', 'us', 'kr', 'sh', 'tech', 'pl', 'uk', 'kz', 'security', 'com', 'mx', 'se']

chrome_options = Options()  
# chrome_options.add_argument("--headless") 
browser = webdriver.Chrome(executable_path="./chromedriver",chrome_options=chrome_options)
url = 'https://vercel.com/domains?q='
qLimit = '&limit=24'
browser.get(url + qLimit)

def conduct_login_steps(b):
  time.sleep(1)
  github_auth = b.find_element_by_xpath('/html/body/div/div/div/div[4]/div[1]/div[2]/div/div/span[2]/button').click()
  time.sleep(1)
  username = os.environ.get("GITHUB_USERNAME")
  password = os.environ.get("GITHUB_PASSWORD")
  github_username = b.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[1]').send_keys(username)
  github_password = b.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[2]').send_keys(password)
  github_signin = b.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[12]').click()
  time.sleep(1)

conduct_login_steps(browser)

def welcome_message():
  log("INFO", figlet_format('Vercel-WHOIS', width=80, justify="center"))
  print("")

def get_who_is(domain):
  try:
    domain_query = whois.query(domain)
    if domain_query:
      if domain_query.registrar and domain_query.registrar != '':
        domain_query_json = {
          'status': domain_query.status,
          'name': domain_query.name,
          'registrar': domain_query.registrar,
          'name_servers': list(domain_query.name_servers)
        }
        log("INFO", (json.dumps(domain_query_json, indent=2)))
        print("")
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
  welcome_message()
  log("INFO", "> ")
  # starting domain search loop
  while True:
    domain_name = raw_input("Enter domain name to search: ").strip()
    log("INFO", " >  WHOIS: ({})".format(domain_name))
    print("")
    is_domain_found = False
    try:
      # browser.get(url + domain_name + qLimit)
      # wait = WebDriverWait(browser, 10)
      # time.sleep(2)
      browser.get(url + qLimit)
      time.sleep(1)
      clear_domain = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/form/div/div/div/div[1]/div/div/input').clear()
      time.sleep(1)
      # browser.get(url + domain_name + qLimit)
      enter_domain = browser.find_element_by_xpath('//html/body/div/div/div/div[2]/div/form/div/div/div/div[1]/div/div/input').send_keys(domain_name)
      time.sleep(1)
      the_input_value = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/form/div/div/div/div[1]/div/div/input').get_attribute('value')
      log("INFO","> Checking ({})".format(the_input_value))
      time.sleep(1)
      available = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div/div[1]/ul/li[1]/div/button').get_attribute('class') # == 'INTERNAL_AVAILABLE'
      print(available)
      if 'INTERNAL_AVAILABLE' in available:
        log("SUCCESS", "> SUCCESS: Domain ({}) was found and available for purchase!".format(domain_name))
        print("")
        is_domain_found = True
      elif 'INTERNAL_UNAVAILABLE' in available:
        log("WARN", "> WARN: Domain ({}) is owned and registered by ({})".format(domain_name, get_who_is(domain_name)))
        print("")
      print_menu(domain_name, is_found=is_domain_found)
      menu_choice = raw_input(': ').strip()
      menu_choice = int(menu_choice.strip('.'))
      if menu_choice == 1:
        new_browser = webdriver.Chrome()
        new_browser.get(url + domain_name + qLimit)
        conduct_login_steps(new_browser)
        continue
      if menu_choice == 2:
        clear_domain = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/form/div/div/div/div[1]/div/div/input')
  
        # browser.find_element_by_id('input-query').send_keys(Keys.CONTROL + "a")
        # browser.find_element_by_id('input-query').send_keys(Keys.DELETE)
        # time.sleep(2)
        continue
        # sys.exit()
      if menu_choice == 3:
        log('INFO', "Have a great day :)")
        sys.exit()
    except Exception as e:
      print(e)
      # if 'INTERNAL_UNAVAILABLE' in browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div/div/div/ul/li/div/button').get_attribute('class'):
      #   log("WARN", "> WARN: Domain ({}) was found but is owned by ({})".format(domain_name, get_who_is(domain_name)))
      log("ERROR", "> ERROR: Domain ({}) was not found.".format(domain_name))

if __name__ == "__main__":
  log("INFO", "Logged in to Vercel.com with GitHub OAuth...")
  print("")
  main()