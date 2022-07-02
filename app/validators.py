from app import Post
from app import db
from requests import get

external_URL = "https://jsonplaceholder.typicode.com"


def id_exists(post_id):
    if db.session.query(Post.id).filter_by(id=post_id).first() is None:
        return False

    return True


def userId_exists(userId):
    response = get(external_URL + "/users/" + str(userId))
    if response.status_code != 200:
        return False

    return True


def valid_title(title):
    return valid_string(title, 40)


def valid_body(body):
    return valid_string(body, 200)


def valid_string(string, length):
    if string == "":
        return False

    if len(string) > length:
        return False

    return True
