# Project Variables
PROJECT_NAME := $(shell basename "$(PWD)")
PORT := 5000
DOCKER_PORT := 5000

# Make Comands
## clean: Clean application files.
clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete
	find . -type f -name '.pytest_*' -delete

## install-packages: Install requirement dependencies.
install-packages:
	pip install -r requirements/common.txt

## install-test-packages: Install test requirement dependencies.
install-test-packages:
	pip install -r requirements/test.txt

## test: Run unit tests.
test:
	py.test -vv

## run: Run API.
run:
	python manage.py run

## start: Clean, install, test and run API.
start: clean install-packages install-test-packages test run

## docker: Build and run API inside a docker container.
docker: docker-build docker-run

## docker-build: Build API inside a docker container.
docker-build:
	docker build -t $(PROJECT_NAME) .

## docker-run: Run API inside a docker container.
docker-run:
	docker run -d -p $(DOCKER_PORT):$(PORT) $(PROJECT_NAME)

## docker-stop: Stop the API container.
docker-stop:
	docker kill $(shell docker ps -q --filter ancestor=$(PROJECT_NAME))

## docker-compose: Run API inside a docker-compose.
docker-compose:
	docker-compose up -d

# Help
.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Choose a command run in "$(PROJECT_NAME)":"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo
