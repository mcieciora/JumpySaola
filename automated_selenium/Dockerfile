FROM ubuntu:20.04
MAINTAINER mcieciora
RUN apt-get update -y && apt-get install -y python3-pip python3-dev

COPY ../requirements-dev.txt /selenium/requirements-dev.txt

WORKDIR /selenium

RUN pip install -r requirements-dev.txt

COPY . /selenium

CMD [ "tar -C /usr/local/bin/ -xvf geckodriver-v0.30.0-linux32.tar" ]

ENTRYPOINT [ "pytest" ]

CMD [ "-x ." ]