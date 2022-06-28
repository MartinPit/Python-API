from models import Post
from database import db
from requests import get


def valid_id(id):
    if not str(id).isdigit():
        return False

    return True


def id_exists(id):
    if db.session.query(Post.id).filter_by(id=id).first() is None:
        return False
    return True


def valid_userId(userId, external_url):
    if not str(userId).isdigit():
        return False

    response = get(external_url + "/users/" + str(userId))
    if response.json() == {}:
        return False

    return True


def valid_title(title):
    if len(title) > 40:
        return False
    return True


def valid_body(body):
    if len(body) > 200:
        return False
    return True
