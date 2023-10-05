from sqlalchemy import Boolean, Column, Integer, String

from .database import Base


# Define the URL model class
class URL(Base):
    __tablename__ = "urls"

    # Define table columns
    id = Column(Integer, primary_key=True)
    key = Column(String(50), unique=True, index=True)
    secret_key = Column(String(50), unique=True, index=True)
    target_url = Column(String(500), index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
