from flask import render_template, request, jsonify
from ..controllers.main import get_employee, get_usernames
from . import bp
import logging


@bp.route("/", methods=["GET"])
def index():
    logging.getLogger().info(
        "Hello world logging", extra={"props": {"extra_property": "extra_value"}}
    )
    return f"Welcome to python backend template."


@bp.route("/methods", methods=["GET", "POST"])
def route():
    if request.method == "POST":
        return jsonify({"Hello": "POST"})
    return jsonify({"Hello": "GET"})


@bp.route("/_health", methods=["GET"])
def health():
    return "OK"


@bp.route("/about", methods=["GET"])
def about():
    return render_template("test.html")


@bp.route("/employees/<int:id>")
def employee(id):
    return get_employee(id)


@bp.route("/usernames", methods=["GET"])
def username():
    return get_usernames()
