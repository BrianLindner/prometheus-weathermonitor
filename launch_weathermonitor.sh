#!/bin/bash

BASEDIR=$(dirname "$0")

source venv/bin/activate

nohup python weather_monitor.py > logs/weather_monitor.log &

deactivate
