#!/usr/bin/env bash
export PATH="$PATH:/home/monitoring/.local/bin"
gunicorn -w 4 server:app --bind 0.0.0.0:8080 --statsd-host=localhost:8125 --statsd-prefix=mylibrary