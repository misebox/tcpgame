#!/bin/bash

python3 server.py &

SRV_PID=$$
echo $SRV_PID

python3 client.py

kill $SRV_PID

