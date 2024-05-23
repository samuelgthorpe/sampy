PROJECT_NAME=sampy
MODULE_NAME=sampy

# build image locally for testing
# USAGE: make docker.build.local
docker.build.local:
	@docker build --tag ${PROJECT_NAME} --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} .

# run a set of build tests from within the container
# NOTE: requires docker.build called prior to build the image
# USAGE: make docker.test.build
docker.test.build:
	@docker run \
		-e AWS_PROFILE="dev" \
		-v ${HOME}/.aws:/root/.aws:ro \
		--entrypoint python3 ${PROJECT_NAME} ./tests/build/test_container_build.py

# run an interactive shell inside the local container image
# NOTE: requires docker.build called prior to build the image
# NOTE: -e flag below just an example of howw to pass globals
# USAGE: make docker.shell
docker.shell:
	@docker run -it \
		-e EXAMPLE_GLOBAL="dummy" \
		-v ${HOME}/.aws:/root/.aws:ro \
		--entrypoint /bin/bash ${PROJECT_NAME}

# locally run unit tests
# USAGE: make unit.test
unit.test:
	@pytest --cov=${MODULE_NAME} --cov-report html:tests/reports/coverage \
		--cov-report term tests/unit -W ignore::DeprecationWarning
	mv tests/reports/coverage/index.html tests/reports/coverage/COVERAGE.html

# locally run linting tests
# USAGE: make lint
lint.test:
	flake8 ${MODULE_NAME}
	flake8 tests
