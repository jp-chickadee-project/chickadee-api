# Chickadee Server
This will run on euclid and serve as the intermediary between the main Raspberry Pi, the website, and the database. It uses threading to manage multiple requests.

Currently it accepts input in the form of a json dictionary, expecting it to have a key 'cmd' corresponding to what the client is requesting. At the moment the valid commands are:

  * **event**
    
      Expected to come from the Pi to indicate that a feeder has been visited; input should also contain all info about the visit
  
  * **sleep**
    
      Put a birdfeeder into sleep mode; input should also contain the ID of the requested feeder
  
  * **restart**
    
      Restart a birdfeeder