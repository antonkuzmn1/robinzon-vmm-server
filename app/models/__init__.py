from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.config import Config
from app.models.log import Log
from app.models.version import Version
from app.models.account import Account
from app.models.group import Group
from app.models.server import Server
from app.models.vm import VM
