from flask import Flask
import os

app = Flask(__name__, template_folder='templates')

from api import routeText, routeAudio