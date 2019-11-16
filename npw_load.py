from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

class Park(Base):
	__tablename__ = 'park'
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	latitude = Column(Float)
	longitude = Column(Float)
	station_id = Column(Integer, ForeignKey('station.id'))
	park_station = relationship("Station", back_populates="parks")

class Station(Base):
	__tablename__ = 'station'
	id = Column(Integer, primary_key=True)
	wban = Column(Integer)
	latitude = Column(Float)
	longitude = Column(Float)
	parks = relationship("Park", back_populates="park_station")
	weathers = relationship("Weather", back_populates="weather_station")
	
class Weather(Base):
	__tablename__ = 'weather'
	id = Column(Integer, primary_key=True)
	month = Column(Integer)
	avg_temp = Column(Float)
	avg_visability = Column(Float)
	avg_wind_speed = Column(Float)
	avg_precipitation = Column(Float)
	avg_snow_depth = Column(Float)
	station_id = Column(Float, ForeignKey('station.id'))
	weather_station = relationship("Station", back_populates="weathers")

database_path = "national_parks_weather.sqlite"
engine = create_engine(f"sqlite:///{database_path}", echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)
session = Session(bind=engine)

# Add our stuff, starting with stations, then parks, and finally the weather
import json

with open('./Results/stations.json', 'r') as f:
	station_data = json.load(f)

stations = []
for s in stations:
	station = Station(wban=s['wban'], latitude=s['lat'], longitude=s['lng'])
	stations.append(station)
session.add_all(stations)

with open('./Results/parks.json', 'r') as f:
	park_data = json.load(f)

parks = []
for p in parks:
	park = Station(name=p['name'], lat=p['latitude'], lng=p['longitude'])
	park.station = session.query()
	parks.append(park)
session.add_all(parks)


with open('./Results/weather.json', 'r') as f:
	weather = json.load(f)
