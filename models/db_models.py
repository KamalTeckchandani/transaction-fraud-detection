import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(String, primary_key=True)
    user_id = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime)
    ip_address = Column(String)
    location = Column(String)
    lat = Column(Float)  # <-- latitude
    lon = Column(Float)  # <-- longitude
    device_id = Column(String)

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String)
    risk_score = Column(Integer)
    reasons = Column(Text)
    explanation = Column(Text)

def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'fraud_detector.db')
    db_path = os.path.abspath(db_path)
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    engine = init_db()
    session = get_session(engine)
    print("Database initialized and session created.")
