#!/usr/bin/env bash
python -m waitress --listen=0.0.0.0:$PORT backend.app:app
