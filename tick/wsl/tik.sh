#!/usr/bin/env bash
cd "/mnt/c/Program Files/InfluxDB"
./influxd.exe &
sleep 2

cd "/mnt/c/Program Files/Kapacitor"
./kapacitord.exe &
sleep 2

cd "/mnt/c/Program Files/Telegraf"
./telegraf.exe &