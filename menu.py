from logger import log
def print_menu(domain):
  log("INFO", "What do you want to do next?")
  print("")
  log("INFO", "--------------------------------------------------------------------------------")
  print("")
  log("WARN", "1. Open up vercel.com/domains to purchase ({})------------------------------".format(domain))
  print("")
  log("WARN", "2. Keep on searching domains----------------------------------------------------")
  print("")
  log("WARN", "3. Quit vercel_whois.py----------------------------------------------------------------")
  print("")