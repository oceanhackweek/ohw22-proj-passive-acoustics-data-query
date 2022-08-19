# NCEI API reference

- NCEI Passive Acoustic Data map service
    - map viewer: https://www.ncei.noaa.gov/maps/passive_acoustic_data/
    - REST endpoints: https://gis.ngdc.noaa.gov/arcgis/rest/services/passive_acoustic_data/MapServer
- ArcGIS REST API for map service
    - documentation: https://developers.arcgis.com/rest/services-reference/enterprise/map-service.htm
    - example query returning JSON for all records in sub-layer 0 (with a where clause of "1=1"):
        ```
        https://gis.ngdc.noaa.gov/arcgis/rest/services/passive_acoustic_data/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=pjson
        ```
- Notes:
    > Unfortunately, it might be a bit inconvenient to query across all the records at once, since the records are split into multiple "sub-layers" for NRS, ADEON, SanctSound, etc. So, you would have to query against each sub-layer separately.
    
    > we are currently developing a new version of this service hosted in ArcGIS Online, so the URLs will change at some point in the next several months.
