#!/bin/bash

BASEDIR=$(dirname "$0")

ps aux | grep "Python weathermonitor.py" | awk '{print $2}' | xargs kill -9
