from random import randrange
import os


# I.   READ FILES
def read_books(books_filename="books.txt") -> list:
    """Return False if the file does not exist."""
    if not os.path.exists(books_filename): 
        print("\nERROR: The file \"", books_filename, "\" does not exist.")
        return False

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
    """Return False if reading file failed."""
    if not os.path.exists(ratings_filename):
        print("\nERROR: The file \"", ratings_filename, "\" does not exist.\n")
        return False

    ratings = {}
    with open(ratings_filename) as f:
        while True:
            username = f.readline().strip()
            # cheack EOF
            if not username:
                break
            ratings_l = f.readline().strip().split(' ')
            try:
                ratings[username] = ratings_l_to_d(ratings_l, books)
            except ValueError:
                print("\nSome fo the ratings in the file is not an integer.")
                return False
    return ratings


def read_files(books_filename="books.txt", ratings_filename="ratings.txt") -> dict:
    """
    Read the data from files and return the database.
    Return false if the files does not exist.
    """
    books = read_books()
    if not books:
        return False
    ratings = read_ratings(books)
    if not ratings:
        return False

    db = {
        'books': books,
        'ratings': ratings
    }
    return db


# II. GET INPUT
def input_positive_int(request_msg: str) -> str:
    """Defensive programming approach, using isdigit method."""
    # ask for input unitl valid
    while True:
        n = input(request_msg)
        if not n.isdigit():
            print("\nPlease input a postitive number.\n")
            continue
        return int(n)


# III. ADD USER
def get_ratings_l(books: list, ratings_percentage=0.2) -> list:
    """Get n ratings from the user - return list of STR."""

    print("\nRATE BOOKS \nScale (worst to best): -5, -3, 0, 1, 3, 5\n")
    # initialize
    books_len = len(books)
    ratings_n = int(books_len * ratings_percentage)
    ratings_l = ['0'] * books_len

    # ask for ratings_n ratings and save it in the list
    for i in range(ratings_n):
        book_i = randrange(books_len)
        # generate new book index until unrated
        while ratings_l[book_i] != '0':
            book_i = randrange(books_len)
        book = books[book_i]
        # ask for input unitl it is in the scale
        while True:
            rating = input(book[1] + ' by ' + book[0] + ": ")
            if rating in ['-5', '-3', '0', '1', '3', '5']:
                break
            else:
                print("\nPlease use only the scale given above.\n")
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
def calculate_similarity(username: str, db) -> list:
    """Return list of similarity of the user with every other user in db."""
    similarity_l = []
    ratings = db['ratings'][username]  # user we are calculating  similarity for
    # loop over each user in the dict of users
    for cur_username, cur_ratings in db['ratings'].items():
        if cur_username == username:
            continue
        similarity = 0
        # loop over each book in dict of ratings
        for cur_book, cur_book_rating in cur_ratings.items():
            # if the current user also has red the book, calculate the similarity
            if cur_book in ratings:
                similarity += cur_book_rating * ratings[cur_book]
        # finally append the tuple (user, similarity) to the list
        similarity_l.append((cur_username, similarity))
    similarity_l.sort(key=lambda x: x[1], reverse=True)
    return similarity_l


# V.   GET RECCOMENDATIONS
def get_rcm(username: str, similarity_l: list, db: dict, rcm_n=10) -> dict:
    """
    Crete the dict of books recommended by various users,
    based on the similarity list.
     """
    rcm = {}
    cur_rcm_n = 0
    for cur_user in similarity_l:
        cur_user_rcm_books_l = []
        for cur_book, cur_rating in db['ratings'][cur_user[0]].items():
            # if the user we are recommending to has alread red the book
            if (cur_book in db['ratings'][username]):
                continue
            # if the book is already recommended, continue
            already_rcm = False
            for already_rcm_books_l in rcm.values():
                if cur_book in already_rcm_books_l:
                    already_rcm = True
                    break
            if already_rcm:
                continue
            # if the book is well rated, add to the list of recommended by the current user
            if (cur_rating == 3) or (cur_rating == 5):
                cur_user_rcm_books_l.append(cur_book)
                # increase the number of recommended books
                cur_rcm_n += 1
                # return dict if we have enough
                if rcm_n <= cur_rcm_n:
                    rcm[cur_user[0]] = cur_user_rcm_books_l
                    return rcm
        # if there are any books recommended by the current user
        if not len(cur_user_rcm_books_l) == 0:
            rcm[cur_user[0]] = cur_user_rcm_books_l
    return rcm


# VI.  GENERATE OUTPUT
def generate_similarity_msg(similarity_l: list) -> str:
    msg = "\nSIMILARITIES:\n\n"
    for user in similarity_l:
        msg += '  ' + user[0] + ' : ' + str(user[1]) + '\n'
    return msg


def generate_rcm_msg(rcm: dict) -> str:
    msg = "\n\nRECOMMENDATIONS:\n\n"
    for user, rcms in rcm.items():
        msg += 'By ' + user + ':\n\n'
        for book in rcms:
            msg += '  ' + book[1] + ' by ' + book[0] + '\n' 
        msg += '\n'
    return msg


def generate_output_file(content: list, output_filename="output.txt"):
    """Generate output file with containing all strings in msgs list divaded by newline."""
    with open(output_filename, 'w') as f:
        print(''.join(content), file=f)


# MAIN FUNCTION
def recommendations():
    """
    Return recommendations calculated using similartiy algorithms.
    Return False if Error ocured.
    """
    # I. READ FILES
    db = read_files()
    if not db:
        print("\nCannot read the data from files, quit\n")
        return False

    # II. GET INPUT
    username_request_msg = "Username: "
    rcm_n_request_msg = "Reccomendation number: "
    username = input(username_request_msg)
    rcm_n = input_positive_int(rcm_n_request_msg)

    # III. ADD USER
    if username not in db['ratings']:
        add_user(username, db)

    # IV. CALCULATE SIMILARITY
    similarity_l = calculate_similarity(username, db)

    # V. GET RECOMMENDATIONS
    rcm = get_rcm(username, similarity_l, db, rcm_n)

    # VI. GENERATE OUTPUT
    similarity_msg = generate_similarity_msg(similarity_l)
    rcm_msg = generate_rcm_msg(rcm)
    print(similarity_msg)
    print(rcm_msg)

    output_content = [
        username_request_msg,
        username + '\n',
        rcm_n_request_msg,
        str(rcm_n) + '\n',
        similarity_msg,
        rcm_msg
    ]

    generate_output_file(output_content)


if __name__ == "__main__":
    recommendations()
