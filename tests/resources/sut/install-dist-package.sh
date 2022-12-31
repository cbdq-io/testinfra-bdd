#!/bin/sh
set -ex
cd /tmp
export VERSION=$( ls /mnt/dist/testinfra-bdd-*.gz | cut -d- -f3 | cut -d. -f1,2,3 )
pip install -q /mnt/dist/testinfra-bdd-*.tar.gz
