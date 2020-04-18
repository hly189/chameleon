#! /usr/bin/env python 

from googleads import adwords
from os import popen 

currentDir = popen("pwd").read().strip()
ymlFile = currentDir + '/googleads.yaml'
adwords_client = adwords.AdWordsClient.LoadFromStorage(ymlFile)
print(type(adwords_client))
