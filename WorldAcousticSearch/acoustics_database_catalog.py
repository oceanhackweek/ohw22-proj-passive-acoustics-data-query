# Author: Roman Battisti
# Project: Passive Acoustic Data Query
# Ocean Hack Week 2022
# GitHub: https://github.com/oceanhackweek/ohw22-proj-passive-acoustics-data-query


# add database access py file to import and database information to catalog and database_longname.
# if database falls into a particular domain (ex. ocean, terrestrial), can add to appropriate list.

# database access api should accept a **query_params dictionary, which will have user provided query parameters.
# many parameters may have no input.


from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd


def placeholder(**kwargs):
    df = pd.DataFrame(kwargs, index=[0])
    for k in standardized_column_output:
        if k not in kwargs:
            df[k] = float('nan')
    return df

catalog = {
           "NCEI": placeholder,
           "ONC": placeholder,
           "OOI_IRIS": placeholder,
           "OOI_2": placeholder
          }

database_longname = {
                     "NCEI": "Something",
                     "ONC": "Ocean Networks Canada",
                     "OOI_1": "Ocean Observatories Initiative IRIS",
                     "OOI_2": "Ocean Observatories Initiative ..."
                    }

freshwater = []

terrestrial = []

marine = ["NCEI", "ONC", "OOI_1", "OOI_2"]


database_subsections = {
                        "all": list(catalog.keys()),
                        "freshwater": freshwater,
                        "marine": marine,
                        "terrestrial": terrestrial
                       }


standardized_column_output = ["filename", "min_time", "max_time", "min_lat", "max_lat", "min_long", "max_long", "min_freq", "max_freq", "min_depth", "max_depth", "data_url"]
