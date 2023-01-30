from flask_restx import Namespace, Resource

from project.container import movie_service
from project.setup.api.models import movie
from project.setup.api.parsers import movie_parser

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.expect(movie_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        return movie_service.get_all(**movie_parser.parse_args())


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        return movie_service.get_one(movie_id)
