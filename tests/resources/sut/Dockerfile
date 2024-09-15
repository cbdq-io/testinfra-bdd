FROM debian:11

COPY requirements.txt /tmp

# hadolint ignore=DL3008
RUN apt-get clean \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    iproute2 \
    iputils-ping \
    net-tools \
    ntp=1:4.2.8p15+dfsg-1 \
    python3-pip \
    procps \
    sudo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && chmod 544 /etc/ntp.conf \
  && chown ntp:ntp /etc/ntp.conf \
  && pip install --no-cache-dir -r /tmp/requirements.txt \
  && useradd -G sudo bar

COPY issue21.txt /tmp
COPY john-smith.json /tmp
COPY install-dist-package.sh /usr/local/bin/install-dist-package.sh

CMD ["sh", "-c", "service ntp start && sleep infinity"]
