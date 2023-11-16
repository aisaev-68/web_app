#!/bin/bash
#alembic upgrade head
python 'app/init_db.py'
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1
