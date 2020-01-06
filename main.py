import json

from aiohttp import ClientConnectorError

from sauce import Sauce
from file_renamer import File_Renamer
from saucenao import exceptions
import ipaddress
import sys
import os
import logging
import re

with open('config.json') as json_file:
    data = json.load(json_file)
    apiKey = data['apiKey']
    similarity = data['similarity']
    loglevel = data['loglevel']

if loglevel == "INFO":
    loglevel = logging.INFO
elif loglevel == "DEBUG":
    loglevel = logging.DEBUG
elif loglevel == "ERROR":
    loglevel = logging.ERROR
elif loglevel == "WARNING":
    loglevel = logging.WARNING
elif loglevel == "CRITICAL:":
    loglevel = logging.CRITICAL

logging.basicConfig(format='%(asctime)s - %(message)s [%(levelname)s]', datefmt='%d-%b-%y %H:%M:%S', level=loglevel)
logging.info("Starting!")
workingDirectory = sys.argv[1]

thesauce = Sauce(workingDirectory, apiKey, similarity)
renamer = File_Renamer(workingDirectory)

for filename in os.listdir(workingDirectory):
    if filename.startswith("unclassified"):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            while True:
                try:
                    sauceData = thesauce.getSauce(filename)
                    renamer.rename(sauceData, filename)
                except exceptions.DailyLimitReachedException as error:
                    logging.critical(error)
                    logging.critical("A critical error has occurred and the application cannot continue!")
                    exit(1)
                except OSError as error:
                    logging.critical("A critical error has occurred and the application cannot continue!")
                else:
                    break

logging.info("Done!")

