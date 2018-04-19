# JPCP Server API
An api to interact with data for the JP chickadee project. All date parameters are assumed to be in unix time format.

### To Run:
Install dependencies:

	pip3 install -r requirements.txt

Create database:

	python3 manage.py createdb -u <username> --dbname <database>

After creating the database, edit `config.py` to match the desired database name.

Running development server:

	python3 manage.py runserver -h <HOSTNAME> -p <PORT>
	
### To Run Tests:

	python3 manage.py test

### To Load Visits:
	
	python3 manage.py loadvisits -v <zipfile> -u <username> -d <database>

The above command will open a given zipfile, which is specified by an absolute path like `~/Downloads/visits.zip`, and run through each file inside it. The files given by the bio students have the format `CLIF_2017-06-16.TXT`, where the first four letters are the feederID for all the visits inside that file. The script will then load those visits into the specified database, if it exists and has the proper schema. 

### To Backup Database:
	
	python3 manage.py backup -u <username> -d <database>

Backing up the database will create a file named 'chickadees.sql' in the home directory. This file can be loaded into mysql with the command `mysql <dbname> < chickadees.sql`

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

Example data to demonstrate formatting. When adding data entries, the fields denoted by a `*` are required while the rest are optional and will typically default to NULL.

## Feeders
```
{
	"battery": 0, 
*	"id": "CLIF", 
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
*	"bandCombo": "#B/v0"
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
*	"rfid": "011016A4D4", 
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
*	"rfid": "011016A269",
*	"feederID": "CLIF",
*	"visitTimestamp": 1492873308,
	"temperature": 44,
	"mass": 108,
    	"bandCombo": "#a0/V",
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
