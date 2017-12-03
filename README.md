FORMAT: 1A

# JPCP Server API

An api to interact with data for the JP chickadee project.


# Interaction

## Feeder Table [/api/feeders]

### List All Feeders [GET]

+ Response 200 (application/json)

		[
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
		]

### Create New Feeder [POST]
Not Yet Implemented

+ Request  (application/json)

		{
			"battery": 0, 
			"feederID": "CARP", 
			"fullName": "Carpenter", 
			"lastContact": 0, 
			"lastPath": "", 
			"lastStatus": "", 
			"latitude": 46.5544600, 
			"longitude": -87.4268200
		}

+ Response 201 (application/json)

## Specific Feeder [/api/feeders/{feederID}]

+ Parameters
	+ feederID (string) - ID of a birdfeeder

### Get Feeder Details [GET]
Not Yet Implemented

+ Response 200 (application/json)
	
		[
			{
				"battery": 0, 
				"feederID": "CARP", 
				"fullName": "Carpenter", 
				"lastContact": 0, 
				"lastPath": "", 
				"lastStatus": "", 
				"latitude": 46.5544600, 
				"longitude": -87.4268200
			}
		]

### Delete Feeder [DELETE]

 + Response 204




## Bird Table [/api/feeders]

### List All Birds [GET]

+ Response 200 (application/json)

		[
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
		]

### Create New Bird [POST]
Not Yet Implemented

+ Request  (application/json)

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

+ Response 201 (application/json)

## Specific Bird Operations [/api/feeders/{rfid}]

+ Parameters
	+ rfid (string) - RFID corresponding to a bird

### Get Bird Details [GET]

+ Response 200 (application/json)
	
		[
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
		]

### Delete Bird [DELETE]

+ Response 204
