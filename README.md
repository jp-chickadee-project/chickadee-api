# JPCP Server API

An api to interact with data for the JP chickadee project. `euclid.nmu.edu/api`
 will be the root directory. For the parameters, all dates are assumed to be in unix time format.


# Interaction

## Feeders

| Interaction   | Verb   | Endpoint                                                | Returns                                  | Implemented? |
|---------------|--------|---------------------------------------------------------|------------------------------------------| -------------|
| All Feeders   | GET    | /api/feeders/                                           | List of all feeders                      | Yes          |
| Create Feeder | POST   | /api/feeders/                                           | The created feeder                       | No           |
| Feeder by ID  | GET    | /api/feeders/{feederID}                                 | The specified feeder                     | Yes          |
| Update by ID  | PUT    | /api/feeders/{feederID}                                 | The updated feeder                       | No           |
| Delete by ID  | DELETE | /api/feeders/{feederID}                                 | The empty object {}                      | No           |
| Visit Range   | GET    | /api/feeders/{feederID}?start={aDate}&end={aDate}       | Visits to feeder within given dates      | No           |

## Birds

| Interaction   | Verb   | Endpoint                                                | Returns                                  | Implemented? |
|---------------|--------|---------------------------------------------------------|------------------------------------------| -------------|
| All Birds     | GET    | /api/birds/                                             | List of all birds                        | Yes          |
| Create Bird   | POST   | /api/birds/                                             | The created bird                         | No           |
| Bird by ID    | GET    | /api/birds/{rfid}                                       | The specified bird                       | Yes          |
| Update by ID  | PUT    | /api/birds/{rfid}                                       | The updated bird                         | No           |
| Delete by ID  | DELETE | /api/birds/{rfid}                                       | The empty object {}                      | No           |
| Visit Range   | GET    | /api/birds/{rfid}?start={aDate}&end={aDate}             | All visits by the specified bird within given dates| No |

## Visits

| Interaction   | Verb   | Endpoint                                                | Returns                                  |
|---------------|--------|---------------------------------------------------------|------------------------------------------|
| Visit Range   | GET    | /api/visits?start={aDate}&end={aDate}                   | List of all visits within given dates    |

# Data Templates

Example data to demonstrate formatting

## Feeders
```
{
	"battery": 0, 
	"feederID": "CLIF", 
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
	"bagAndBirdWeight": 22.5000, 
	"bagWeight": 12.3000, 
	"bandNumber": "2830-56001", 
	"banders": "Lindsay, Szarmach", 
	"bibLength": 0.00, 
	"billDepth": 3.50, 
	"billLength": 10.30, 
	"billWidth": 3.40, 
	"birdWeight": 10.2000, 
	"capLength": 0.00, 
	"captureSite": "Carpenter Net", 
	"captureTimestamp": 1507296600, 
	"image": null, 
	"leftLegBottom": "(#) - USFWS Number", 
	"leftLegTop": "(Y) - YELLOW darvic", 
	"logTimestamp": 1507579380, 
	"longestSecondary": 54, 
	"netEnter": 1507262400, 
	"netExit": 1507262400, 
	"notes": "hallux 8.8", 
	"released": 1507262400, 
	"rfid": "011016A269", 
	"rightLegBottom": "NONE", 
	"rightLegTop": "(g0) - green no stripe RFID", 
	"species": "RBNU", 
	"suspectedSex": "female", 
	"tailLength": 37, 
	"tarsus": 16.50, 
	"tissueSample": "feather", 
	"weather": "Clear, 55F", 
	"wingChord": 66
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
