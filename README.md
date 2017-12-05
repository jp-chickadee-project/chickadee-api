# JPCP Server API

An api to interact with data for the JP chickadee project. 

+ `euclid.nmu.edu:{port}/api` will be the root directory, where ports can be:
	
	+ `8155` - The production api, ideally running constantly and updated during downtime
	
	+ `8160` - The testing api, only running occasionally and updated frequently

All date parameters are assumed to be in unix time format.


# Interaction

## Feeders

| Interaction   | Verb   | Endpoint                                                | Returns                                  | Implemented? |
|---------------|--------|---------------------------------------------------------|------------------------------------------| -------------|
| All Feeders   | GET    | /api/feeders/                                           | List of all feeders                      | Yes          |
| Create Feeder | POST   | /api/feeders/                                           | The created feeder                       | No           |
| Feeder by ID  | GET    | /api/feeders/{feederID}                                 | The specified feeder                     | Yes          |
| Update by ID  | PUT    | /api/feeders/{feederID}                                 | The updated feeder                       | No           |
| Delete by ID  | DELETE | /api/feeders/{feederID}                                 | The empty object {}                      | No           |
| Visit Range   | GET    | /api/feeders/{feederID}?start={aDate}&end={aDate}       | Visits to feeder within given dates      | Yes          |

## Birds

| Interaction   | Verb   | Endpoint                                                | Returns                                  | Implemented? |
|---------------|--------|---------------------------------------------------------|------------------------------------------| -------------|
| All Birds     | GET    | /api/birds/                                             | List of all birds                        | Yes          |
| Create Bird   | POST   | /api/birds/                                             | The created bird                         | No           |
| Bird by ID    | GET    | /api/birds/{rfid}                                       | The specified bird                       | Yes          |
| Update by ID  | PUT    | /api/birds/{rfid}                                       | The updated bird                         | No           |
| Delete by ID  | DELETE | /api/birds/{rfid}                                       | The empty object {}                      | No           |
| Visit Range   | GET    | /api/birds/{rfid}?start={aDate}&end={aDate}             | All visits by the specified bird within given dates| Yes |
| Bird Options  | GET    | /api/birds/options                                      | List of bird options                     | Yes          |

## Visits

| Interaction   | Verb   | Endpoint                                                | Returns                                  | Implemented? |
|---------------|--------|---------------------------------------------------------|------------------------------------------|--------------|
| Visit Range   | GET    | /api/visits?start={aDate}&end={aDate}                   | List of all visits within given dates    | Yes |

# Data Templates

Example data to demonstrate formatting

## Feeders
```
{
	"battery": 0, 
	"id": "CLIF", 
	"fullName": "Cliff", 
	"lastContactTimestamp": 0, 
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
	"legLeftTop": "(i0) - indigo no stripe RFID", 
	"legRightBottom": "(#) - USFWS Number", 
	"legRightTop": "(B) - BLACK darvic", 
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
	"mass": 108
}
```

##Bird Options
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
  "legs": [
    "(ap) - azure pink stripe RFID", 
    "(w0) - white no stripe RFID", 
    "(yp) - yellow pink stripe RFID"
  ], 
  "species": [
    "RBNU", 
    "BCCH", 
    "WBNU"
  ], 
  "suspectedSex": [
    "female", 
    "unknown", 
    "", 
    "male"
  ], 
  "tissueSample": [
    "feather", 
    "none", 
    "no"
  ]
}
