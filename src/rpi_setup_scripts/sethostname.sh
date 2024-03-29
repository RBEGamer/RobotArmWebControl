#!/bin/bash
# /usr/sbin/change_hostname.sh - program to permanently change hostname.  Permissions
# are set so that www-user can `sudo` this specific program.
#https://stackoverflow.com/questions/41582334/how-do-i-change-the-hostname-using-python-on-a-raspberry-pi
# args:
# $1 - new hostname, should be a legal hostname

sed -i "s/$HOSTNAME/$1/g" /etc/hosts
echo $1 > /etc/hostname
#/etc/init.d/hostname.sh
hostname $1  # this is to update the current hostname without restarting
