from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from src.infra.models.base import BaseSQLModel


organization_activity = Table(
    "organization_activity",
    BaseSQLModel.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)


class Organization(BaseSQLModel):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship('Building', back_populates='organizations')
    activities = relationship('Activity', secondary=organization_activity, back_populates='organizations', lazy='selectin')
    phones = relationship('Phone', back_populates='organization', cascade='all, delete-orphan')


class Phone(BaseSQLModel):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='phones')


class Building(BaseSQLModel):
    __tablename__ = 'buildings'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    organizations = relationship('Organization', back_populates='building')


class Activity(BaseSQLModel):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id', ondelete="SET NULL"), nullable=True)
    children = relationship('Activity', backref='parent', remote_side=[id])
    organizations = relationship('Organization', secondary=organization_activity, back_populates='activities', lazy='selectin')
