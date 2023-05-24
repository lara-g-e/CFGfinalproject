import requests
import mysql.connector
import nltk
import numpy
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import re

# create a custom error to be thrown when we fail to connect with the DB


class DbConnectionError(Exception):
    pass


# create a function to connect to the db, implement your own user/password/database details


def _connect_to_db(films):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Africa11",
        database="films",
    )
    return connection


# create a function to connect to the API to search for images and cast


def search_movies_database(film_title):

    url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/'{}'".format(film_title)

    querystring = {"exact":"false","titleType":"movie"}

    headers = {
   "X-RapidAPI-Key": "40a78ce9ebmshbd91df11ae06b8fp149f9bjsnb829ec155bc9",
   "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    code = response.json()
    try:
        (code['results'][0]['primaryImage']['caption']['plainText'])
    except TypeError:
        'No further info available'
    except IndexError:
        'No further info available'
    else:
       chunks = ne_chunk(pos_tag(word_tokenize((code['results'][0]['primaryImage']['caption']['plainText']))))

       human_names = []
       gender_list = []
       for chunk in chunks:
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
            human_names.append(' '.join(c[0] for c in chunk))

       for each in human_names:
        endpoint = "https://api.genderize.io?name={}".format(each)
        response = requests.get(endpoint)
        code_2 = response.json()
        gender = (code_2['gender'])
        gender_list.append(gender)

       if "female" and "male" in gender_list:
           print(code['results'][0]['primaryImage']['caption']['plainText'])
           print('Female and Male Main Actors')
       elif "male" not in gender_list and "female" in gender_list:
           print(code['results'][0]['primaryImage']['caption']['plainText'])
           print('Female Main Actors')
       else:
           print(code['results'][0]['primaryImage']['caption']['plainText'])



# create a function to use the SQL connection to search our database using the users input, return the results


def get_records_by_year_and_bech_rating(start_year, end_year, bechdel_rating):
    db_connection = None
    results = []
    try:
        db_name = 'films'
        db_connection = _connect_to_db(db_name)

        cursor = db_connection.cursor()

        query = """SELECT *
                FROM films.films
                WHERE
                films.year
                BETWEEN '{}' AND '{}'
                HAVING rating = '{}';""".format(start_year, end_year, bechdel_rating)
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            # print(row)
            title = row[1]
            # we will now weed out faulty results with special chars and jumbled order before appending to results
            if '&' not in title:
                if 'The' not in title:
                    results.append(title)
        cursor.close()

    except Exception:
        raise DbConnectionError("Database connection unavailable.")
    finally:
        if db_connection:
            db_connection.close()

    return results


# login and registration login


def login_to_website(username, password):
    db_connection = None

    try:
        db_name = 'films'
        db_connection = _connect_to_db(db_name)

        cursor = db_connection.cursor()

        account_query = """ SELECT * FROM users WHERE username = %s AND password = %s""".format(username, password)

        cursor.execute(account_query)
        search_results = cursor.fetchone()

        if search_results:
            # redirect to homepage
            return True
        else:
            return "Incorrect username or password combination"

    except Exception:
        raise DbConnectionError("Database connection unavailable.")
    finally:
        if db_connection:
            db_connection.close()
            return


def register_an_account(username, password):
    db_connection = None

    try:
        db_name = 'films'
        db_connection = _connect_to_db(db_name)

        cursor = db_connection.cursor()

        registration_query = """ SELECT * FROM users WHERE username = %s""".format(username)
        cursor.execute(registration_query)
        account_search = cursor.fetchone()
        if account_search:
            return "This account already exists"
        elif not re.match(r'[A-Za=z0-9]+', username):
            return "Username must only contain letters and numbers"
        elif not username or not password:
            return "Please fill out the registration form"
        else:
            cursor.execute("INSERT INTO users VALUE (NULL, %s, %s", (username, password))
            db_connection.commit()
            return "You have successfully created an account"

    except Exception:
        raise DbConnectionError("Database connection unavailable.")
    finally:
        if db_connection:
            db_connection.close()
            return


