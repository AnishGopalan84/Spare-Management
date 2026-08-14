from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///database/spare.db")

Session = sessionmaker(bind=engine)

def get_session():
    return Session()