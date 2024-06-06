#!/bin/bash

uvicorn fly_fastapi_example.main:app --host '::' --host 0.0.0.0 --port 8080 --reload