from database import get_session
from models import Category, Brand, Model, Unit

session = get_session()

print(session.query(Category).count())
print(session.query(Brand).count())
print(session.query(Model).count())
print(session.query(Unit).count())