from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Park(Base):
	__tablename__ = 'parks'
	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	latitude = Column(Float)
	longitude = Column(Float)
	station_id = Column(Integer, ForeignKey('stations.id'))
	park_station = relationship("Station", back_populates="parks")

class Station(Base):
	__tablename__ = 'stations'
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
	station_id = Column(Integer, ForeignKey('stations.id'))
	weather_station = relationship("Station", back_populates="weathers")

database_path = "national_parks_weather.sqlite"
engine = create_engine(f"sqlite:///{database_path}", echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)
session = Session(bind=engine)

# Add our stuff, starting with stations, then parks, and finally the weather
import json

# ============== #
#    STATIONS    #
# ============== #

with open('./Results/stations.json', 'r') as f:
	station_data = json.load(f)

stations = []
for wban, loc in station_data.items():
    station = Station(wban = wban, latitude = loc['lat'], longitude = loc['lng'])
    stations.append(station)

session.add_all(stations)

# ============== #
#     PARKS      #
# ============== #

with open('./Results/parks.json', 'r') as f:
	park_data = json.load(f)

parks = []
for i, p in park_data.items():
	park = Park(name=p['name'], latitude=p['latitude'], longitude=p['longitude'])
	park.park_station = session.query(Station).filter_by(wban=p['wban']).first()
	parks.append(park)

session.add_all(parks)

# ============== #
#    WEATHER     #
# ============== #

with open('./Results/weather.json', 'r') as f:
	weather_data = json.load(f)

weather_results = []
for i, w in weather_data.items():
    weather = Weather(month = w['month'], avg_temp = w['avg_temp'], \
        avg_visability = w['avg_visability'], avg_wind_speed = w['avg_wind_speed'], \
        avg_precipitation = w['avg_precipitation'], avg_snow_depth = w['avg_snow_depth'])
    weather.weather_station = session.query(Station).filter_by(wban=w['wban']).first()
    weather_results.append(weather)

session.add_all(weather_results)

session.commit()