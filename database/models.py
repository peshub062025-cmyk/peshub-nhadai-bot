from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


# =========================
# Người chơi
# =========================
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)


# =========================
# Mùa giải
# =========================
class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)


# =========================
# Trận đấu
# =========================
class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    season_id = Column(Integer, ForeignKey("seasons.id"))
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"))

    round = Column(String(50), nullable=False)

    youtube_link = Column(String(500), nullable=False)

    season = relationship("Season")

    player1 = relationship(
        "Player",
        foreign_keys=[player1_id]
    )

    player2 = relationship(
        "Player",
        foreign_keys=[player2_id]
    )
