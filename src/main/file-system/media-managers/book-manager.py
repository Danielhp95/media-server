
class BookMediaManager(MediaManager):

    def __init__(self):
        MediaManager.__init__( self )
        self.ROOT_DIR = os.path.join(self.ROOT_MEDIA_DIR, 'books/')
   
    def findBook(self, bookname):
        # Get all books and return only the name
        books = map(lambda a: os.path.splitext(a)[0], self.listAllFiles())
       
        distance_threshold = 3
        
        matches = [match for match in books if levenshtein(match, bookName) < distance_threshold]              
        return matches 

    def findAuthor(self, author):
        authors = map(os.path.basename, os.listdir(self.ROOT_DIR))

        distance_threshold = 3
        
        matches = [match for match in authors if levenshtein(match, author) < distance_threshold]              
        return matches

    def addBook():
        pass
