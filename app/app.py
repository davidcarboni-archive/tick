import logging
import b3
import sleuth
import os
import statsd
import random


from flask import Flask, request, redirect, render_template, jsonify


# Config

STATSD = os.getenv("STATSD") or "localhost"
statsd.Connection.set_defaults(host=STATSD, port=8125)

# Logging

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("b3").setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# App

app = Flask("tick", static_folder='static', static_url_path='')


status_counters = {}
request_frequency = statsd.Counter('request_frequency')


def status_code_counter(response):
    global status_counters
    status_code = response.status_code
    if status_code not in status_counters:
        # We explicitly ignore race conditions on the basis this is 'good enough':
        status_counters[status_code] = statsd.Counter('status_' + str(response.status_code))
    return status_counters[status_code]


def count_request_frequency():
    log.info("Incrementing request_frequency")
    global request_frequency
    request_frequency += 1


def count_response_codes(response):
    log.info("Incrementing status code frequency: " + str(response.status_code))
    status_code_frequency = status_code_counter(response)
    status_code_frequency += 1
    return response


app.before_request(b3.start_span)
app.before_request(count_request_frequency)
app.after_request(b3.end_span)
app.after_request(count_response_codes)


@app.route('/')
def home():
    if random.random() < 0.3:
        response = jsonify({'status': 418})
        response.status_code = 418
        return response
    return render_template('index.html')


if __name__ == "__main__":

    # Go!
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT") or "5000"),
        debug=True,
        threaded=True
    )
