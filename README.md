# Vaccinbot

Simple bot that automatically downloads data from ViteMaDose to find appointments within 24h. 
By default it finds appointments for all vaccine types within 50km from St. Genis-Pouilly.

Use:

```
usage: Vaccinbot.py [-h] [--interval INTERVAL] [--slack-token SLACK_TOKEN]
                    [--free-mobile-user FREE_MOBILE_USER]
                    [--free-mobile-password FREE_MOBILE_PASSWORD]
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
                        Path to file containing a slack token (activates Slack
                        bot feature).
  --free-mobile-user FREE_MOBILE_USER
                        User to be used with the Free Mobile SMS API
  --free-mobile-password FREE_MOBILE_PASSWORD
                        Path to file containing a Free mobile password.
  --location LAT LONG   Latitude and longitude of your location. Default: St.
                        Genis.
  --max-distance MAX_DISTANCE
                        Maximum radius of search from your position in km.
                        Default: 50 km
  --vaccines [VACCINES [VACCINES ...]]
                        List of vaccines to look for. P=Pfizer-BioNTech;
                        M=Moderna; AZ=AstraZeneca; J=Janssen. Default: all.
  --depts [DEPTS [DEPTS ...]]
                        List of department numbers where to look for vaccines
                        (add 0 before single-digit depts. e.g. 01 not 1).
                        Default: 01 (Ain) + neighbouring depts.
```

### Examples:

Text only:

```bash
./Vaccinbot.py --interval 20 --location 46 6 --max-distance 55 --vaccines P  
```

Slack bot:

```bash
python3.6 Vaccinbot.py --interval 20 --slack-token slack_token.txt --location 46 6 --max-distance 55 --vaccines AZ J 
```

Free Mobile API, credits: [Mael-Le-Garrec](https://github.com/Mael-Le-Garrec)

```bash
python3.6 Vaccinbot.py --free-mobile-user 12345678 --free-mobile-password free_password.txt
```

## Dependencies

The dependencies can be installed from the command line via `pip`:
```
pip install -r requirements.txt
```

Credits: [RKHashmani](https://github.com/RKHashmani).

## Slack bot

Create a Slack app, create the channel ```#vaccinbot```, copy and paste the app token in a file. Link the file via the ```---slack-token``` option.
This will enable the Slack bot integration.

## Free Mobile

Access your personal area, enable SMS notifications under My Options, copy and paste your API token in a file. 

## Other integration?

PRs for other chat types are welcome!


## Other credits

* [alexander-held](https://github.com/alexander-held): lighter Docker image
* [defranchis](https://github.com/defranchis): improved day selection
