from termcolor import colored
def log(level, msg):
  level_switch = {
    "INFO": "cyan",
    "WARN": "yellow",
    "ERROR": "red",
    "SUCCESS": "green",
    "": "white",
  }
  print(colored(msg, level_switch.get(level))),