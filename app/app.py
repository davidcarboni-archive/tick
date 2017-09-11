import logging
import b3
import sleuth
import os
import statsd
import random


from flask import Flask, request, redirect, render_template, jsonify


# Config

TELEGRAF = os.getenv("TELEGRAF") or "localhost"
statsd.Connection.set_defaults(host=TELEGRAF, port=8125)

# Logging

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("b3").setLevel(logging.INFO)
log = logging.getLogger(__name__)


# App

app = Flask("tick", static_folder='static', static_url_path='')


def count_request_frequency():
    log.info("Incrementing request_frequency")
    request_frequency = statsd.Counter('request_frequency')
    request_frequency += 1


def count_errors(response):
    log.info("Incrementing response_code_frequency: " + str(response.status_code))
    response_code_frequency = statsd.Counter('status_' + str(response.status_code))
    response_code_frequency += 1
    return response


app.before_request(b3.start_span)
app.before_request(count_request_frequency)
app.after_request(count_errors)
app.after_request(b3.end_span)


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
