from flask import Flask
import os

template_dir = os.path.abspath('client')
app = Flask(__name__, template_folder=template_dir)

from api import routes