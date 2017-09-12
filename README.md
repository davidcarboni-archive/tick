# Tick stack 

This repository demonstrates a Python/statsd Tick stack integration, using Docker Compose and official Docker library images.

A key point to be demonstrated here is that either or both of Telegraf and Influxdb can be taken down, without adversely affecting operation of the microservice.

Much of this is based on the instructions at: https://hub.docker.com/_/telegraf/

## Requirements

You'll need:
 * Docker
 * Docker Compose

## Running

To run Influxdb, Telegraf and an example Python app that uses a statsd client:

    tick$ ./run.sh # Ctrl-C to stop tailing combined logs
    tick$ curl localhost:5555
    tick$ docker exec -it tick_influxdb_1 influx
    > use telegraf
    > show measurements
    > select * from request_frequency
    > select * from status_418

To run the demo, you can execute:

    ./run.sh

To 'ping' the microservice, you can use a `while true`. This should show you 200 and 418 responses:

    while [ true ]; do curl -I -X GET localhost:5555 | grep HTTP; date; sleep 1; done

To 'tail' the metric, you can go for a `while true`:

    while [ true ]; do docker exec -it tick_influxdb_1 influx -database 'telegraf' -precision s -execute 'select * from status_418'; date; sleep 1; done

To test resilience of the application to the Tick stack being unavailable, try any combination of:

 * `docker-compose stop influxdb`
 * `docker-compose stop telegraf`
 * `docker-compose start influxdb`
 * `docker-compose start telegraf`

## How it works

 * Standard Docker images for Influxdb and Telegraf are used
 * A lightly customised Telegraf config file was created, based on the output of `docker run --rm telegraf -sample-config > telegraf.conf`
 * The config file points Telegraf to `influxdb` and enables the statsd input plugin
 * A Python app runs on port 5555 that increments counters called `request_frequency`, `status_200` and `status_418` on every request.

And that's it.

