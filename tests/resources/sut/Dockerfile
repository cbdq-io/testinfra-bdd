FROM debian:11

RUN apt-get clean \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    iproute2=5.10.0-4 \
    iputils-ping=3:20210202-1 \
    net-tools=1.60+git20181103.0eebece-1 \
    ntp=1:4.2.8p15+dfsg-1 \
    python3-pip=20.3.4-4+deb11u1 \
    procps=2:3.3.17-5 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && chmod 544 /etc/ntp.conf \
  && chown ntp:ntp /etc/ntp.conf \
  && pip install --no-cache-dir semver==2.12.0 testinfra-bdd==2.1.0

COPY issue21.txt /tmp
COPY john-smith.json /tmp

CMD ["sh", "-c", "service ntp start && sleep infinity"]
