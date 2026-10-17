FROM debian:13

ENV PIP_BREAK_SYSTEM_PACKAGES=1

COPY requirements.txt /tmp

# hadolint ignore=DL3008
RUN apt-get clean \
  && apt-get update \
  && apt-get install --no-install-recommends -y \
    iproute2 \
    iputils-ping \
    net-tools \
    openntpd=1:6.2p3-4.2+b3 \
    python3-pip \
    procps \
    sudo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && chmod 544 /etc/openntpd/ntpd.conf \
  && chown ntpd:ntpd /etc/openntpd/ntpd.conf \
  && pip install --no-cache-dir -r /tmp/requirements.txt \
  && useradd -G sudo bar

COPY --chmod=544 --chown=ntpd ntpd.conf /etc/openntpd/ntpd.conf

COPY issue21.txt /tmp
COPY john-smith.json /tmp
COPY install-dist-package.sh /usr/local/bin/install-dist-package.sh

CMD ["sh", "-c", "service openntpd start && sleep infinity"]
