"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        global call_count 
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            call_count += 1
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


# TODO Add any functions you need here
def displaysort(urls:list):
  threads = []
  names = []
  for url in urls:
      obj = Request_thread(url)
      threads.append(obj)
  
  for thread in threads:
      thread.start()

  for thread in threads:
      thread.join()

  for objs in threads:
       names.append(objs.response["name"])
  
  names.sort()

  return names
      
def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    topapi = Request_thread(TOP_API_URL)
    topapi.start()
    topapi.join()

    # TODO Retireve Details on film 6
    movie6 = Request_thread(f'{topapi.response["films"]}6')
    movie6.start()
    movie6.join()

    # TODO Display results
    log.write("-----------------------------------------")
    log.write(f'Title   : {movie6.response["title"]}')
    log.write(f'Director: {movie6.response["director"]}')
    log.write(f'Producer: {movie6.response["producer"]}')
    log.write(f'Released: {movie6.response["release_date"]}')
    log.write("")
    characters = displaysort(movie6.response["characters"])
    planets = displaysort(movie6.response["planets"])
    starships = displaysort(movie6.response["starships"])
    vehicles = displaysort(movie6.response["vehicles"])
    species = displaysort(movie6.response["species"])

    log.write(f'Characters :{len(characters)}')
    log.write(", ".join(characters))
    log.write("")
    log.write(f'Planets :{len(planets)}')
    log.write(", ".join(planets))
    log.write("")
    log.write(f'Starships :{len(starships)}')
    log.write(", ".join(starships))
    log.write("")
    log.write(f'Vehicles :{len(vehicles)}')
    log.write(", ".join(vehicles))
    log.write("")
    log.write(f'Species :{len(species)}')
    log.write(", ".join(species))
    log.write("")

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
