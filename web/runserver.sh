#!/bin/bash
gunicorn -t 120 -w 4 -b 0.0.0.0:5000 app:app > output_full 2>&1
