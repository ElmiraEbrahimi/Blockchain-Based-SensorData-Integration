# IOT_Blockchain_Data_Integration

## Overview

The project simulates reading from a fake sensor (data from the [UMass Smart Dataset*- 2017 release](https://traces.cs.umass.edu/index.php/Smart/Smart), including a wide variety of data collected from real homes) and stores the values on a local blockchain. The user can set filters in a panel to determine what data from this sensor is within the normal range and should be stored in the blockchain, as well as filters for the speed at which data can be read from the sensor or sent to the blockchain.
[Project details](docs-img%2Fsensor_data_integration.pdf)

## Architecture
<p align="center">
  <img src="docs_imgs/architecture.png" width="600">
</p>

## Prerequisites

- Install [Python 3.11](https://www.python.org/downloads/)

- Install [Ganache](https://trufflesuite.com/ganache/). It can also be installed via [NPM](https://docs.nethereum.com/en/latest/ethereum-and-clients/ganache-cli/)

- Install [Mosquitto Broker](https://mosquitto.org/download/)

### Set virtual environment

`py -3.11 -m venv venv`

`.\venv\Scripts\activate`

### Install Requirements

`pip3 install -r requirements.txt`

### Django Server

`cd django_website`

`python manage.py makemigrations core`

`python manage.py migrate`

If you get an error, delete the `migrations` folder and `db.sqlite3` and repeat these steps again.

#### Create superuser

`python manage.py createsuperuser`

    Username: admin
    Password: admin
    Password (again): admin
    Bypass password validation and create user anyway? [y/N]:y

### Blockchain

`cd blockchain/`

#### Compile Solidity

`python compile_contract.py`

#### Deploy compiled contract

`python deploy.py`

#### Run event handler

`python event_handler.py`

## Run

To run the project, do the following steps in order.

- run mosquitto broker service on default `port 1883`

run the command prompt as an administrator and
navigate to your broker installation location

`net start mosquitto`

- run ganache on `localhost:8545`

- run Django server:

`cd django_website`

`python manage.py runserver`

 visit (http://localhost:8000/admin) to see the running server

- run `blockchain/event_handler.py` 

- run `mqtt_broker/subscriber.py` 

- run `mqtt_broker/publisher.py`