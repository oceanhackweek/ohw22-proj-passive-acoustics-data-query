# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 12:22:53 2022

@author: kibwo
"""

import pandas as pd
# import datetime


def get_ooi_metadata_LF(**kwargs):
    """
    Expected Keys Parameter kwargs
    ----------
    start_time : datetime.datetime
        time of first acoustic data sample
    end_time : datetime.datetime
        time of the last acoustic data sample
    min_lat : float
        southern boundary, lat/lon bounding box already checked by lat_long_checks.py        
    max_lat : float
        northern boundary, lat/lon bounding box already checked by lat_long_checks.py        
    min_lon : float
        western boundary, lat/lon bounding box already checked by lat_long_checks.py        
    max_lon : float
        eastern boundary, lat/lon bounding box already checked by lat_long_checks.py 
    min_freq : float, optional
        minimum frequency for sampling rate
    max_freq : float, optional
        maximum frequency for sampling rate
    min_depth : float, optional
        minimum depth of the hydrophone
    max_depth : float, optional
        minimum depth of the hydrophone
    
    Returns
    -------
    meta_df : pandas.Dataframe
        dataframe with requested metadata for OOI low frequency hydrophones
    
    """
    # default values in case these aren't passed with keys
    min_freq = -1
    max_freq = -1
    min_depth = -1
    max_depth = -1
    
    for key, value in kwargs.items():
        if key == "min_time":
            start_time = value
            print('start_time: ' + start_time.strftime("%Y-%m-%d %H:%M:%S"))
        elif key == "max_time":
            end_time = value
            print('end_time: ' + end_time.strftime("%Y-%m-%d %H:%M:%S"))
        elif key == "min_lat":
            min_lat = value
            print('min_lat: ' + str(min_lat))
        elif key == "max_lat":
            max_lat = value
            print('max_lat: ' + str(max_lat))
        elif key == "min_long":
            min_lon = value
            print('min_lon: ' + str(min_lon))
        elif key == "max_long":
            max_lon = value
            print('max_lon: ' + str(max_lon))
        elif key == "min_freq":
            min_freq = value
            print('min_freq: ' + str(min_freq))
        elif key == "max_freq":
            max_freq = value
            print('max_freq: ' + str(max_freq))
        elif key == "min_depth":
            min_depth = value
            print('min_depth: ' + str(min_depth))
        elif key == "max_depth":
            max_depth = value
            print('max_depth: ' + str(max_depth))
            
    url = _build_LF_URL(start_time, end_time, min_lat, max_lat, min_lon, max_lon)
    print('url: '+ url)
    
    for k in range(5):
        try:
            df = pd.read_csv(url, sep='|')
            print(df.head())
            break
        except Exception:
            if k == 4:
                print(Exception( ))
                print("   Specific Time window timed out.")
                return None
            
    # Post processing based on freq and depth ranges
    meta_df = df
    if (min_depth >= 0):
        meta_df = meta_df.loc[abs(df[' Elevation ']) >= min_depth]
        
    
    if (max_depth >= 0):
        meta_df = meta_df.loc[abs(meta_df[' Elevation ']) <= max_depth]
        
    if (min_freq >= 0):
        meta_df = meta_df.loc[abs(df[' SampleRate ']) >= min_freq]
        
    
    if (max_freq >= 0):
        meta_df = meta_df.loc[abs(meta_df[' SampleRate ']) <= max_freq]
            
    return meta_df
    
    
    
    
def _build_LF_URL(starttime, endtime, minlat, maxlat, minlon, maxlon):
    
    starttime = starttime.strftime("%Y-%m-%dT%H:%M:%S")
    endtime = endtime.strftime("%Y-%m-%dT%H:%M:%S")
    
    network = "OO"
    channel = "?DH"
    
    base_url = "https://service.iris.edu/fdsnws/station/1/query?"
    netw_url = "net=" + network + "&"
    chan_url = "cha=" + channel + "&"
    strt_url = "start=" + starttime + "&"
    end_url = "end=" + endtime + "&"
    minlat_url = "minlat=" + str(minlat) + "&"
    maxlat_url = "maxlat=" + str(maxlat) + "&"
    minlon_url = "minlon=" + str(minlon) + "&"
    maxlon_url = "maxlon=" + str(maxlon) + "&"
    avail_url = "includeavailability=TRUE&"
    detail_url = "level=channel&"
    form_url = "format=text"    
    
    
    url = (
        base_url
        + netw_url
        + chan_url
        + strt_url
        + end_url
        + minlat_url
        + maxlat_url
        + minlon_url
        + maxlon_url
        + avail_url
        + detail_url
        + form_url
    )
    
    return url
    
            