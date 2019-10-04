from api import App

server_app = App()
app = getattr(server_app, "flask")

# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return "hi"