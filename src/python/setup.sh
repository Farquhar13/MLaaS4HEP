#!/bin/bash
# setup uproot
export PYTHONPATH=/Users/vk/CMS/RandD/usr/lib/python2.7/site-packages:$PYTHONPATH
# setup pyxrootd
export PYTHONPATH=$PYTHONPATH:/Users/vk/CMS/RandD/xrootd-4.7.0/build/build/lib.macosx-10.13-x86_64-2.7
if [ "`hostname`" == "vkair" ]; then
    source /opt/anaconda2/etc/profile.d/conda.sh
    export PYTHONPATH=$PYTHONPATH:/opt/anaconda2/lib/python2.7/site-packages
fi
