from flask import Flask

app = Flask(__name__)

from co2app import routes
