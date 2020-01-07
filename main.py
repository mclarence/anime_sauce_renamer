import json
from Services.SauceNaoService import SauceNaoService
from Services.IqdbService import IqdbService
from file_renamer import File_Renamer
from saucenao import exceptions
import os
import logging
import argparse
import ntpath

parser = argparse.ArgumentParser()
parser.add_argument("fileOrDirectory", help="The file or directory to rename image(s).", type=str)
parser.add_argument("service", help="The service to lookup the image. 'saucenao', 'iqdb' or 'auto' is accepted.",
                    type=str)
parser.add_argument("--verbose", help="Increase output verbosity.", action="store_true")
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s [%(levelname)8s] - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
logging.info("Loading configuration.")
with open('config.json') as json_file:
    try:
        data = json.load(json_file)
    except ValueError as e:
        print(e)
        logging.error("Unable to load configuration file!")
        logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
        exit(1)

    apiKey = data['apiKey']
    if type(apiKey) != str:
        logging.error("Invalid API Key! Must be string.")
        logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
        exit(1)
    logging.debug("SauceNao API Key = " + (apiKey[:20] + '..'))

    similarity = data['similarity']
    try:
        int(similarity)
    except ValueError:
        try:
            float(similarity)
        except ValueError:
            logging.error("Invalid similarity value! Must be a float or string.")
            logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
            exit(1)

    loglevel = data['loglevel']
    if loglevel not in ["INFO", "DEBUG", "ERROR", "WARNING", "CRITICAL"]:
        logging.error(
            "Invalid log level specified! Must be either INFO, DEBUG, ERROR, WARNING or CRITICAL. Defaulting to INFO")
        loglevel = logging.INFO
    else:
        if args.verbose:
            logging.info("Verbosity enabled.")
            loglevel = logging.DEBUG
        else:
            if loglevel == "INFO":
                loglevel = logging.INFO
                logging.info("Log level set to INFO.")
            elif loglevel == "DEBUG":
                loglevel = logging.DEBUG
                logging.info("Log level set to DEBUG.")
            elif loglevel == "ERROR":
                loglevel = logging.ERROR
                logging.info("Log level set to ERROR.")
            elif loglevel == "WARNING":
                loglevel = logging.WARNING
                logging.info("Log level set to WARNING.")
            elif loglevel == "CRITICAL:":
                loglevel = logging.CRITICAL
                logging.info("Log level set to CRITICAL.")
    logging.getLogger().setLevel(loglevel)
logging.info("Configuration loaded.")
logging.info("Starting! ε=ε=ε=ε=┌(;￣▽￣)┘")

fileOrDirectory = args.fileOrDirectory

if os.path.exists(fileOrDirectory):
    if os.path.isdir(fileOrDirectory):
        if args.service == "saucenao":
            searchService = SauceNaoService(fileOrDirectory, apiKey, similarity)
        elif args.service == "iqdb":
            searchService = IqdbService(fileOrDirectory)
        elif args.service == "auto":
            searchService = SauceNaoService(fileOrDirectory, apiKey, similarity)
        else:
            searchService = SauceNaoService(fileOrDirectory, apiKey, similarity)

        renamer = File_Renamer(fileOrDirectory)
        filesToRename = os.listdir(fileOrDirectory)
        if len(filesToRename) > 199:
            logging.warning("This session may exceed SauceNao API daily search limit!")
        elif len(filesToRename) == 0:
            logging.warning("There are no files to check and rename! ┐('～`;)┌")
            logging.info("Done! ヽ(*⌒▽⌒*)ﾉ")
            exit(1)

        unclassifiedFileCount = 0
        for filename in filesToRename:
            if filename.startswith("unclassified"):
                unclassifiedFileCount += 1

        if unclassifiedFileCount == 0:
            logging.warning("There were files in this directory but none of them started with unclassified! ┐('～`;)┌")
            logging.info("Done! ヽ(*⌒▽⌒*)ﾉ")
            exit(1)

        for filename in filesToRename:
            if filename.startswith("unclassified"):
                logging.info("I will now be checking and renaming " + str(unclassifiedFileCount) + " file(s) :)")
                if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                    while True:
                        try:
                            sauceData = searchService.getSauce(filename)
                            if sauceData.resultsFound == False and args.service == 'auto':
                                logging.warning("No results returned from SauceNao for file " + filename)
                                logging.warning("'auto' specified, using iqdb")
                                sauceData = IqdbService(fileOrDirectory).getSauce(filename)
                                if sauceData.resultsFound == False:
                                    logging.warning("No results returned from both services for file " + filename)
                            renamer.rename(sauceData, filename)
                        except exceptions.DailyLimitReachedException as error:
                            logging.error(error)
                            logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
                            exit(1)
                        except OSError as error:
                            logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
                            exit(1)
                        except Exception as error:
                            logging.error(error)
                            logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
                            exit(1)
                        else:
                            break
    if os.path.isfile(fileOrDirectory):
        filename = ntpath.basename(fileOrDirectory)
        filepath = os.path.dirname(os.path.abspath(fileOrDirectory))
        if args.service == "saucenao":
            searchService = SauceNaoService(filepath, apiKey, similarity)
        elif args.service == "iqdb":
            searchService = IqdbService(filepath)
        elif args.service == "auto":
            searchService = SauceNaoService(filepath, apiKey, similarity)
        else:
            searchService = SauceNaoService(filepath, apiKey, similarity)
        renamer = File_Renamer(filepath)
        logging.info("I will now be checking and renaming " + filename + " :)")
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            while True:
                try:
                    sauceData = searchService.getSauce(filename)
                    if sauceData.resultsFound == False and args.service == 'auto':
                        logging.warning("No results returned from SauceNao for file " + filename)
                        logging.warning("'auto' specified, using iqdb")
                        sauceData = IqdbService(filepath).getSauce(filename)
                        if sauceData.resultsFound == False:
                            logging.warning("No results returned from both services for file " + filename)
                    renamer.rename(sauceData, filename)
                except exceptions.DailyLimitReachedException as error:
                    logging.error(error)
                    logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
                    exit(1)
                except OSError as error:
                    logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
                    exit(1)
                except Exception as error:
                    logging.error(error)
                    logging.critical("A critical error has occurred and the application cannot continue! (-_-)")
                    exit(1)
                else:
                    break

logging.info("Done! ヽ(*⌒▽⌒*)ﾉ")
