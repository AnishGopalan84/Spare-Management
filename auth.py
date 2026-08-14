import bcrypt
from database import get_session
from models import User
from sqlalchemy import func

def create_user(username,password,role,fullname):

    session=get_session()

    hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

    user=User(
        username=username,
        password=hashed,
        role=role,
        fullname=fullname
    )

    session.add(user)
    session.commit()

def login(username,password):

    session=get_session()

    #user=session.query(User).filter_by(username=username).first()
    user = session.query(User).filter(
    func.lower(User.username) == username.lower()
                    ).first()

    if user is None:
        return None

    if bcrypt.checkpw(password.encode(),user.password.encode()):
        return user

    return None