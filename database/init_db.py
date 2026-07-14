from database.db import Base, engine

# Import tất cả models để SQLAlchemy biết cần tạo bảng nào
from database.models import Player, Season, Match


def create_database():
    Base.metadata.create_all(bind=engine)
    print("✅ SQLite database đã sẵn sàng.")
