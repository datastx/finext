
WORKDIR = $(shell pwd)
VENV_DIR = $(WORKDIR)/.venv
VENV_BIN = $(VENV_DIR)/bin
DOCKER_FILES = $(WORKDIR)/docker
POSTGRES_CONTAINER_NAME=heroes-pg
POSTGRES_IMAGE_NAME=local-pg-build
POSTGRES_PORT=5432
POSTGRES_DOCKER_FILE = $(DOCKER_FILES)/Dockerfile.postgres


setup-local: clean-venv venv
	$(VENV_BIN)/pip install git+https://github.com/hunkim/streamlit-google-oauth
	cp -R -p -n example.env .env || echo ".env already exists"
	cp -R -p -n credentials_sample.json credentials.json || echo "credentials.json already exists"
	echo "fill out credentials.json with relevant credentials"
	echo "https://bridgedataoutput.com/myApplication/overview"
	

docker-build:
	docker build -f $(POSTGRES_DOCKER_FILE) -t ${POSTGRES_IMAGE_NAME} .

start-pg: docker-build
	docker run --name ${POSTGRES_CONTAINER_NAME} -d -p ${POSTGRES_PORT}:${POSTGRES_PORT} ${POSTGRES_IMAGE_NAME} 

stop-pg:
	docker stop ${POSTGRES_CONTAINER_NAME}

delete-all-containers:
	docker system prune --force

cleanup:
	make stop-pg
	make delete-all-containers


remove-branches:
	git branch | grep -v "main" | xargs git branch -D 

run-backend: start-pg
	uvicorn app.backend.main:app

run-backend-background: start-pg
	uvicorn app.backend.main:app -d

init-alembic:
	alembic init -t async migrations

run-migration:
	alembic revision -m “heroes”

alembic-head:
	alembic upgrade head

test: start-pg
	pytest --tb=auto 

run-frontend:
	scripts/run.sh

get-models:
	scripts/download_models.sh


run:
	python app/main.py -i "coke"


include Makefile.venv