from flask import Flask
from flask_restful import Api, Resource, reqparse
from requests import get

from database import db, new_id
from models import Post
from validators import valid_title, valid_body, id_exists, userId_exists, external_URL

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


class Index(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


class SinglePost(Resource):
    def get(self, post_id):
        if id_exists(post_id):
            return Post.query.filter_by(id=post_id).first().__repr__()

        response = get(external_URL + "/posts/" + str(post_id))
        if response.status_code != 200:
            return {}, 404

        return save_post(response.json())

    def delete(self, post_id):
        if not id_exists(post_id):
            return {}, 404

        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        return {}, 200

    def patch(self, post_id):
        if not id_exists(post_id):
            return {}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('title', required=False, location='json')
        parser.add_argument('body', required=False, location='json')

        post = Post.query.filter_by(id=post_id).first()
        data = parser.parse_args(strict=True)

        if data['title'] is not None:
            if not valid_title(data['title']):
                return {}, 400
            post.title = data['title']

        if data['body'] is not None:
            if not valid_body(data['body']):
                return {}, 400
            post.body = data['body']

        db.session.commit()
        return post.__repr__(), 200


class PostList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=False, type=int, location='args')
        parser.add_argument('userId', required=False, type=int, location='args')

        data = parser.parse_args()
        if data['userId'] is not None:
            if data['id'] is not None:
                posts = Post.query.filter_by(userId=data['userId']).filter_by(id=data['id']).all()
            else:
                posts = Post.query.filter_by(userId=data['userId']).all()
        else:
            if data['id'] is not None:
                posts = Post.query.filter_by(id=data['id']).all()
            else:
                posts = Post.query.all()

        output = []
        for post in posts:
            output.append(post.__repr__())

        return output, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int, location='json')
        parser.add_argument('userId', required=True, type=int, location='json')
        parser.add_argument('title', required=True, location='json')
        parser.add_argument('body', required=True, location='json')

        data = parser.parse_args(strict=True)
        if id_exists(data['id']):
            data['id'] = new_id()

        if not userId_exists(data['userId']):
            return {}, 400

        return save_post(data), 201


api.add_resource(Index, '/')
api.add_resource(SinglePost, '/posts/<int:post_id>')
api.add_resource(PostList, '/posts')


def save_post(post):
    new_post = Post(post['id'], post['userId'], post['title'], post['body'])
    db.session.add(new_post)
    db.session.commit()

    return new_post.__repr__()


if __name__ == '__main__':
    app.run()
