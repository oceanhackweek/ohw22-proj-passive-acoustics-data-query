# Author: Roman Battisti
# Project: Passive Acoustic Data Query
# Ocean Hack Week 2022
# GitHub: https://github.com/oceanhackweek/ohw22-proj-passive-acoustics-data-query


import warnings

import numpy as np
import pandas as pd

from dtime_handling import strToDatetime
import lat_long_checks
from utilities import compute_min_max, none_or_float

from acoustics_database_catalog import catalog, database_subsections, freshwater, marine, terrestrial
import acoustics_database_catalog


class WorldAcousticsFinder(object):
    """
    Returns available hydrophone metadata from web-based databases based on user criterias. Data which partially overlaps
    user criteria (for example, a hydrophone file which lies partially, but not entirely, within a given time frame will
    be returned.
    
    Parameters
    ----------
    min_time: formatted str or datetime object
        The minimum time hydrophone data should exist.
        Datetime format should follow _________ conventions.
    max_time: formatted str or datetime object
        The maximum time hydrophone data should exist.
        Datetime format should follow _________ conventions.
    time_period: timedelta object
        The difference between min_time and max_time.
        max_time will be replaced by min_time + time_period.
    day_first: Bool
        Whether day comes first in datetime string if
        strings are provided in min_time/max_time.
    year_first: str or datetime object
        Whether year comes first in datetime string if
        strings are provided in min_time/max_time. Will
        override day_first.
    min_lat: str, int, or float
        The minimum latitude for geographic bounding box.
    max_lat: str, int, or float
        The maximum latitude for geographic bounding box.
    min_long: str, int, or float
        The minimum longitude for geographic bounding box.
    max_long: str, int, or float
        The maximum longitude for geographic bounding box.
    latitude: str, int, or float
        The latitudinal centroid of the bounding box. Paired
        with radius, will replace min_lat and max_lat.
    longitude: str, int, or float
        The longitudinal centroid of the bounding box. Paired
        with radius, will replace min_long and max_long.
    radius: str, int, or float
        The radius from the latitude/longitude centroid. Creates
        the bounding box (not circle) for the search. If not provided,
        assumed to be 0.
    min_freq: str, int, or float
        The minimum sampling frequency of the hydrophone data.
    max_freq: str, int, or float
        The maximum frequency of the hydrophone data.
    min_depth: str, int, or float
        The minimum depth of the hydrophone data.
    max_depth: str, int, or float
        The maximum depth of the hydrophone data.
    region: str
        Whether user wants any, marine, terrestrial, or freshwater based acoustic sensors
    
    """
    def __init__(self, min_time=None, max_time=None, time_period=None, day_first=False, year_first=False, 
                 min_lat=None, max_lat=None, min_long=None, max_long=None, latitude=None, longitude=None, radius=0,
                 min_freq=None, max_freq=None, min_depth=None, max_depth=None, region="all"):
        
        # Time Range
        if type(min_time) == str:
            self.min_time = strToDatetime(min_time, day_first, year_first)
        else:
            self.min_time = min_time
        if type(max_time) == str:
            self.max_time = strToDatetime(max_time, day_first, year_first)
        else:
            self.max_time = max_time
        if time_period:
            self.max_time = min_time + time_period
        
        # GPS bounding box
        if latitude:
            self._compute_min_max_lat(latitude, radius)
        else:
            coords = lat_long_checks.min_max_coords([min_lat, max_lat], "lat")
            self.min_lat, self.max_lat = lat_long_checks.min_max_coords([min_lat, max_lat], "lat")
        if longitude:
            self._compute_min_max_long(longitude, radius)
        else:
            self.min_long, self.max_long = lat_long_checks.min_max_coords([min_long, max_long], "long")
        
        # Frequency range
        self.min_freq = none_or_float(min_freq)
        self.max_freq = none_or_float(max_freq)
        
        # Depth range
        self.min_depth = none_or_float(min_depth)
        self.max_depth = none_or_float(max_depth)
        
        # Subselect regions
        self.region = region.lower()
        if self.region not in database_subsections:
            self.region = "all"
            warnings.warn(f'{region} is not an available sensor placement, search results defaulted to "all"')
        
        self.query_params = self._build_query_dict()
        self.available_data = pd.DataFrame([], columns=acoustics_database_catalog.standardized_column_output)
        
    def _compute_min_max_lat(self, lat, radius):
        """Compute the min_lat and max_lat if user provides latitude."""
        lat = lat_long_checks.convertLatLong(lat, "lat")
        radius = none_or_float(radius)
        if radius < 1e-10:
            warnings.warn("You have specified a latitude but your radius as at or near zero. Your search will not likely return any hits.")
        self.min_lat, self.max_lat = compute_min_max(lat, radius)
    
    def _compute_min_max_long(self, long, radius):
        """Compute the min_long and max_long if user provides longitude."""
        long = lat_long_checks.convertLatLong(long, "long")
        radius = none_or_float(radius)
        if radius < 1e-10:
            warnings.warn("You have specified a longitude but your radius as at or near zero. Your search will not likely return any hits.")
        self.min_long, self.max_long = compute_min_max(long, radius)
    
    def _build_query_dict(self):
        """Create a dictionary of user provided paramters to filter data."""
        query_params = {}
        for attr, value in self.__dict__.items():
            if value:
                query_params[attr] = value
        return query_params
    
    def _fetchData(self, dbs=[]):
        """
        Iterate through the requested databases (specified by dbs) to find available acoustic data.
        :param dbs: (list) databases to include from the database catalog.
        """
        
        self.available_data = pd.DataFrame([], columns=acoustics_database_catalog.standardized_column_output)  # reset available data from last query
        generator = self._databaseGenerator(dbs)
        for db, data in generator:
            data["database"] = db
            self.available_data = pd.concat([self.available_data, data])
    
    def _databaseGenerator(self, dbs: list):
        """
        Iterates through the catalog of databases and yields output (dataframe?) for each.
    
        :param dbs: list of databases to query.

        :yields: pandas dataframe?
        """

        for db in dbs:
            if db in catalog:
                yield db, catalog[db](**self.query_params)
    
    def findAcousticSensors(self):
        self._fetchData(dbs=database_subsections[self.region])
        return self.available_data.reset_index(drop=True)
    
    def findFreshwaterAcoustics(self):
        self._fetchData(dbs=freshwater)
        return self.available_data.reset_index(drop=True)
    
    def findMarineAcoustics(self):
        self._fetchData(dbs=marine)
        return self.available_data.reset_index(drop=True)
    
    def findTerrestrialAcoustics(self):
        self._fetchData(dbs=terrestrial)
        return self.available_data.reset_index(drop=True)


if __name__ == "__main__":
    test = WorldAcousticsFinder(min_time="2020-05-06 12:00:00", latitude=10.6, region="terrestrial")
    print(test.query_params)
    test2 = WorldAcousticsFinder(min_time="2020-05-06 12:00:00", min_lat=10.6, max_lat=12.8)
    print(test2.findMarineAcoustics())
    print(test2.query_params)
    test3 = WorldAcousticsFinder(region="test")
    print(test3.query_params)