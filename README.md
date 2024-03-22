# Sensor Data Management Service

## Overview

This service operates within an environment comprising several interconnected components, all orchestrated to manage data flows and interactions effectively. It collaborates with services that utilize Telegraf and InfluxDB, forming a cohesive ecosystem for data collection, storage, and retrieval.

## Services

The following services are integral to the functioning of this system:

- **InfluxDB**: A time-series database used for storing and managing time-stamped data. InfluxDB provides high performance and scalability, making it suitable for handling large volumes of time-series data.

- **Telegraf**: A plugin-driven server agent specifically configured as an MQTT consumer. Telegraf is responsible for subscribing to MQTT topics and consuming data messages published by IoT devices. It then processes and forwards this data to InfluxDB for storage and further analysis.

- **Flask Application**: This service, built using Flask, acts as a generic endpoint for querying InfluxDB. It facilitates the retrieval of time-series data based on specified parameters, providing flexibility and ease of access for users.

## Flask Application API

### Features

- **Generic InfluxDB Query Endpoint**: Allows users to query InfluxDB for time-series data using various parameters.
- **Flexible Query Parameters**: Users can specify parameters such as bucket name, time range, aggregation methods, time window, and filters through URL query parameters.
- **Error Handling**: Provides error handling for missing parameters, invalid queries, and unexpected exceptions.

### API Endpoint

- **Query InfluxDB Endpoint**:
  - Endpoint: `/records`
  - Method: GET
  - Description: A generic endpoint for querying InfluxDB. Users can specify parameters such as bucket name, start time, stop time, aggregation method, time window, and filters through URL query parameters.

### Query Parameters

Users can specify various parameters to tailor their queries to their specific needs. These parameters include:

- **bucket**: The name of the bucket containing the desired time series data.
- **start**: The earliest time to include in results (e.g., '-5m' or '2023-11-01T12:00:00Z').
- **stop**: The latest time to include in results (e.g., '-2m' or '2023-12-01T12:00:00Z').
- **method**: The name of a desired aggregation method to execute on the time series data (e.g., 'count').
- **window**: Time window to group the results based on time bounds (e.g., '1m').
- **numeric_records_only**: A flag indicating whether only numeric records are queried, supporting more aggregation methods. Set this if exclusively querying numeric records.
- ***filters**: Every other key-value query parameter is applied as a filter (e.g., device_serial=nodemcu-001) to the query.

## Docker Compose

The Docker Compose file defines services for InfluxDB, Telegraf, and the Flask application. It sets up the necessary networks and volumes for communication and data storage between services.

## Environment Variables

Ensure that the required environment variables are set in the `.env` file for proper configuration of InfluxDB credentials and other settings. A file `.env.example` is also provided to indicate the list of all required variables.
