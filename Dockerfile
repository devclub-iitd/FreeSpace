FROM python:3.6

RUN apt-get update

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

WORKDIR /Free-Space

COPY requirements.txt ./

RUN apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN pip install -r requirements.txt

COPY . /Free-Space/

RUN ./folderCreate.sh
RUN python html_generator.py

EXPOSE 8080

CMD [ "python3","-m","http.server","8080" ]