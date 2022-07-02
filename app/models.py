from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(40), nullable=False)
    body = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return {'id': self.id,
                'userId': self.userId,
                'title': self.title,
                'body': self.body}

    def __init__(self, post_id, userId, title, body):
        self.id = post_id
        self.userId = userId
        self.title = title
        self.body = body
