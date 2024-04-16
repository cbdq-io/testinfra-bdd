#!/bin/sh
set -ex
cd /tmp
export VERSION=$( ls /mnt/dist/testinfra_bdd-*.gz | cut -d- -f2 | cut -d. -f1,2,3 )
pip install --force-reinstall --quiet /mnt/dist/testinfra_bdd-*.tar.gz
