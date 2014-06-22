#-------------------------------------------------------------------------------
# Name:        stocksDatabaseManager.py
# Purpose:
#
# Author:      avsolatorio
#
# Created:     22/06/2014
# Copyright:   (c) avsolatorio 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import sqlalchemy

Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)

def isDataInDatabase(model, session, **kwargs):
    result = False
    if session.query(model).filter_by(**kwargs).count():
        result = True

    return result

class TransactionTime(Base):
    __tablename__ = "transaction_time"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    day = sqlalchemy.Column(sqlalchemy.Integer)
    month = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    hour = sqlalchemy.Column(sqlalchemy.Integer)
    minute = sqlalchemy.Column(sqlalchemy.Integer)
    second = sqlalchemy.Column(sqlalchemy.Integer)
    day_of_week = sqlalchemy.Column(sqlalchemy.String)
    __table_args__ = (sqlalchemy.UniqueConstraint('day', 'month', 'year', 'hour', 'minute', 'second', 'day_of_week', name='transaction_time_constraint'),)

    def __repr__(self):
        return "<TransactionTime(day=%d, month=%d, year=%d, hour=%d, minute=%d, second=%d, day_of_week=%s)>" % (self.day, self.month, self.year, self.hour, self.minute, self.second, self.day_of_week)

class Stock(Base):
    __tablename__ = "stock"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    stock_symbol = sqlalchemy.Column(sqlalchemy.String)
    stock_name = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return "<Stock(stock_symbol=%s, stock_name=%s)>" % (self.stock_symbol. self.stock_name)

class Broker(Base):
    __tablename__ = "broker"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    broker_code = sqlalchemy.Column(sqlalchemy.String)
    broker_name = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return "<Broker(broker_code=%s, broker_name=%s)>" % (self.broker_code, self.broker_name)


class Transaction(Base):
    __tablename__ = "transaction"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    buyer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('broker.id'))
    buyer = relationship("Broker", foreign_keys=[buyer_id], backref=backref('transaction_for_buyer', order_by=id))

    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('broker.id'))
    seller = relationship("Broker", foreign_keys=[seller_id], backref=backref('transaction_for_seller', order_by=id))

    stock_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('stock.id'))
    stock = relationship("Stock", foreign_keys=[stock_id], backref=backref('transaction', order_by=id))

    transaction_time_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('transaction_time.id'))
    transaction_time = relationship("TransactionTime", foreign_keys=[transaction_time_id], backref=backref('transaction', order_by=id))

    volume = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Float)



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def main():
    pass

if __name__ == '__main__':
    main()
