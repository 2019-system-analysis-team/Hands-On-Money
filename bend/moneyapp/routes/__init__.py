from flask import Blueprint
routes = Blueprint('routes', __name__)

from .home import *
from .user import *
from .organization import *
from .task import *
from .review import *
from .feedback import *
from .balance import *