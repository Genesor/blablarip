from ConfigParser import SafeConfigParser
import os

def get_config():
  config = SafeConfigParser()
  config.read(os.path.dirname(os.path.realpath(__file__))+'/config.ini')

  return config
