from flask import Flask
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)
api = Api(app)

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

videos = {}


def abort_no_video_id(video_id):
    if video_id not in videos:
        abort(404, message="Video does not exist")


class Video(Resource):

    def get(self, video_id):
        abort_no_video_id(video_id)
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
