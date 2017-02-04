import os
import re

# Surely there is a nicer way to go around this
import sys

import book-manager

sys.path.insert(0, '../utils')

import stringUtils


class MediaManager():

    def __init__(self):
        self.ROOT_MEDIA_DIR = os.path.dirname(os.path.abspath('media/'))
        self.bookManager = BookMediaManager()
        os.mkdir(os.path.join(self.ROOT_MEDIA_DIR, '.sources')) # creates source files for scraper

    def createMedia(self, newMedia):
        newMediaDirectory = os.path.join(ROOT_MEDIA_DIR, newMedia)
        if os.path.isdir(newMediaDirectory):
            print('Media ' + newMedia + ' already exists')
        else:
            os.mkdir(os.path.join(self.ROOT_MEDIA_DIR, newMedia))
    
    # TODO: fix  ROOT_DIR? 
    def listAllFiles = lambda: [x for x in os.walk(self.ROOT_DIR) if os.path.isfile(x)]

    def addSource(self):
        pass

