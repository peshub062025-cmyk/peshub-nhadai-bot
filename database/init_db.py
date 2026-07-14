from database.db import engine
from database.db import Base

import database.models


def create_database():

    if engine is None:
        print("⚠ Database chưa được cấu hình.")
        return

    Base.metadata.create_all(bind=engine)

    print("✅ Database sẵn sàng.")
