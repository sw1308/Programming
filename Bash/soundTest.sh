#!/bin/bash

# USAGE
# arecord -Diec958:CARD=U0x46d0x825,DEV=0 -f S16_LE | soundTest.sh

function ord {
    printf '%d' "'$1"
}

while read -rs -n 1 char
do
    printf "%$(ord $char)s\n" "|"
done < "${1:-/dev/stdin}"
