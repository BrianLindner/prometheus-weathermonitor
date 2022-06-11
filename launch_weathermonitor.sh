#!/bin/bash

BASEDIR=$(dirname "$0")

source venv/bin/activate

nohup python weathermonitor.py > logs/weathermonitor.log &

deactivate
