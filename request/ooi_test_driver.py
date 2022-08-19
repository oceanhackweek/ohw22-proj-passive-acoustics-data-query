# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 17:10:54 2022

@author: kibwo
"""

import datetime
import ooi_request

start_time = datetime.datetime(2016,1,7,0,0,0)
end_time = datetime.datetime(2017,1,8,0,0,0)

ooi_meta = ooi_request.get_ooi_metadata_LF(min_time= start_time, max_time= end_time, min_lat= 44, max_lat= 47 , min_long= -135, max_long= -125)