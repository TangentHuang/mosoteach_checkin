FROM harisekhon/debian-java:jre8

# install python
RUN apt-get -y install python3
RUN apt-get -y install python3-pip


WORKDIR /usr/src/app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt



