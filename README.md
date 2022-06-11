# Prometheus Weather Monitor

## Overview

A weather monitoring service to retrieve weather data from a variety of weather sources and send to a Prometheus instalation via a Pushgateway

---

## Requirements

* Prometheus instalation
* A Prometheus Pushgateway configured
  * [Prometheus Pushgateway](https://prometheus.io/docs/practices/pushing/)
  * [https://github.com/prometheus/pushgateway](https://github.com/prometheus/pushgateway)
* API Keys to weather services (See [Configuration](#Configuration))

---

## Installation

```shell
# setup virtual environment
python3 -v venv venv
```
Install modules
```shell
source venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

Place configuration settings in local **config.ini** file
(see [config.ini.example](config.ini.example))

* **[SETTINGS]** (Section):

  * **check_interval_minutes** : number of minutes to wait between weather service checks
  * **pushgateway** : the URL to the Prometheus pushgateway service to send metrics to
  * **log_level** : Level of logging [DEBUG, INFO, WARN, ERROR]
<br/>

* **[API_KEYS]** (section)
  the API keys/secrets for each service
  * **[name of service]** : <API Key/secret**>
<br/>

* **[LOCATIONS]** (Section):

  A list of JSON structures denoting the indivudal locations/cities to retreive and weather for
  * **name** : user friendl name of the location to use in Prometheus,
  * **service** : name of weather service to utilize (see list
  * **location_code** : the ID of the location for service lookup}

Sample Config.ini file (see [config.ini.example](config.ini.example))
```txt
[SETTINGS]
check_interval_minutes = 15
pushgateway = <URL to your Prometheus Pushgateway>
log_level = DEBUG

[API_KEYS]
openweathermap = <your key here>
weatherbit = <your key here>

[LOCATIONS]
location1 = {'name': 'Louisville, KY', 'service': 'openweathermap', 'location_code': '4299276'}
location2 = {'name': '<loation 2 name>', 'service': '<service name>', 'location_code': '<location code>'}
```

---

## Running

```shell
Python weather_monitor.py
```

or use the launch file to run in background (have to manually kill the process)

```shell
./launch_weathermonitor.sh
```
