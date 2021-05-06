FROM python

RUN python -m pip install tabulate geopy requests python-dateutil

ADD Vaccinbot.py . 

ENTRYPOINT [ "./Vaccinbot.py" ]