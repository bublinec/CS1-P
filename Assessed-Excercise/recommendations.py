from random import randrange


# I.   READ FILES
def read_books(books_filename="books.txt") -> list:
    books = []
    with open(books_filename) as f:
        for line in f:
            book = line.strip().split(',')  # to list
            book = (book[0], book[1])  # to tuple
            books.append(book)
    return books


def ratings_l_to_d(ratings_l: list, books: list) -> dict:
    return {books[i]: int(ratings_l[i]) for i in range(len(ratings_l)) if ratings_l[i] != '0'}


def read_ratings(books: list, ratings_filename="ratings.txt") -> dict:
    ratings = {}
    with open(ratings_filename) as f:
        while True:
            username = f.readline().strip()
            # cheack EOF
            if not username:
                break
            ratings_l = f.readline().strip().split(' ')
            ratings[username] = ratings_l_to_d(ratings_l, books)
    return ratings


def read_files(books_filename="books.txt", ratings_filename="ratings.txt") -> dict:
    """Read the data from files and return the database."""
    books = read_books()
    ratings = read_ratings(books)
    db = {
        'books': books,
        'ratings': ratings
    }
    return db


# II.  GET INPUT
def get_input(output_filename="output.txt") -> tuple:
    """
    Get the username and number of recommendations from the user,
    using command line and return it as a tuple: (username, rcm_n).
    """
    username = input("Username: ")
    rcm_n = int(input("Reccomendation number: "))
    return(username, rcm_n)


# III. ADD USER
def get_ratings_l(books: list, rcm_p=0.2) -> list:
    """Get n ratings from the user."""

    print("\nRATE BOOKS \nScale (worst to best): -5, -3, 0, 1, 3, 5\n")
    # initialize
    books_len = len(db['books'])
    rcm_n = int(books_len * rcm_p)  # rcm_p = 20% as specified
    ratings_l = ['0'] * books_len

    # ask for rcm_n ratings and save it in the list
    for i in range(rcm_n):
        book_i = randrange(books_len)
        # generate new book index until unrated
        while ratings_l[book_i] != '0':
            book_i = randrange(books_len)
        book = books[book_i]
        rating = input(book[0] + ", " + book[1] + ": ")
        ratings_l[book_i] = rating
    return ratings_l


def add_user(username: str, db: dict, ratings_filename="ratings.txt"):
    """Post user into the database and write into the file."""
    ratings_l = get_ratings_l(db['books'])

    # add user to ratings file
    with open(ratings_filename, 'a') as f:
        f.write(username + '\n' + ' '.join(ratings_l) + '\n')
        
    # add user to database
    db['ratings'][username] = ratings_l_to_d(ratings_l, db['books'])



# IV.  CALCULATE SIMILARITY
def dot_prodcut(a: list, b: list) -> int:
    """Return the dot product of vectors a and b."""
    pass


def calculate_similarity(username: str, db="db") -> list:
    """Return list of similarity of the user with each other user in db."""
    pass


# V.   CALCULATE RECCOMENDATIONS
def calculate_rcm(similarity: list, db="db") -> dict:
    """Crete the dict of books recommended by various users, based on the similarity."""
    pass

# MAIN FUNCTION
def recommendations():
    pass




if __name__ == "__main__":
    db = read_files()
    user_input = get_input() 
    if user_input[0] not in db['ratings']:
        add_user(user_input[0], db)