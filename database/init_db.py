from database.db import engine
from database.db import Base

import database.models

def create_database():

    Base.metadata.create_all(bind=engine)

    print("✅ Database đã sẵn sàng.")
