#!/bin/bash
gunicorn app:app -k uvicorn.workers.UvicornWorker
