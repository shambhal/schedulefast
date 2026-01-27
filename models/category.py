# models.py - SQLAlchemy Database Models
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey,UniqueConstraint,Date,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import timedelta
import datetime
from enum import Enum
Base = declarative_base()
class Config(Base):
     __tablename__="config_configmodel"
     cname = Column(String(10), nullable=False) 
     cvalue = Column(String(50), nullable=False)
     id = Column(Integer, primary_key=True, index=True)
class Information(Base):
    __tablename__="information_information"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    seo_url = Column(String(250), nullable=False, unique=True, index=True)
    content = Column(Text, nullable=True)
    status = Column(Boolean, default=True)
    sort_order = Column(Integer, default=10)
class Banner(Base):
    __tablename__="banners_banner"
    
    id = Column(Integer, primary_key=True, index=True)
    #category_id = Column(Integer, ForeignKey("category_category.id", ondelete="CASCADE"))
    image = Column(String(255), nullable=True, default="")
    tag = Column(String(10), nullable=True)
    sort_order = Column(Integer, default=0)
    category_id= Column(Integer, default=0)
    #category = relationship("Category", back_populates="banners")

class Doctor(Base):
    __tablename__ = "doctor_doctor"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # Assuming a 1-to-1 relationship with a User table
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), nullable=True)
    sunday = Column(String(120), nullable=True) 
    monday = Column(String(120), nullable=True)
    tuesday = Column(String(120), nullable=True)  
    wednesday = Column(String(120), nullable=True) 
    thursday = Column(String(120), nullable=True) 
    image = Column(String(120), nullable=True) 
    friday = Column(String(120), nullable=True) 
    saturday = Column(String(120), nullable=True) 
    off = Column(String(120), nullable=True) 
    categories = relationship('Category' ,secondary="doctor_doctorcategory", back_populates="doctors")
    special_days=relationship("DoctorSpecial",back_populates="doctor")
    booked=relationship("Book",back_populates="doctors")
class DoctorCategory(Base):
    __tablename__ = "doctor_doctorcategory"
    __table_args__ = (
        UniqueConstraint("doctor_id", "category_id", name="unique_doctor_category"),
    )

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctor_doctor.id"),primary_key=True)
    category_id = Column(Integer, ForeignKey("category_category.id"),primary_key=True)
    is_primary = Column(Boolean, default=False)

    #doctor = relationship("Doctor")
    #category = relationship("Category")
class DoctorSpecial(Base):
     # sdate=models.DateField('Special Date')
    __tablename__ = "doctor_doctorspecial"

    id = Column(Integer, primary_key=True, index=True)
    sdate = Column(Date, nullable=False)
    hours = Column(Text, default="08:00-12:00", nullable=False)
    off = Column(Text, nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctor_doctor.id"), nullable=False)

    doctor = relationship("Doctor", back_populates="special_days")

    def __repr__(self):
        return f"<DoctorSpecial {self.sdate} {self.doctor.name}>"
class DoctorQ(Base):
    __tablename__ = "doctor_doctor"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)  # Assuming a 1-to-1 relationship with a User table
    first_name = Column(String(50))
    is_active=Column(Integer)
    last_name = Column(String(50))
    years_of_experience = Column(Integer)
    bio=Column(Text)
    email = Column(String(100), unique=True, index=True)
    phone = Column (String(20), nullable=True)
    gender = Column(String(5), nullable=True)   
    image=Column(String(100),nullable=True)
class Category(Base):
    """
    Category model with hierarchical structure support.
    Categories can have parent categories creating a tree structure.
    """
    __tablename__ = "category_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("category_category.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    doctors = relationship('Doctor',secondary="doctor_doctorcategory", back_populates="categories")
    # Relationships
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Return the full path of the category including parent categories."""
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(path))

    def get_descendants(self):
        """Get all descendant categories."""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def is_root(self):
        """Check if this is a root category (no parent)."""
        return self.parent_id is None

    def get_level(self):
        """Get the level of this category in the hierarchy."""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
'''    
class ServiceStatus(str, enum.Enum):
    UN = "UN"
    AV = "AV"
'''


# models/cart.py

class PMS(Base):
    __tablename__='payment_payment'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    title = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    

class Cart(Base):
    __tablename__ = 'cart_cart'

    id = Column(Integer, primary_key=True, index=True)
    dated = Column(Date, nullable=False)
    price = Column(Numeric(6, 2), nullable=False)
    slot = Column(String(20), nullable=False)
    device_id = Column(String(50), nullable=True)
    user_id = Column(Integer, nullable=True, default=0)
    category_id=Column(Integer,nullable=True,default=0)
    category_name=Column(String,nullable=True,default='')
    doctor_name=Column(String,nullable=True, default='')
    doctor_id = Column(Integer, ForeignKey("doctor_doctor.id"), nullable=False)

    #doctor = relationship("Doctor" back_populates="cart")  # Assuming Doctor model is defined elsewhere
class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String, nullable=False)
    first_name=Column(String,nullable=False)
    is_staff=0
    date_joined=Column(DateTime,default=datetime.datetime.now())
    last_name=Column(String,nullable=True)

    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # one-to-one with Customer
    customer = relationship("Customer", back_populates="user", uselist=False)    
class Customer(Base):
    __tablename__='customer_customer'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), unique=True)  # OneToOne
    phone = Column(String, unique=True, nullable=False)

    user = relationship("User",  back_populates="customer")
    # Order Status Enum
class OrderStatus(Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class Order(Base):
    __tablename__ = "orders_order"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    device_id = Column(String(120), nullable=True)
    payment_method = Column(String(20), nullable=False)
    user_agent = Column(String(300), nullable=True)
    total = Column(Numeric(7, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    comment = Column(String(200), nullable=True)
    currency_code = Column(String(4), nullable=True)
    user_id = Column(Integer, nullable=True)  # Replace with ForeignKey if User model exists
    status = Column(String, default=OrderStatus.PENDING, nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    history = relationship("OrderHistory", back_populates="order", cascade="all, delete-orphan")
    totals = relationship("OrderTotal", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "orders_orderitems"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    name = Column(String(50), nullable=False)
    dated = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("category_category.id"), nullable=False)
    category= Column(String(50),nullable=True)  # snapshot at the time of order
    doctor_id = Column(Integer, ForeignKey("doctor_doctor.id"), nullable=False)
    doctor = Column(String(50),nullable=True)  # snapshot at the time of order
    slot = Column(String(50), nullable=False)
    price = Column(Numeric(7, 2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders_order.id"), nullable=True)

    order = relationship("Order", back_populates="items")


class OrderHistory(Base):
    __tablename__ = "orders_orderhistory"

    id = Column(Integer, primary_key=True, index=True)
    dated = Column(DateTime, default=datetime.datetime.now)
    status = Column(String(20), nullable=False)
    order_id = Column(Integer, ForeignKey("orders_order.id"), nullable=False)

    order = relationship("Order", back_populates="history")


class OrderTotal(Base):
    __tablename__ = "order_totals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    total = Column(Numeric(7, 2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders_order.id"), nullable=False)

    order = relationship("Order", back_populates="totals")
class EmailOTP(Base):
    __tablename__ = "email_otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp_code = Column(String)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))
    is_used = Column(Boolean, default=False)
class Book(Base):
    __tablename__ = "doctor_book"

    id = Column(Integer, primary_key=True, index=True)
    dated = Column(Date, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_doctor.id"), nullable=False, default=1)
    slot = Column(String(20), nullable=False)
    desc = Column(Text, nullable=True)
    name = Column(String(60), nullable=False)
    phone = Column(String(15), nullable=True)
    order_id = Column(Integer, nullable=True, default=0)
    email = Column(String(150), nullable=True, default="demo@gmail.com")
    status = Column(String(15), nullable=False, default="AV")
    device_id = Column(String(150), nullable=True)
    user_id = Column(Integer, nullable=True, default=0)
    order_item_id = Column(Integer, nullable=True, default=0)
    extra_info = Column(Text, nullable=True, default="")
    history=relationship("BookHistory",back_populates="book")
    # Relationship (if Service model exists)
    doctors = relationship("Doctor", back_populates="booked")

    __table_args__ = (
        UniqueConstraint("dated", "doctor_id", "slot", "status", name="unique2_booking"),
    )

    def __str__(self):
        return f"{self.name}-{self.dated}-{self.slot}"    

class BookHistory(Base):
    __tablename__ = "doctor_bookhistory"

    id = Column(Integer, primary_key=True, index=True)
    dated = Column(Date, nullable=False, default=func.current_date())
    status = Column(String(20), nullable=False)
    book_id = Column(Integer, ForeignKey("doctor_book.id"), nullable=False)
    info = Column(Text, nullable=True)

    book = relationship("Book", back_populates="history")

    def __repr__(self):
        return f"<BookHistory(book_id={self.book_id}, dated='{self.dated}', status='{self.status}')>"    