COLOR_OK=\\x1b[0;32m
COLOR_NONE=\x1b[0m
COLOR_ERROR=\x1b[31;01m
COLOR_WARNING=\x1b[33;01m
COLOR_ZSCALER=\x1B[34;01m

VERSION=$(shell grep -E -o '(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?' ./zscaler/__init__.py)

help:
	@echo "$(COLOR_ZSCALER)"
	@echo "  ______              _           "
	@echo " |___  /             | |          "
	@echo "    / / ___  ___ __ _| | ___ _ __ "
	@echo "   / / / __|/ __/ _\` | |/ _ \ '__|"
	@echo "  / /__\__ \ (_| (_| | |  __/ |   "
	@echo " /_____|___/\___\__,_|_|\___|_|   "
	@echo "                                  "
	@echo "                                  "
	@echo "$(COLOR_NONE)"
	@echo "$(COLOR_OK)Zscaler SDK Python$(COLOR_NONE) version $(COLOR_WARNING)$(VERSION)$(COLOR_NONE)"
	@echo ""
	@echo "$(COLOR_WARNING)Usage:$(COLOR_NONE)"
	@echo "$(COLOR_OK)  make [command]$(COLOR_NONE)"
	@echo ""
	@echo "$(COLOR_WARNING)Available commands:$(COLOR_NONE)"
	@echo "$(COLOR_OK)  help$(COLOR_NONE)           Show this help message"
	@echo "$(COLOR_WARNING)clean$(COLOR_NONE)"
	@echo "$(COLOR_OK)  clean                  	Remove all build, test, coverage and Python artifacts$(COLOR_NONE)"
	@echo "$(COLOR_OK)  clean-build                   Remove build artifacts$(COLOR_NONE)"
	@echo "$(COLOR_OK)  clean-pyc                     Remove Python file artifacts$(COLOR_NONE)"
	@echo "$(COLOR_OK)  clean-test                    Remove test and coverage artifacts$(COLOR_NONE)"
	@echo "$(COLOR_WARNING)development$(COLOR_NONE)"
	@echo "$(COLOR_OK)  check-format                  Check code format/style with black$(COLOR_NONE)"
	@echo "$(COLOR_OK)  format                        Reformat code with black$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint                          Check style with flake8 for all packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zcc                      Check style with flake8 for zcc packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:ztw                      Check style with flake8 for ztw packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zdx                      Check style with flake8 for zdx packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zpa                      Check style with flake8 for zpa packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zia                      Check style with flake8 for zia packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zid                      Check style with flake8 for zid packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zins                     Check style with flake8 for zins packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zms                     Check style with flake8 for zms packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zbi                     Check style with flake8 for zbi packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zaiguard                 Check style with flake8 for zaiguard packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:ztb                      Check style with flake8 for ztb packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  lint:zwa                      Check style with flake8 for zwa packages$(COLOR_NONE)"
	@echo "$(COLOR_OK)  coverage                      Check code coverage quickly with the default Python$(COLOR_NONE)"
	@echo "$(COLOR_WARNING)test$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:all                      Run all tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:unit                     Run only unit tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:unit:coverage            Run unit tests with coverage report$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zcc          Run only zcc integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:ztw          Run only ztw integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zdx          Run only zdx integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zia          Run only zia integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zpa          Run only zpa integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zins         Run only zins integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zms         Run only zms integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zbi         Run only zbi integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:zaiguard     Run only zaiguard integration tests$(COLOR_NONE)"
	@echo "$(COLOR_OK)  test:integration:ztb          Run only ztb integration tests$(COLOR_NONE)"
	@echo "$(COLOR_WARNING)security$(COLOR_NONE)"
	@echo "$(COLOR_OK)  security-scan                 Run Trivy (vuln + secret scan, excludes local_dev/openapi)$(COLOR_NONE)"
	@echo "$(COLOR_WARNING)build$(COLOR_NONE)"
	@echo "$(COLOR_OK)  build:dist                    Build the distribution for publishing$(COLOR_NONE)"
	@echo "$(COLOR_WARNING)publish$(COLOR_NONE)"
	@echo "$(COLOR_OK)  publish:test                  Publish distribution to testpypi (Will ask for credentials)$(COLOR_NONE)"
	@echo "$(COLOR_OK)  publish:prod                  Publish distribution to pypi (Will ask for credentials)$(COLOR_NONE)"

clean: clean-build clean-pyc clean-test clean-docsrc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-docs:
	rm -fr docs/_build/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-docsrc:
	rm -fr docsrc/_build/

docs: clean-docsrc
	$(MAKE) -C docsrc html
	open docsrc/_build/html/index.html

lint:
	poetry run flake8 zscaler --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zcc:
	poetry run flake8 zscaler/zcc --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zcc --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:ztw:
	poetry run flake8 zscaler/ztw --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/ztw --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zdx:
	poetry run flake8 zscaler/zdx --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zdx --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zpa:
	poetry run flake8 zscaler/zpa --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zpa --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zia:
	poetry run flake8 zscaler/zia --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zia --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zid:
	poetry run flake8 zscaler/zid --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zid --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zins:
	poetry run flake8 zscaler/zins --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zins --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zms:
	poetry run flake8 zscaler/zms --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zms --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zbi:
	poetry run flake8 zscaler/zbi --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zbi --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zwa:
	poetry run flake8 zscaler/zwa --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zwa --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zeasm:
	poetry run flake8 zscaler/zeasm --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zeasm --count --select=E9,F63,F7,F82 --show-source --statistics

lint\:zaiguard:
	poetry run flake8 zscaler/zaiguard --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	poetry run flake8 zscaler/zaiguard --count --select=E9,F63,F7,F82 --show-source --statistics

format:
	poetry run black .

check-format:
	poetry run black --check --diff .

test\:unit:
	@echo "$(COLOR_ZSCALER)Running unit tests...$(COLOR_NONE)"
	poetry run pytest tests/unit --disable-warnings -v

test\:unit\:coverage:
	@echo "$(COLOR_ZSCALER)Running unit tests with coverage...$(COLOR_NONE)"
	poetry run pytest tests/unit --cov=zscaler --cov-report xml --cov-report term --junitxml=junit.xml -o junit_family=legacy --disable-warnings -v

test\:integration\:zcc:
	@echo "$(COLOR_ZSCALER)Running zcc integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zcc --disable-warnings

test\:integration\:ztw:
	@echo "$(COLOR_ZSCALER)Running ztw integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/ztw --disable-warnings

test\:integration\:zdx:
	@echo "$(COLOR_ZSCALER)Running zdx integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zdx --disable-warnings

test\:integration\:zpa:
	@echo "$(COLOR_ZSCALER)Running zpa integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zpa --disable-warnings

test\:integration\:zia:
	@echo "$(COLOR_ZSCALER)Running zia integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zia --disable-warnings

test\:integration\:zid:
	@echo "$(COLOR_ZSCALER)Running zid integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zid --disable-warnings

test\:integration\:zins:
	@echo "$(COLOR_ZSCALER)Running zins integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zins --disable-warnings

test\:integration\:zms:
	@echo "$(COLOR_ZSCALER)Running zms integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zms --disable-warnings

test\:integration\:zbi:
	@echo "$(COLOR_ZSCALER)Running zbi integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zbi --disable-warnings

test\:integration\:zwa:
	@echo "$(COLOR_ZSCALER)Running zwa integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zwa --disable-warnings

test\:integration\:zeasm:
	@echo "$(COLOR_ZSCALER)Running zeasm integration tests...$(COLOR_NONE)"
	poetry run pytest tests/integration/zeasm --disable-warnings

test-simple:
	poetry run pytest --disable-warnings

security-scan:
	@echo "$(COLOR_ZSCALER)Running Trivy security scan (vuln + secret)...$(COLOR_NONE)"
	trivy fs . --scanners vuln,secret --skip-version-check

coverage:
	poetry run pytest --cov=zscaler --cov-report xml --cov-report term

coverage\:zcc:
	poetry run pytest tests/integration/zcc -v --cov=zscaler/zcc --cov-report xml --cov-report term

coverage\:ztw:
	poetry run pytest tests/integration/ztw -v --cov=zscaler/ztw --cov-report xml --cov-report term

coverage\:zdx:
	poetry run pytest tests/integration/zdx -v --cov=zscaler/zdx --cov-report xml --cov-report term

coverage\:zia:
	poetry run pytest tests/integration/zia --cov=zscaler/zia --cov-report xml --cov-report term 

coverage\:zpa:
	poetry run pytest tests/integration/zpa --cov=zscaler/zpa --cov-report xml --cov-report term

coverage\:zid:
	poetry run pytest tests/integration/zid --cov=zscaler/zid --cov-report xml --cov-report term 

coverage\:zins:
	poetry run pytest tests/integration/zins --cov=zscaler/zins --cov-report xml --cov-report term

coverage\:zms:
	poetry run pytest tests/integration/zms --cov=zscaler/zms --cov-report xml --cov-report term

coverage\:zbi:
	poetry run pytest tests/integration/zbi --cov=zscaler/zbi --cov-report xml --cov-report term

coverage\:zeasm:
	poetry run pytest tests/integration/zeasm --cov=zscaler/zeasm --cov-report xml --cov-report term
# ==========================================
# VCR Testing Commands
# ==========================================
# Note: For recording, export credentials first:
#   export ZSCALER_CLIENT_ID="your_id"
#   export ZSCALER_CLIENT_SECRET="your_secret"
#   export ZSCALER_VANITY_DOMAIN="your_domain"
#   export ZPA_CUSTOMER_ID="your_customer_id"
#   export ZSCALER_CLOUD="production"
# ==========================================

# Run all tests with VCR cassettes (no credentials needed)
test\:vcr:
	@echo "$(COLOR_ZSCALER)Running tests with VCR cassettes (no credentials needed)...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/ -v --disable-warnings

# Run integration tests with VCR cassettes
test\:integration\:vcr:
	@echo "$(COLOR_ZSCALER)Running integration tests with VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration -v --disable-warnings

# Run integration tests with VCR and coverage
test\:integration\:vcr\:coverage:
	@echo "$(COLOR_ZSCALER)Running integration tests with VCR cassettes and coverage...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration --cov=zscaler --cov-report xml --cov-report term --disable-warnings -v

# Record new VCR cassettes for all integration tests (requires credentials)
test\:vcr\:record:
	@echo "$(COLOR_WARNING)Recording VCR cassettes (requires credentials)...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZIA
test\:vcr\:record\:zia:
	@echo "$(COLOR_ZSCALER)Recording ZIA VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zia --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZPA
test\:vcr\:record\:zpa:
	@echo "$(COLOR_ZSCALER)Recording ZPA VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zpa --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZCC
test\:vcr\:record\:zcc:
	@echo "$(COLOR_ZSCALER)Recording ZCC VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zcc --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZDX
test\:vcr\:record\:zdx:
	@echo "$(COLOR_ZSCALER)Recording ZDX VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zdx --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for Zid
test\:vcr\:record\:zid:
	@echo "$(COLOR_ZSCALER)Recording Zid VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zid --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for Z-Insights (zins)
test\:vcr\:record\:zins:
	@echo "$(COLOR_ZSCALER)Recording Z-Insights (zins) VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zins --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZMS
test\:vcr\:record\:zms:
	@echo "$(COLOR_ZSCALER)Recording ZMS VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zms --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZBI
test\:vcr\:record\:zbi:
	@echo "$(COLOR_ZSCALER)Recording ZBI VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zbi --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZTW
test\:vcr\:record\:ztw:
	@echo "$(COLOR_ZSCALER)Recording ZTW VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/ztw --record-mode=rewrite -v --disable-warnings

# Record VCR cassettes for ZEASM
test\:vcr\:record\:zeasm:
	@echo "$(COLOR_ZSCALER)Recording ZEASM VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration/zeasm --record-mode=rewrite -v --disable-warnings

# Playback VCR cassettes for ZIA (no credentials needed)
test\:vcr\:playback\:zia:
	@echo "$(COLOR_ZSCALER)Playing back ZIA VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zia -v --disable-warnings

# Playback VCR cassettes for ZPA (no credentials needed)
test\:vcr\:playback\:zpa:
	@echo "$(COLOR_ZSCALER)Playing back ZPA VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zpa -v --disable-warnings

# Playback VCR cassettes for ZCC (no credentials needed)
test\:vcr\:playback\:zcc:
	@echo "$(COLOR_ZSCALER)Playing back ZCC VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zcc -v --disable-warnings

# Playback VCR cassettes for ZDX (no credentials needed)
test\:vcr\:playback\:zdx:
	@echo "$(COLOR_ZSCALER)Playing back ZDX VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zdx -v --disable-warnings

# Playback VCR cassettes for Zid (no credentials needed)
test\:vcr\:playback\:zid:
	@echo "$(COLOR_ZSCALER)Playing back Zid VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zid -v --disable-warnings

# Playback VCR cassettes for Z-Insights (zins) (no credentials needed)
test\:vcr\:playback\:zins:
	@echo "$(COLOR_ZSCALER)Playing back Z-Insights (zins) VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zins -v --disable-warnings

# Playback VCR cassettes for ZMS (no credentials needed)
test\:vcr\:playback\:zms:
	@echo "$(COLOR_ZSCALER)Playing back ZMS VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zms -v --disable-warnings

# Playback VCR cassettes for ZBI (no credentials needed)
test\:vcr\:playback\:zbi:
	@echo "$(COLOR_ZSCALER)Playing back ZBI VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zbi -v --disable-warnings

# Playback VCR cassettes for ZTW (no credentials needed)
test\:vcr\:playback\:ztw:
	@echo "$(COLOR_ZSCALER)Playing back ZTW VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/ztw -v --disable-warnings

# Playback VCR cassettes for ZEASM (no credentials needed)
test\:vcr\:playback\:zeasm:
	@echo "$(COLOR_ZSCALER)Playing back ZEASM VCR cassettes...$(COLOR_NONE)"
	MOCK_TESTS=true poetry run pytest tests/integration/zeasm -v --disable-warnings

# Run integration tests against live API (no VCR)
test\:integration\:live:
	@echo "$(COLOR_WARNING)Running LIVE integration tests (requires credentials)...$(COLOR_NONE)"
	MOCK_TESTS=false poetry run pytest tests/integration --record-mode=none -v --disable-warnings

# ==========================================
# Sweep Commands
# ==========================================

sweep\:zia:
	@echo "$(COLOR_WARNING)WARNING: This will destroy infrastructure. Use only in development accounts.$(COLOR_NONE)"
	ZIA_SDK_TEST_SWEEP=true poetry run python tests/integration/zia/sweep/run_sweep.py --sweep

sweep\:zpa:
	@echo "$(COLOR_WARNING)WARNING: This will destroy infrastructure. Use only in development accounts.$(COLOR_NONE)"
	ZPA_SDK_TEST_SWEEP=true poetry run python tests/integration/zpa/sweep/run_sweep.py --sweep

sweep\:zid:
	@echo "$(COLOR_WARNING)WARNING: This will destroy infrastructure. Use only in development accounts.$(COLOR_NONE)"
	ZIDENTITY_SDK_TEST_SWEEP=true poetry run python tests/integration/zid/sweep/run_sweep.py --sweep

sweep\:zins:
	@echo "$(COLOR_WARNING)WARNING: This will destroy infrastructure. Use only in development accounts.$(COLOR_NONE)"
	ZINS_SDK_TEST_SWEEP=true poetry run python tests/integration/zins/sweep/run_sweep.py --sweep


build\:dist:
	python3 setup.py sdist bdist_wheel
	pip3 install dist/zscaler-sdk-python-${VERSION}.tar.gz
	ls -l dist

publish\:test:
	python3 -m twine upload --repository testpypi dist/*

publish\:prod:
	python3 -m twine upload dist/*

# Runtime-only dependencies
sync-deps:
	@poetry export --help >/dev/null 2>&1 || poetry self add poetry-plugin-export
	poetry export -f requirements.txt --without-hashes > requirements.txt

# Dev dependencies for contributors/CI
sync-dev-deps:
	@poetry export --help >/dev/null 2>&1 || poetry self add poetry-plugin-export
	poetry export -f requirements.txt --without-hashes --with dev > requirements-dev.txt


local-setup:
ifeq ($(wildcard ~/.local/bin/poetry),)
	@echo "installing poetry"
	curl -sSL https://install.python-poetry.org | python3 -
else
	@echo "poetry installation found"
endif
	~/.local/bin/poetry install

# ==========================================
# Security Scanning
# ==========================================

# Scan VCR cassettes for secrets (default)
security\:scan:
	@echo "$(COLOR_ZSCALER)Scanning for secrets in VCR cassettes...$(COLOR_NONE)"
	./scripts/check-secrets.sh

# Scan entire repository for secrets
security\:scan\:full:
	@echo "$(COLOR_ZSCALER)Scanning entire repository for secrets...$(COLOR_NONE)"
	./scripts/check-secrets.sh --full

# Install secret detection tools
security\:install:
	@echo "$(COLOR_ZSCALER)Installing secret detection tools...$(COLOR_NONE)"
	./scripts/check-secrets.sh --install

.PHONY: clean-pyc clean-build docs clean
