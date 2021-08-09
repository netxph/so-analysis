from flask import Blueprint

api_bp = Blueprint('api_pb', __name__)

@api_bp.route("/test")
def test():
    return "hello world"