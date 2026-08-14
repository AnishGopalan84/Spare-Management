from database import get_session
from models import Category, Brand, Model, Unit

session = get_session()

# -------------------------
# Categories
# -------------------------
categories = [
    "Printer",
    "Copier",
    "Scanner",
    "Toner",
    "Drum",
    "Developer",
    "Maintenance Kit"
]

for item in categories:
    if not session.query(Category).filter_by(name=item).first():
        session.add(Category(name=item))


# -------------------------
# Brands
# -------------------------
brands = [
    "Toshiba",
    "Epson",
    "Konica Minolta",
    "HP",
    "Canon",
    "Xerox"
]

for item in brands:
    if not session.query(Brand).filter_by(name=item).first():
        session.add(Brand(name=item))

session.commit()


# -------------------------
# Models
# -------------------------
brand_map = {
    "Toshiba": [
        "e-STUDIO 2525AC",
        "e-STUDIO 3525AC",
        "e-STUDIO 4528A",
        "e-STUDIO 6525AC"
    ],
    "Epson": [
        "M4000",
        "C800"
    ],
    "HP": [
        "LaserJet M428",
        "LaserJet M404"
    ],
    "Canon": [
        "IR 2925",
        "IR C3226"
    ]
}

for brand_name, model_list in brand_map.items():

    brand = session.query(Brand).filter_by(name=brand_name).first()

    if brand:

        for model_name in model_list:

            if not session.query(Model).filter_by(
                name=model_name,
                brand_id=brand.id
            ).first():

                session.add(
                    Model(
                        name=model_name,
                        brand_id=brand.id
                    )
                )


# -------------------------
# Units
# -------------------------
units = [
    "PCS",
    "SET",
    "BOX",
    "NOS",
    "ROLL"
]

for item in units:

    if not session.query(Unit).filter_by(name=item).first():

        session.add(Unit(name=item))

session.commit()

print("Master data inserted successfully.")