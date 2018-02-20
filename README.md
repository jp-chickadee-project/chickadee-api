# JPCP Server API
An api to interact with data for the JP chickadee project. 

+ `euclid.nmu.edu:{port}/api` will be the root directory, where ports can be:
	
	+ `8155` - The production api, ideally running constantly and updated during downtime
	
	+ `8160` - The testing api, only running occasionally and updated frequently

All date parameters are assumed to be in unix time format.


### To Run:
Dependencies:

    Flask==0.12
    Flask_MySQLdb==0.2.0
    flask_cors==3.0.3
    mysql_connector_repackaged==0.3.1
    
A local instance of mysql with the correct schema is required. Runtime configuration of the api and database are specified in a json file named `config` in the same directory as `app.py`, with the following format:

  	{
      "username": "", 					# username for mysql
      "password": "",					# password for mysql
      "database": "chickadeesTesting",	# name of database to use
      "host": "localhost",				# hostname for flask server to run on
      "port": 8155,						# port for flask server to run on
  	}

This format is temporary and best used for development, the ideal endgame is to have username/password be entered as input when `app.py` is run and to have flask deployed on Apache to handle hosting needs.

Running `python3 app.py` will start hosting on the hostname/port from the config file.
     
    
### To Run Tests:
While in the same directory as `app.py`, running the package `nose2` will search for all test cases and run them, with no further configuration needed.
 		



# Interaction

## Feeders


| Interaction   | Verb   | Endpoint                                                | Returns                                  | 
|---------------|--------|---------------------------------------------------------|------------------------------------------| 
| All Feeders   | GET    | /api/feeders                                            | List of all feeders                      |
| Create Feeder | POST   | /api/feeders                                            | The created feeder                       |
| Feeder by ID  | GET    | /api/feeders/{feederID}                                 | The specified feeder                     |
| Update by ID  | PUT    | /api/feeders/{feederID}                                 | The updated feeder                       |
| Delete by ID  | DELETE | /api/feeders/{feederID}                                 | The empty object {}                      |

## Birds

| Interaction   | Verb   | Endpoint                                                | Returns                                  |
|---------------|--------|---------------------------------------------------------|------------------------------------------|
| All Birds     | GET    | /api/birds                                              | List of all birds                        |
| Create Bird   | POST   | /api/birds                                              | The created bird                         |
| Bird by ID    | GET    | /api/birds/{rfid}                                       | The specified bird                       |
| Update by ID  | PUT    | /api/birds/{rfid}                                       | The updated bird                         |
| Delete by ID  | DELETE | /api/birds/{rfid}                                       | The empty object {}                      |
| Bird Options  | GET    | /api/birds/options                                      | List of bird options                     |

## Visits

| Interaction   | Verb   | Endpoint | Returns | Parameters |
|---------------|--------|--------------------|--------------------------------|------------------------------|
| Add Visit     | POST   | /api/visits        | The created visit              |                              |
| Visit Range   | GET    | /api/visits        | List of matching visits        | rfid, feederID, start, end   |
| Latest Visits | GET    | /api/visits/latest | List of matching latest visits | rfid, feederID, limit        |

# Data Templates

Example data to demonstrate formatting

## Feeders
```
{
	"battery": 0, 
	"id": "CLIF", 
	"fullName": "Cliff", 
	"lastContact": 0, 
	"lastPath": "", 
	"lastStatus": "", 
	"latitude": 46.5523000, 
	"longitude": -87.4243000
}
```
## Birds
```
{
	"bagAndBirdWeight": 22.75, 
	"bagWeight": 12.3, 
	"bandNumber": "2830-56002", 
	"banders": "Lindsay, Szarmach", 
	"bandCombo": "#B/v0"
	"bibWidth": 22.5, 
	"billDepth": 3.7, 
	"billLength": 5.1, 
	"billWidth": 3.5, 
	"birdWeight": 10.45, 
	"capLength": 32.5, 
	"captureSite": "Carpenter Net", 
	"captureTimestamp": 1507296600, 
	"image": null, 
	"legLeftBottom": "NONE", 
	"legLeftTop": "v0", 
	"legRightBottom": "#", 
	"legRightTop": "B",
	"logTimestamp": 1507579560, 
	"longestSecondary": 54, 
	"netEnterTimestamp": 1507262400, 
	"netExitTimestamp": 1507262400, 
	"notes": "molting R6, R6 photos taken", 
	"releasedTimestamp": 1507262400, 
	"rfid": "011016A4D4", 
	"species": "BCCH", 
	"suspectedSex": "unknown", 
	"tailLength": 61, 
	"tarsusLength": 17.7, 
	"tissueSample": "feather", 
	"weather": "Clear, 55F", 
	"wingChordLength": 63
}
```
## Visits
```
{
	"rfid": 011016A269
	"feederID": CLIF
	"visitTimestamp": 1492873308
	"temperature": 44
	"mass": 108,
    "bandCombo": "#a0/V"
}
```

## Bird Options
```
{
  "banders": [
    "Richards", 
    "Nate", 
    "SJS", 
    "James", 
    "Selewski", 
    "Dershem"
  ], 
  "captureSite": [
    "Carpenter Net", 
    "Cliffside Net", 
    "Riley Net"
  ], 
  "bands": {
    "#": "USFWS Number", 
    "A": "AZURE darvic", 
    "B": "BROWN darvic", 
    "G": "GREEN darvic", 
    "V": "VIOLET darvic",  
    "a0": "azure no stripe RFID", 
    "ab": "azure black stripe RFID", 
    "ag": "azure green stripe RFID", 
  }, 
  "species": [
    "RBNU", 
    "BCCH", 
    "WBNU"
  ], 
  "suspectedSex": [
    "female", 
    "unknown", 
    "male"
  ], 
  "tissueSample": [
    "feather", 
    "none"
  ]
}
