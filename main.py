from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABESE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    __tablename__ = 'video_model'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video (name = {self.name}, views {self.views}, likes{self.likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str,
    help="Name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int,
    help="Number of views is required", required=True)
video_put_args.add_argument(
    "likes", type=int,
    help="Number of likes is requires", required=True)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id already taken")
        video = VideoModel(
            id=video_id, name=args["name"], likes=args["likes"], views=args["views"])
        db.session.add(video)
        db.session.commit()
        return video, 201

    def delete(self, video_id):

        return '', 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
