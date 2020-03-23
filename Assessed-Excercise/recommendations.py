# I.   READ FILES
def read_books(books_filename="books.txt") -> list:
    books = []
    with open(books_filename) as f:
        for line in f:
            book = line.strip().split(',')  # to list
            book = (book[0], book[1])  # to tupleer
            books.append(book)
    return books


def read_users(books: list, users_filename="ratings.txt") -> dict:
    users = {}
    with open(users_filename) as f:
        while True:
            username = f.readline().strip()
            if not username:
                break  # EOF
            ratings = f.readline().strip().split(' ')
            # convert ratings list to dict
            ratings = {books[i]: int(ratings[i]) for i in range(len(ratings)) if ratings[i] != '0'}
            users[username] = ratings
    return users


def get_db(books_filename="books.txt", users_filename="ratings.txt") -> dict:
    """Read the data from files and return the database."""
    books = read_books()
    users = read_users(books)
    db = {
        'books': books,
        'users': users
    }
    return db





# II.  GET INPUT
def get_input() -> list:
    """
    Get the username and number of recommendations from the user,
    using command line and return it as a tuple: (username, rcm_n)
    """
    pass


# III. ADD USER
def get_rcm(n: int) -> list:
    """Get n recommendations from the user"""
    pass


def add_user(username: str, rcm: list, db="db"):
    """Post user into the database and write into the file."""
    pass


# IV.  CALCULATE SIMILARITY
def dot_prodcut(a: list, b: list) -> int:
    """Return the dot product of vectors a and b."""
    pass


def calculate_similarity(username: str, db="db") -> list:
    """Return list of similarity of the user with each other user in db."""
    pass


# V.   GET RECCOMENDATIONS
def get_rcm(similarity: list, db="db") -> dict:
    """Crete the dict of books recommended by various users, based on the similarity."""
    pass

# MAIN FUNCTION
def recommendations():
    pass




if __name__ == "__main__":
    db = get_db()
    print(db)