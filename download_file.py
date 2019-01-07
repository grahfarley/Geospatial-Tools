
import scrapy
import os
from pipedreams.items import PipedreamsItem
x = PipedreamsItem()

os.chdir("C:\Users\graham.farley\Documents\Documents\TiffSpid")
with open('links.txt') as f:
    data = f.readlines()
os.chdir("C:\Users\graham.farley\Documents\Documents\pipedreams")

i = 0

class PipeSpider(scrapy.Spider):
    name = "pipe"
    start_urls = ["http://geodata.lib.ncsu.edu/NAIP/NAIP16/Tiles_in_TIFF_format_UTM/"]

    custom_settings = {
        'DOWNLOAD_MAXSIZE': 0,
        'DOWNLOAD_WARNSIZE': 0,
        'DOWNLOAD_TIMEOUT': 10000,
        'REDIRECT_ENABLED' : False,
        'MEDIA_ALLOW_REDIRECT' : True,
        #'DOWNLOAD_FAIL_ON_DATALOSS' : False,
        }

    

    def parse(self, response):
        x['file_urls'] = data
