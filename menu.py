from logger import log
def print_menu(domain):
  log("INFO", "What do you want to do next?")
  log("INFO", "--------------------------------------------------------------------------------")
  log("WARN", "1. Open up vercel.com/domains to purchase {}------------------------------".format(domain))
  log("WARN", "2. Keep on searching domains----------------------------------------------------")
  log("WARN", "3. Quit whois.py----------------------------------------------------------------")