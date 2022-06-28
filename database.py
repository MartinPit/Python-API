from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def new_id():
    from models import Post
    return db.session.query(db.func.max(Post.id)).scalar() + 1
