#!/usr/bin/env python

import requests
import json
import dateutil.parser
from datetime import datetime, timezone
import tabulate
import geopy.distance
from operator import itemgetter
import slack
import time
import argparse

SECONDS_IN_DAY = 60*60*24

ST_GENIS = (46.2440083, 6.0253162)
MY_LOCATION = ST_GENIS
PING_INTERVAL_MINUTES = 15
SLACK_TOKEN_FILE = None
MAX_DISTANCE = 50
DEPARTMENTS = ["01", "38", "73", "74", "39", "71", "69"]

VACCINES={}
VACCINES["P"] = "Pfizer-BioNTech"
VACCINES["M"] = "Moderna"
VACCINES["AZ"] = "AstraZeneca"
VACCINES["J"] = "Janssen"
VACCINES["mRNA"] = "ARNm"
SELECTED_VACCINES = ["Pfizer-BioNTech", "Moderna", "AstraZeneca", "ARNm", "Janssen"]

parser = argparse.ArgumentParser(description="A bot that automatically fetches date from ViteMaDose and finds appointments within 24h.")
parser.add_argument("--interval", type=int, help="Time in minutes between queries to ViteMaDose. Default: " + str(PING_INTERVAL_MINUTES), default=PING_INTERVAL_MINUTES)
parser.add_argument("--slack-token", type=argparse.FileType(), help="Path to file containing a slack token (activates Slack bot feature).")
parser.add_argument("--location", type=float, metavar=("LAT", "LONG"), nargs=2, help="Latitude and longitude of your location. Default: St. Genis.", default=ST_GENIS)
parser.add_argument("--max-distance", type=int, help="Maximum radius of search from your position. Default: " + str(MAX_DISTANCE) , default=MAX_DISTANCE)
parser.add_argument("--vaccines", type=str, nargs="*", help="List of vaccines to look for. P=Pfizer-BioNTech;  M=Moderna; AZ=AstraZeneca; J=Janssen. Default: all.", default=SELECTED_VACCINES)
parser.add_argument("--depts", type=str, nargs="*", help="List of department numbers where to look for vaccines (add 0 before single-digit depts. e.g. 01 not 1). Default: 01 (Ain) + neighbouring depts.", default=DEPARTMENTS)

args = parser.parse_args()

PING_INTERVAL_MINUTES = args.interval
SLACK_TOKEN_FILE = args.slack_token
MY_LOCATION = args.location
MAX_DISTANCE = args.max_distance
SELECTED_VACCINES = [VACCINES[v] for v in args.vaccines]
DEPARTMENTS = args.depts

def postMessage(client, message, channel):
  response = client.chat_postMessage(
    channel=channel,
    text=message
  )

department_list_json = requests.get("https://vitemadose.gitlab.io/vitemadose/departements.json").json()
department_list = {}
for dep in department_list_json:
  department_list[dep["code_departement"]] = dep["nom_departement"]

responses = {}

print("Looking for:", SELECTED_VACCINES)
print("Radius:", MAX_DISTANCE, "km")
print("Searching appointments within 24h...")

table_header = ["Vaccine", "Distance", "Day", "Time", "Location", "URL"]

while(True):

  found_appointments = []

  for dep in DEPARTMENTS:
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
        time_interval_day = ((appointment_time - now).total_seconds())/SECONDS_IN_DAY
        if time_interval_day < 1:
          location = (centre["location"]["latitude"], centre["location"]["longitude"])
          distance = round(geopy.distance.distance(location, MY_LOCATION).km)
          vaccine_types = centre["vaccine_type"]
          if (distance < MAX_DISTANCE) and (len(list(set(SELECTED_VACCINES) & set(vaccine_types))) > 0) :
            vaccine_types_str = ",".join(vaccine_types)
            entry = [
              vaccine_types_str,
              "{:d}".format(distance) + " km",
              "{:d}".format(appointment_time.day) + "/" + "{:d}".format(appointment_time.month),
              "{:02d}".format(appointment_time.hour) + ":" + "{:02d}".format(appointment_time.minute),
              # centre["nom"],
              centre["location"]["city"] + ", " + department_list[dep],
              centre["url"]
            ]
            found_appointments.append(entry)

  distance_time = lambda tuple: (float(tuple[1][:-3], ))
  sorted_appointments = sorted(found_appointments, key=distance_time)
  print("\n")
  print(tabulate.tabulate(sorted_appointments, headers=table_header))
  print("\n")

  if SLACK_TOKEN_FILE is not None: 
    if len(sorted_appointments) > 0:
      client = slack.WebClient(token=SLACK_TOKEN_FILE.readline())
      postMessage(client, 
          "```" + tabulate.tabulate(sorted_appointments, headers=table_header) + "```",
        "#vaccinbot"
      )

  print("Sleeping, back in", PING_INTERVAL_MINUTES, " minutes")
  time.sleep(60*PING_INTERVAL_MINUTES)