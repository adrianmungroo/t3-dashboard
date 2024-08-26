Dataset are grouped into either Historical (Time Series, .csv) or GIS (spatial, geojson). Then by Key Variable (Jobs, Generation, etc.) Each folder contains a text file called #_DataSource which gives information on the files in that folder. Under each filename, there are descriptors, explained here:

Type
--------------------------------------
There are three data types:
(1) Time Series: There will always be a column titled "Year" and then corresponding values. They all describe the same geographical region, which is specified under "Spatial Range" and in the file title. 
(2) County: Gives data to be mapped to counties. There will be a column titled "FIPS".
(3) Tract: Gives data to be mapped to census tracts. There will be a column titled "FIPS".

Spatial Range
----------------------------------
Clarifies what region the data is related to. Examples: Georgia, Fulton County, SOCO Balancing Authority. This info should also be 

Description
-----------------------------------
Gives what information is contained in the dataset. Includes what years data covers.

Data Source
-----------------------------------
Provides a link to where raw data was downloaded

Methodology
----------------------------------
Describes what processing was done to the raw data. 
Examples: Deleting info from other states, replacing missing data with zero values

Notes
----------------------------------
Additional potentially relevant information.