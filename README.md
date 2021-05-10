# Vaccinbot

Simple bot that automatically downloads data from ViteMaDose to find appointments within 24h. 

Use:

```
usage: Vaccinbot.py [-h] [--interval INTERVAL] [--slack-token SLACK_TOKEN]
                    [--location LAT LONG] [--max-distance MAX_DISTANCE]
                    [--vaccines [VACCINES [VACCINES ...]]]
                    [--depts [DEPTS [DEPTS ...]]]

A bot that automatically fetches date from ViteMaDose and finds appointments
within 24h.

optional arguments:
  -h, --help            show this help message and exit
  --interval INTERVAL   Time in minutes between queries to ViteMaDose.
                        Default: 15
  --slack-token SLACK_TOKEN
                        Path to file containing a slack token (activates Slack bot feature).
  --location LAT LONG   Latitude and longitude of your location. Default: St. Genis.
  --max-distance MAX_DISTANCE
                        Maximum radius of search from your position in km. 
                        Default: 50 km
  --vaccines [VACCINES [VACCINES ...]]
                        List of vaccines to look for. P=Pfizer-BioNTech; M=Moderna; AZ=AstraZeneca; J=Janssen; mRNA. Default: all.
  --depts [DEPTS [DEPTS ...]]
                        List of department numbers where to look for vaccines
                        (add 0 before single-digit depts. e.g. 01 not 1).
                        Default: 01 (Ain) + neighbouring depts.
```

Example:

No Slack bot:
```./Vaccinbot.py --interval 20 --location 46 6 --max-distance 55 --vaccines P  ```

With Slack bot:
```python3.6 Vaccinbot.py --interval 20 --slack-token slack_token.txt --location 46 6 --max-distance 55 --vaccines AZ J ```

## Slack bot

Create a Slack app, create the channel ```#vaccinbot```, copy and paste the app token in a file. Link the file via the ```---slack-token``` option.
This will enable the Slack bot integration.

## Other integration?

PRs for other chat types are welcome!
