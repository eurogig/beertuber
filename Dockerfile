FROM python:3.7


COPY requirements .
RUN pip install -r requirements

COPY youtubetemplate.txt
COPY beertypes.csv

COPY untappd_noauth.py .
COPY getlatestcheckin.py .
COPY Google.py .

CMD [ "python", "getlatestcheckin.py" ]
