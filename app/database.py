from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def new_id():
    from models import Post
    return db.session.query(db.func.max(Post.id)).scalar() + 1


def init_db():
    # if input('Are you sure you want to delete all data? (y/n)\n').lower() == 'y':
    db.drop_all()
    db.create_all()
    db.session.commit()
