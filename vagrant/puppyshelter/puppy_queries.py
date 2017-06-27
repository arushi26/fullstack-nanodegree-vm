from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy
import datetime

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBsession = sessionmaker(bind = engine)
session = DBsession()

# Query all of the puppies and return the results in ascending alphabetical order
puppies_ascending = session.query(Puppy).order_by(Puppy.name.asc()).all()

for puppy in puppies_ascending:
	print puppy.name
	print puppy.dateOfBirth
	print puppy.gender
	print puppy.weight
	print puppy.picture
	print puppy.shelter_id

# Query all of the puppies that are less than 6 months old organized by the youngest first
sixmonthold = datetime.date.today() - datetime.timedelta(days = (6* 365/12))

puppies_very_young = session.query(Puppy).filter(Puppy.dateOfBirth > sixmonthold).order_by(Puppy.dateOfBirth.desc()).all()

for puppy in puppies_very_young:
	print puppy.name
	print puppy.dateOfBirth
	print puppy.gender
	print puppy.weight
	print puppy.picture
	print puppy.shelter_id

# Query all puppies by ascending weight
puppies_ascending_weight = session.query(Puppy).order_by(Puppy.weight.asc()).all()

for puppy in puppies_ascending_weight:
	print puppy.name
	print puppy.dateOfBirth
	print puppy.gender
	print puppy.weight
	print puppy.picture
	print puppy.shelter_id

# Query all puppies grouped by the shelter in which they are staying
puppies_by_shelter = session.query(Puppy).order_by(Puppy.shelter_id, Puppy.name).all()

for puppy in puppies_by_shelter:
	print puppy.name
	print puppy.shelter_id
