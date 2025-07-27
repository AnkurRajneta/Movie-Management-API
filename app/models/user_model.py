from sqlalchemy import INTEGER, String, BOOLEAN, Column, DateTime, func, null
from app.config.database import Base
from app.enums.table_enums import TableName



class UserModel(Base):
    __tablename__ = TableName.USER

    id = Column(INTEGER, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable= True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now(),nullable=True)

   