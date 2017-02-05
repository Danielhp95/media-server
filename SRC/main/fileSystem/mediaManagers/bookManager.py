
import mediaManager 

class BookMediaManager(mediaManager.MediaManager):

    def __init__(self):
        MediaManager.__init__( self )
        self.ROOT_DIR = os.path.join(self.ROOT_MEDIA_DIR, 'books/')
   
    def findBook(self, bookname):
        # Get all books and return only the name
        books = map(lambda a: os.path.splitext(a)[0], self.listAllFiles())
       
        distance_threshold = 3
        
        matches = [match for match in books if stringUtils.levenshtein(match, bookName) < distance_threshold]              
        return matches 

    def findAuthor(self, author):
        authors = map(os.path.basename, os.listdir(self.ROOT_DIR))

        distance_threshold = 3
        
        matches = [match for match in authors if stringUtils.levenshtein(match, author) < distance_threshold]              
        return matches

    # A book will just be a dictionary. Main fields are title and author
    # Parameter file is expected to be the FULL path to the directory
    def addBook(self, book, file):
        name   = book['name']
        author = book['author']
        # may want to format the name/author

        # check that file still there
        if not os.path.isfile(os.path.abspath(file)):
            # log that book did not exist
            print('Book ' + name + ' by ' + author + ' was not found')

      
        # Add author to library if it is not already there 
        authorDirectory = os.path.join(ROOT_DIR, author)
        if not os.path.isdir(authorDirectory):
            print('New author added to library: ' + author)
            os.mkdir(authorDirectory)

        # Add file
        if os.path.isfile(os.path.join(authorDirectory, name)):
            print('Book ' + name + ' by ' + ' already exists in library')
        else:
            os.rename(file, os.path.join(authorDirectory, name))
            print('Book ' + name + ' by ' + ' added to library')
            

    def addSource(self, newSource):
        pass
        
