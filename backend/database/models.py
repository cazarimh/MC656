from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from .config import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, unique=True, index=True)
    user_name = Column(String, index=True)
    user_hashed_password = Column(String, index=True)

    user_transactions = relationship('Transaction', back_populates='user', cascade='all, delete-orphan')

class Transaction(Base):
    __tablename__ = 'transactions'

    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    transaction_id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(Date, index=True)
    transaction_value = Column(Float, index=True)
    transaction_type = Column(String, index=True)
    transaction_category = Column(String, index=True)
    transaction_description = Column(String, nullable=True, index=True)

    user = relationship('User', back_populates='user_transactions')