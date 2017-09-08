# Tick stack 

Much of this is based on the instructions at: https://hub.docker.com/_/telegraf/

## Requirements

You'll need:
 * Docker
 * Docker Compose

## Running

To run Influxdb, Telegraf and an example Python app that uses a statsd client:

    tick$ ./run.sh # Ctrl-C to stop tailing combined logs
    tick$ curl localhost:5555
    tick$ docker exec -it tick_influx_1 influx
    > use telegraf
    > select * from "demo-counter"

## How it works

 * Standard Docker images for Influxdb and Telegraf are used
 * A lightly customised Telegraf config file was generated using `docker run --rm telegraf -sample-config > telegraf.conf`
 * The config file points Telegraf to `influxdb` and enables the statsd input plugin
 * A Python app runs on port 5555 that increments a counter called `demo-counter` on every request to `/`

And that's it.

