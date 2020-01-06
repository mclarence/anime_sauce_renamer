# Anime Sauce Renamer

Anime Sauce Renamer is a python script which renames files based on their source obtained from [SauceNao](https://saucenao.com/). The new file name will include either material, characters, pixiv id, gelbooru id and so on.

## Requirements
* Python 3.6.7
* [SauceNAO API wrapper](https://github.com/DaRealFreak/saucenao) by DaRealFreak
* unicode_slugify
* aiohttp

These all can be install with pip.

## Installation

Download the repository and install any required modules with:

```bash
pip install -r requirements.txt
```
Create a `config.json` file within the same directory of the script with the following contents:
```json
{
    "apiKey": "",
    "similarity": 80,
    "loglevel": "INFO"
}
```
* `apiKey` - SauceNAO.com api key. Can be obtained for free by making an account on the site.
* `similarity` - The similarity of SauceNao returned results and the local image. Recommended percentage is 80.
* `loglevel` - The logging level. Can be either `INFO`, `DEBUG`, `WARN` or `CRITICAL`
## Usage
Place all images you want to rename in a folder. Rename all images so that they begin with "unclassified". It is imperitve that each of the images file names begin with "unclassified" otherwise the script won't rename the image. Examples of valid file names include:

* `unclassified1.png`
* `unclassified_2.png`
* `unclassifiedImg1.jpg`

PNG and JPG are supported only.

```python
python main.py <directory>
```
* `directory` - The directory of images to be renamed.

Unknown images will be renamed to "unknown.jpg/.png"

## Known Issues
* The SauceNao API is limited to 200 searches per day, per api key, per ip address for free users. Hence 200 images can only be renamed per day. You are able to do more searches by purchasing a required amount on the SauceNao website or if you don't want to pay anything you can use a VPN with a new API key by signing up again on the website.

## To Do
* Add proxy support.

## License
[MIT](https://choosealicense.com/licenses/mit/)