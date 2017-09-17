FROM harisekhon/debian-java:jre8
FROM java:8

# install python
RUN apt-get -y install python3
RUN apt-get -y install python3-pip


WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt



