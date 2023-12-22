from flask import Flask
from server.api import api

app = Flask(__name__)

api(app)
app.debug = True
app.run(host='127.0.0.1', port='1654')
