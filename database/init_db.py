from database.db import Base
from database.db import engine

import database.models


def create_database():
    Base.metadata.create_all(bind=engine)
