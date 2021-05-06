FROM python

RUN python -m pip install tabulate geopy requests python-dateutil slackclient

ADD Vaccinbot.py slack_token.txt ./

ENTRYPOINT [ "./Vaccinbot.py" ]