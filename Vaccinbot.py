#!/usr/bin/env python3.6

import requests
import json
import dateutil.parser
from datetime import datetime, timezone
import tabulate
import geopy.distance
from operator import itemgetter

ST_GENIS = (46.2440083, 6.0253162)

my_location = ST_GENIS

seconds_in_day = 60*60*24
department_list_json = requests.get("https://vitemadose.gitlab.io/vitemadose/departements.json").json()
department_list = {}
for dep in department_list_json:
  department_list[dep["code_departement"]] = dep["nom_departement"]

departments = ["01", "38", "73", "74", "39", "71", "69"]
# departments = ["74"]
responses = {}

print("Searching appointments within 24h..")

table_header = ["Vaccine", "Distance", "Day", "Time", "Name", "Location"]
found_appointments = []

for dep in departments:
  print("Searching in " + dep + ", " + department_list[dep])
  now = datetime.now(timezone.utc)
  response = requests.get("https://vitemadose.gitlab.io/vitemadose/" + dep + ".json")
  responses[dep] = response
  if response.status_code == 200:
    response_json = response.json()
    available_centres = response_json["centres_disponibles"]
    for centre in available_centres:
      next_available_appointment = centre["prochain_rdv"]
      appointment_time = dateutil.parser.parse(next_available_appointment)
      time_interval_day = ((appointment_time - now).total_seconds())/seconds_in_day
      if time_interval_day < 1:
        location = (centre["location"]["latitude"], centre["location"]["longitude"])
        distance = round(geopy.distance.distance(location, my_location).km)
        vaccine_types = ",".join(centre["vaccine_type"])
        entry = [
          vaccine_types,
          "{:d}".format(distance) + " km",
          "{:d}".format(appointment_time.day) + "/" + "{:d}".format(appointment_time.month),
          "{:02d}".format(appointment_time.hour) + ":" + "{:02d}".format(appointment_time.minute).format(2),
          centre["nom"],
          centre["location"]["city"] + ", " + department_list[dep]
        ]
        found_appointments.append(entry)

distance_time = lambda tuple: (float(tuple[1][:-3], ))
sorted_appointments = sorted(found_appointments, key=distance_time)
print(tabulate.tabulate(sorted_appointments, headers=table_header))