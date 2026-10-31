
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from .database import Base


# Student and staff accounts
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")


# Services and counters
class Counter(Base):
    __tablename__ = "counters"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), nullable=False)
    status = Column(String(20), default="active")


# Student queue tokens
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    counter_id = Column(Integer, ForeignKey("counters.id"))
    token_number = Column(String(20), nullable=False)
    status = Column(String(20), default="waiting")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Queue activity history
class QueueHistory(Base):
    __tablename__ = "queue_history"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey("tokens.id"))
    action = Column(String(30), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
