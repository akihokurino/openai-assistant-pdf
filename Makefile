SHELL := /bin/bash

venv:
	python3 -m venv venv

vendor:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

setup:
	source venv/bin/activate && python create-assistant.py

chat:
	source venv/bin/activate && python chat.py