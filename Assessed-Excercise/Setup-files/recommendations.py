# I.   GET DATA
def get_data(books_file="books.txt", ratings_file="ratings.txt") -> dict:
    """Read the data from files and return the database."""
    


# II.  GET INPUT
def get_input() -> list:
    """
    Get the username and number of recommendations from the user,
    using command line and return it as a tuple: (username, rcm_n)
    """
    pass


# III. ADD USER
def get_rcm(n:int) -> list:
    """Get n recommendations from the user"""
    pass

def add_user(username:str, rcm: list, , db="db"):
    """Post user into the database and write into the file."""
    pass

# IV.  CALCULATE SIMILARITY
def dot_prodcut(a:list, b:list) -> int:
    """Return the dot product of vectors a and b."""
    pass

def calculate_similarity(username:str, db="db") -> list:
    """Return list of similarity of the user with each other user in db."""
    pass

# V.   GET RECCOMENDATIONS
def get_rcm(similarity:list, , db="db") -> dict:
    """Crete the dict of books recommended by various users, based on the similarity."""
    pass




# MAIN FUNCTION
def recommendations():
    pass


if __name__ = "__main__":
    recommendations()