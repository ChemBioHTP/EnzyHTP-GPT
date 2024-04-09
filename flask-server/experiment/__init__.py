from flask import Blueprint

experiment = Blueprint('experiment', __name__)

from . import views