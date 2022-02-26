APP_VERSION   = $(shell cat VERSION)
COV_CONFIG    = ".coveragerc"
SOURCE_FOLDER = "src"
TESTS_FOLDER  = "tests"
TESTS_PARAMS  = "-p no:cacheprovider"


.PHONY: check
check:
	@echo "Checking code format"
	@black --check $(SOURCE_FOLDER) $(TESTS_FOLDER)
	@isort --check $(SOURCE_FOLDER) $(TESTS_FOLDER)
	@mypy --pretty $(SOURCE_FOLDER) $(TESTS_FOLDER)


.PHONY: install-dev
install-dev:
	@echo "Installing Development packages"
	@pip install -r reqs/requirements-all.txt
	@pre-commit install


.PHONY: test
test:
	@echo "Testing code"
	@pytest --cov-config=$(COV_CONFIG) --cov=$(SOURCE_FOLDER) "$(TESTS_PARAMS)"
