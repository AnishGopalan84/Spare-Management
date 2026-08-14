from database import get_session
from models import SparePart


session = get_session()

print("---- Spare Parts ----")

spares = session.query(SparePart).all()

for s in spares:
    print(
        s.id,
        s.part_number,
        s.part_name,
        s.category,
        s.brand,
        s.model,
        s.unit,
        s.stock_qty,
        s.selling_price
    )

session.close()