FROM amdavidson/dockertools

RUN apt-get update && \
apt-get -y install python3 python3-pandas sqlite

CMD bash
