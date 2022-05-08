FROM debian:11

RUN apt-get clean \
  && apt-get update \
  && apt-get install --no-install-recommends -y ntp=1:4.2.8p15+dfsg-1 procps=2:3.3.17-5 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && chmod 544 /etc/ntp.conf \
  && chown ntp:ntp /etc/ntp.conf
