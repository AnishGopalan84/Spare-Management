from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, Float,Date, Text
from datetime import date
from database import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String(255))
    role = Column(String(30))
    fullname = Column(String(100))
    active = Column(Integer, default=1)

class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    customer_code = Column(
        String(50),
        unique=True,
        nullable=False
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    company_name = Column(
        String(100)
    )

    contact_person = Column(
        String(100)
    )

    mobile = Column(
        String(30)
    )

    email = Column(
        String(100)
    )

    address = Column(
        String(200)
    )

    city = Column(
        String(50)
    )

    country = Column(
        String(50)
    )

    vat_number = Column(
        String(50)
    )

    remarks = Column(
        String(200)
    )






class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)



class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    models = relationship("Model", back_populates="brand")
                          

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String(100), nullable=False)
    brand = relationship("Brand", back_populates="models")



class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True, nullable=False)



class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True)

    part_number = Column(String(50), unique=True, nullable=False)

    part_name = Column(String(100), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    brand_id = Column(Integer, ForeignKey("brands.id"))

    model_id = Column(Integer, ForeignKey("models.id"))

    unit_id = Column(Integer, ForeignKey("units.id"))

    purchase_price = Column(Float, default=0)

    selling_price = Column(Float, default=0)

    stock_qty = Column(Integer, default=0)

    minimum_stock = Column(Integer, default=0)

    location = Column(String(50))

    remarks = Column(String(200))
    category = relationship("Category")

    brand = relationship("Brand")

    model = relationship("Model")

    unit = relationship("Unit")

class Supplier(Base):
        __tablename__ = "suppliers"

        id = Column(Integer, primary_key=True)
        supplier_code = Column(String(20), unique=True)
        supplier_name = Column(String(100), nullable=False)
        company_name = Column(String(100))
        contact_person = Column(String(100))
        mobile = Column(String(30))
        email = Column(String(100))
        address = Column(String(512))
        city = Column(String(100))
        country = Column(String(100))
        vat_number = Column(String(50))
        payment_terms = Column(String(100))
        remarks = Column(String(512))

class Purchase(Base):
        __tablename__ = "purchases"

        id = Column(Integer, primary_key=True)

        purchase_no = Column(String(20), unique=True)

        purchase_date = Column(Date)

        supplier_id = Column(
            Integer,
            ForeignKey("suppliers.id")
        )

        remarks = Column(String(255))

        grand_total = Column(Float, default=0)

        created_by = Column(String(100))

        supplier = relationship("Supplier")

        items = relationship(
            "PurchaseItem",
            back_populates="purchase",
            cascade="all, delete-orphan"
        )

class PurchaseItem(Base):
        __tablename__ = "purchase_items"

        id = Column(Integer, primary_key=True)

        purchase_id = Column(
            Integer,
            ForeignKey("purchases.id")
        )

        spare_id = Column(
            Integer,
            ForeignKey("spare_parts.id")
        )

        quantity = Column(Integer)

        purchase_price = Column(Float)

        total = Column(Float)

        purchase = relationship(
            "Purchase",
            back_populates="items"
        )

        spare = relationship("SparePart")

class MaterialIssue(Base):
    __tablename__ = "material_issues"

    id = Column(Integer, primary_key=True)

    issue_no = Column(String(20), unique=True)

    issue_date = Column(Date)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    remarks = Column(String(512))

    grand_total = Column(Float, default=0)

    created_by = Column(String(100))

    status = Column(
    String(20),
    default="COMPLETED",
    nullable=False
    )

    invoiced = Column(
        Boolean,
        default=False,
        nullable=False
    )

    customer = relationship("Customer")

    items = relationship(
        "MaterialIssueItem",
        back_populates="issue",
        cascade="all, delete-orphan"
    )

class MaterialIssueItem(Base):
    __tablename__ = "material_issue_items"

    id = Column(Integer, primary_key=True)

    issue_id = Column(
        Integer,
        ForeignKey("material_issues.id")
    )

    spare_id = Column(
        Integer,
        ForeignKey("spare_parts.id")
    )

    quantity = Column(Integer)

    issue_price = Column(Float)

    total = Column(Float)

    issue = relationship(
        "MaterialIssue",
        back_populates="items"
    )

    spare = relationship("SparePart")


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)

    invoice_no = Column(
        String(50),
        unique=True,
        nullable=False
    )

    invoice_date = Column(
        Date,
        nullable=False
    )

    invoice_type = Column(
        String(30),
        nullable=False
    )
    # DIRECT
    # MATERIAL_ISSUE

    status = Column(
        String(20),
        default="COMPLETED",
        nullable=False
    )
    # COMPLETED
    # CANCELLED

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )

    # For Cash / Walk-in customer details
    customer_name = Column(
        String(200),
        nullable=True
    )

    company_name = Column(
        String(200),
        nullable=True
    )

    phone = Column(
        String(50),
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    po_number = Column(
        String(100),
        nullable=True
    )

    po_date = Column(
        Date,
        nullable=True
    )

    remarks = Column(
        Text,
        nullable=True
    )

    material_issue_id = Column(
        Integer,
        ForeignKey("material_issues.id"),
        nullable=True
    )

    grand_total = Column(
        Numeric(12, 3),
        nullable=False,
        default=0
    )

    created_by = Column(
        String(100),
        nullable=False
    )
class InvoiceItem(Base):

    __tablename__ = "invoice_items"

    id = Column(
        Integer,
        primary_key=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    item_type = Column(
        String(20),
        nullable=False
    )
    # SPARE
    # SERVICE

    spare_id = Column(
        Integer,
        ForeignKey("spare_parts.id"),
        nullable=True
    )

    description = Column(
        String(255),
        nullable=False
    )

    quantity = Column(
        Numeric(12, 3),
        nullable=False
    )

    unit_price = Column(
        Numeric(12, 3),
        nullable=False
    )

    total = Column(
        Numeric(12, 3),
        nullable=False
    )

class DeliveryOrder(Base):

    __tablename__ = "delivery_orders"

    id = Column(
        Integer,
        primary_key=True
    )

    do_no = Column(
        String(50),
        unique=True,
        nullable=False
    )

    do_date = Column(
        Date,
        nullable=False
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )

    customer_name = Column(
        String(200),
        nullable=True
    )

    status = Column(
        String(20),
        default="COMPLETED",
        nullable=False
    )
    # COMPLETED
    # CANCELLED

    created_by = Column(
        String(100),
        nullable=False
    )
class DeliveryOrderItem(Base):

    __tablename__ = "delivery_order_items"

    id = Column(
        Integer,
        primary_key=True
    )

    do_id = Column(
        Integer,
        ForeignKey("delivery_orders.id"),
        nullable=False
    )

    spare_id = Column(
        Integer,
        ForeignKey("spare_parts.id"),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=False
    )

    quantity = Column(
        Numeric(12, 3),
        nullable=False
    )

