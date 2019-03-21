FROM python:3.6

ARG COOKIE_ID

RUN apt-get update

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

WORKDIR /Free-Space

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /Free-Space/

# RUN python tableGen.py $COOKIE_ID
EXPOSE 8080

CMD [ "python3","-m","http.server","8080" ]