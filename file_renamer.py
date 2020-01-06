from resultData import ResultData
import shutil
import os
from slugify import slugify
import logging
class File_Renamer:
    def __init__(self, workingDirectory):
        self.workingDirectory = workingDirectory
        self.logger = logging.getLogger(__name__)

    def rename(self, sauceData: ResultData, filename: str):
        fn_strings = []
        for attr, value in sauceData.__dict__.items():
            if value is not None or not "":
                if attr == 'resultsFound':
                    if not value:
                        fn_strings.append("unknown")
                        break
                    else:
                        continue
                elif attr == 'material':
                    fn_strings.append(value)
                elif attr == 'characters':
                    if fn_strings[0] is not None:
                        if fn_strings[0] in value or fn_strings[0] is not "":
                            del fn_strings[0]
                    else:
                        del fn_strings[0]
                        continue
                    fn_strings.append(value[0])
                elif attr == 'pixiv_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("pixiv")
                    fn_strings.append(str(value))
                    break
                elif attr == 'nijie_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("nijie")
                    fn_strings.append(str(value))
                    break
                elif attr == 'seiga_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("seiga")
                    fn_strings.append(str(value))
                    break
                elif attr == 'anidb_aid':
                    if value is None or value is "":
                        continue
                    fn_strings.append("anidb")
                    fn_strings.append(str(value))
                    break
                elif attr == 'pawoo_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("pawoo")
                    fn_strings.append(str(value))
                    break
                elif attr == 'bcy_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("bcy")
                    fn_strings.append(str(value))
                    break
                elif attr == 'da_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("da")
                    fn_strings.append(str(value))
                    break
                elif attr == 'gelbooru_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("gelbooru")
                    fn_strings.append(str(value))
                    break
                elif attr == 'danbooru_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("danbooru")
                    fn_strings.append(str(value))
                    break
                elif attr == 'yandere_id':
                    if value is None or value is "":
                        continue
                    fn_strings.append("yandere")
                    fn_strings.append(str(value))
                    break

        if filename.endswith(".jpg"):
            ext = ".jpg"
        else:
            ext = ".png"
        newFileName = slugify("_".join(fn_strings))

        if os.path.isfile(os.path.join(self.workingDirectory, newFileName)):
            count = 1
            while os.path.isfile(os.path.join(self.workingDirectory, newFileName)):
                newFileName = newFileName + "_" + str(count)
                count = count + 1
        try:
            shutil.move(os.path.join(self.workingDirectory, filename), os.path.join(self.workingDirectory, newFileName + ext))
        except OSError as error:
            self.logger.error("An I/O error has occurred. Could not rename file!")
            raise error
        else:
            self.logger.info("Renamed " + filename + " to " + newFileName + ext)









