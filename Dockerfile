FROM python:3.9-slim

ADD Vaccinbot.py ./
ADD requirements.txt .

RUN pip install -r requirements.txt


ENTRYPOINT [ "./Vaccinbot.py" ]