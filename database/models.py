from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from database.db import Base


# ==========================
# Người chơi
# ==========================

class Player(Base):

    __tablename__ = "players"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), unique=True, nullable=False)

    active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================
# Mùa giải
# ==========================

class Season(Base):

    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)

    current = Column(Boolean, default=False)


# ==========================
# Trận đấu
# ==========================

class Match(Base):

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)

    season_id = Column(
        Integer,
        ForeignKey("seasons.id")
    )

    player1_id = Column(
        Integer,
        ForeignKey("players.id")
    )

    player2_id = Column(
        Integer,
        ForeignKey("players.id")
    )

    round = Column(String(30))

    youtube_id = Column(String(30))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    season = relationship("Season")

    player1 = relationship(
        "Player",
        foreign_keys=[player1_id]
    )

    player2 = relationship(
        "Player",
        foreign_keys=[player2_id]
    )
