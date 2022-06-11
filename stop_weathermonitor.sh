#!/bin/bash

BASEDIR=$(dirname "$0")

ps aux | grep "Python weather_monitor.py" | awk '{print $2}' | xargs kill -9
