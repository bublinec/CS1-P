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


# III. ADD USER
def get_ratings_l(books: list, ratings_percentage=0.2) -> list:
    """Get n ratings from the user."""

    print("\nRATE BOOKS \nScale (worst to best): -5, -3, 0, 1, 3, 5\n")
    # initialize
    books_len = len(books)
    ratings_n = int(books_len * ratings_percentage)
    ratings_l = ['0'] * books_len

    # ask for ratings_n ratings and save it in the list
    for i in range(atings_n):
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
def calculate_similarity_l(username: str, db) -> list:
    """Return list of similarity of the user with each other user in db."""
    similarity_l = []
    ratings = db['ratings'][username]  # user we are calculating for
    # loop over each user in the dict of users
    for cur_username, cur_ratings in db['ratings'].items():
        if cur_username == username:
            continue
        similarity = 0
        # loop over each book in dict of ratings
        for cur_book, cur_book_rating in cur_ratings.items():
            # if they both red the book calculate the similarity
            if cur_book in ratings:
                similarity += cur_book_rating * ratings[cur_book]
        # finally append the tuple (user, similarity) to the list
        similarity_l.append((cur_username, similarity))
    similarity_l.sort(key=lambda x: x[1], reverse=True)
    return similarity_l


# V.   GET RECCOMENDATIONS
def get_rcm(username: str, similarity_l: list, db: dict, rcm_n=10) -> dict:
    """Crete the dict of books recommended by various users,
     based on the similarity list.
     """
    rcm = {}
    cur_rcm_n = 0
    for cur_user in similarity_l:
        cur_user_rcm_l = []
        for cur_book, cur_rating in db['ratings'][cur_user[0]].items():
            # if the user we are recommending to alread red the book,
            # or it is already recommended, continue
            if (cur_book in db['ratings'][username]) or (cur_book in rcm.values()):
                continue
                # if the book is well rated, add to the list of recommended by the current user
                # increase the number of recommended
            if (cur_rating == 3) or (cur_rating == 5):
                cur_user_rcm_l.append(cur_book)
                cur_rcm_n += 1
                # return dict if we have enough
                if rcm_n <= cur_rcm_n:
                    rcm[cur_user[0]] = cur_user_rcm_l
                    return rcm
        rcm[cur_user[0]] = cur_user_rcm_l


# MAIN FUNCTION
def recommendations():
    db = read_files()

    # II.  GET INPUT - we really don't need function for this
    username = input("Username: ")
    rcm_n = int(input("Reccomendation number: "))

    if username not in db['ratings']:
        add_user(username, db)
    similarity_l = calculate_similarity_l(username, db)
    rcm = get_rcm(username, similarity_l, db, rcm_n)
    print(rcm)


if __name__ == "__main__":
    recommendations()
