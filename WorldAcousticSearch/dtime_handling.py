# Author: Roman Battisti
# Project: Passive Acoustic Data Query
# Ocean Hack Week 2022
# GitHub: https://github.com/oceanhackweek/ohw22-proj-passive-acoustics-data-query


import re
import numpy as np
import pandas as pd


def strToDatetime(dtime: str, dayFirst=False, yearFirst=False):
    """
    Convert datetime string to a pandas datetime object.
    
    :param dtime: (str) datetime string. Days, months, years must be separated by - or /, times are separated :.
    :param dayFirst: (bool) whether day comes before month.
    :param yearFirst: (bool) whether year comes before month and day.
    """
    
    return pd.to_datetime(dtime, dayfirst=dayFirst, yearfirst=yearFirst)


def datetimeToISO8610(dtime) -> str:
    """
    Return datetime as a string in the ISO8610 (YYYY-MM-DDTHH:MM:SSZ) format.
    
    :param dtime: (datetime object) datetime to be converted to ISO8610 format
    
    :return: (str) datetime in ISO8610 format
    """
    
    return dtime.strftime('%Y-%m-%dT%H:%M:%SZ')


def addMultipleInputHandling(func) -> list:
    """
    Wraps function which takes a single variable to handle a list.
    """
    
    def wrap(*args, **kwargs) -> list:
        output = []
        for arg in args:
            output.append(func(arg, **kwargs))
        
        return output if len(output) > 1 else output[0]
    
    return wrap