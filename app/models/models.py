from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.database.db import Base

# Пользователи
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


# Подгруппы объектов
class Subgroup(Base):
    __tablename__ = "subgroups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    sites = relationship("Site", back_populates="subgroup")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="subgroups")


# Строительные объекты
class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, nullable=True)
    is_archived = Column(Boolean, default=False)
    subgroup_id = Column(Integer, ForeignKey("subgroups.id"), nullable=True)

    subgroup = relationship("Subgroup", back_populates="sites")
    expenses = relationship("Expense", back_populates="site")
    salaries = relationship("Salary", back_populates="site")
    workers = relationship("Worker", back_populates="site")
    tools = relationship("Tool", back_populates="site")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="sites")

    from_transfers = relationship(
        "ToolTransfer",
        back_populates="from_site",
        foreign_keys="ToolTransfer.from_site_id"
    )
    to_transfers = relationship(
        "ToolTransfer",
        back_populates="to_site",
        foreign_keys="ToolTransfer.to_site_id"
    )


# Сотрудники
class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"))

    site = relationship("Site", back_populates="workers")
    salaries = relationship("Salary", back_populates="worker")
    expenses = relationship("Expense", back_populates="worker")
    is_archived = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="workers")


# Инструменты
class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, nullable=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    is_archived = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="tools")
    site = relationship("Site", back_populates="tools")
    transfers = relationship("ToolTransfer", back_populates="tool")


# Расходы
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String, index=True)  # 'purchase' или 'salary'
    comment = Column(String, nullable=True)
    date = Column(Date, default=func.current_date())
    site_id = Column(Integer, ForeignKey("sites.id"))
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="expenses")

    site = relationship("Site", back_populates="expenses")
    worker = relationship("Worker", back_populates="expenses")


# Зарплата
class Salary(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    date = Column(Date, default=func.current_date())
    comment = Column(String, nullable=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    site_id = Column(Integer, ForeignKey("sites.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="salaries")

    worker = relationship("Worker", back_populates="salaries")
    site = relationship("Site", back_populates="salaries")


# Перемещения инструментов
class ToolTransfer(Base):
    __tablename__ = "tool_transfers"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    from_site_id = Column(Integer, ForeignKey("sites.id"))
    to_site_id = Column(Integer, ForeignKey("sites.id"))
    comment = Column(String, nullable=True)
    date_value = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="tool_transfers")
    tool = relationship("Tool", back_populates="transfers")
    from_site = relationship(
        "Site", back_populates="from_transfers", foreign_keys=[from_site_id]
    )
    to_site = relationship(
        "Site", back_populates="to_transfers", foreign_keys=[to_site_id]
    )


# Материалы
class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unit = Column(String, nullable=True)
    is_archived = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="materials")
