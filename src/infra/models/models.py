from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.infra.models.base import BaseSQLModel


Base = declarative_base()

organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)


class Organization(BaseSQLModel):
    __tablename__ = 'organizations'  # noqa
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    building = relationship('Building', back_populates='organizations')
    activities = relationship('Activity', secondary=organization_activity, back_populates='organizations')
    phones = relationship('Phone', back_populates='organization', cascade='all, delete-orphan')


class Phone(BaseSQLModel):
    __tablename__ = 'phones'  # noqa
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    organization = relationship('Organization', back_populates='phones')


class Building(BaseSQLModel):
    __tablename__ = 'buildings'  # noqa
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    organizations = relationship('Organization', back_populates='building')


class Activity(BaseSQLModel):
    __tablename__ = 'activities'   # noqa
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('activities.id'))
    children = relationship('Activity', backref='parent', remote_side=[id])
    organizations = relationship('Organization', secondary=organization_activity, back_populates='activities')
