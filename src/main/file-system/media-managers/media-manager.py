import os
import re

# Surely there is a nicer way to go around this
import sys

sys.path.insert(0, '../utils')

import stringUtils


class MediaManager():

    def __init__(self):
        self.ROOT_MEDIA_DIR = os.path.dirname(os.path.abspath('media/'))

    def createMedia(newMedia):
        try:
            os.mkdir(os.path.join(ROOT_MEDIA_DIR, newMedia))
        except FileExistsError:
            print('Media ' + newMedia + ' already exists')
    
    # TODO: fix  ROOT_DIR? 
    def listAllFiles = lambda: [x for x in os.walk(self.ROOT_DIR) if os.path.isfile(x)]
