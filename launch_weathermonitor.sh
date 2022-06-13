#!/bin/bash

BASEDIR=$(dirname "$0")

source venv/bin/activate

mkdir -p logs/
nohup python weathermonitor.py &

deactivate
