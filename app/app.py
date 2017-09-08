import logging
import b3
import sleuth
import os
import statsd

from flask import Flask, request, redirect, render_template, jsonify


# Logging

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("b3").setLevel(logging.INFO)
log = logging.getLogger(__name__)

# App

app = Flask("tick", static_folder='static', static_url_path='')
app.before_request(b3.start_span)
app.after_request(b3.end_span)


@app.route('/')
def home():
    log.info("Incrementing counter..")
    client = statsd.StatsClient('telegraf', 8125)
    client.incr('demo-counter')
    log.info("Done.")
    return render_template('index.html')


if __name__ == "__main__":

    # Go!
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT") or "5000"),
        debug=True,
        threaded=True
    )
