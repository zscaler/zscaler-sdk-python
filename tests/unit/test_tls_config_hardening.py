"""
Testing TLS settings provenance and token redaction in logs
"""

import logging
from unittest.mock import Mock, patch

import pytest

from zscaler.config.config_setter import ConfigSetter
from zscaler.logger import dump_request, dump_response
from zscaler.oneapi_client import Client
from zscaler.oneapi_http_client import HTTPClient

POISONED_YAML = """\
zscaler:
  client:
    proxy:
      host: 127.0.0.1
      port: 9999
    sslContext: false
"""

CREDENTIALS = {"clientId": "client-id", "clientSecret": "client-secret", "vanityDomain": "acme", "cloud": "beta"}


@pytest.fixture
def local_yaml(tmp_path):
    path = tmp_path / "zscaler.yaml"
    path.write_text(POISONED_YAML)
    missing = str(tmp_path / "absent.yaml")
    with patch("zscaler.config.config_setter._LOCAL_YAML_PATH", str(path)), patch(
        "zscaler.config.config_setter._GLOBAL_YAML_PATH", missing
    ):
        yield path


def test_yaml_ssl_context_is_ignored_and_proxy_is_kept(local_yaml, caplog):
    with caplog.at_level(logging.WARNING):
        config = ConfigSetter().get_config()

    assert "sslContext" not in config["client"]
    assert config["client"]["proxy"]["host"] == "127.0.0.1"
    assert f"Ignoring 'sslContext' in {local_yaml}" in caplog.text
    assert "Applying zscaler.yaml from the current working directory" in caplog.text


def test_yaml_cannot_disable_tls_verification(local_yaml):
    client = Client(dict(CREDENTIALS))

    assert client._request_executor._http_client._ssl_context is True


def test_constructor_ssl_context_is_honored_with_warning(local_yaml, caplog):
    with caplog.at_level(logging.WARNING):
        client = Client({**CREDENTIALS, "sslContext": False})

    assert client._request_executor._http_client._ssl_context is False
    assert "TLS certificate verification is disabled" in caplog.text


@pytest.mark.parametrize("ssl_context, expected", [(None, True), (True, True), ("/etc/ca.pem", "/etc/ca.pem")])
def test_http_client_ssl_context(ssl_context, expected):
    assert HTTPClient({"sslContext": ssl_context})._ssl_context == expected


def test_dump_request_redacts_api_token():
    logger = Mock()

    dump_request(
        logger, "https://csbapi.zscaler.net/zscsb/submit", "POST", None, {"api_token": "s3cr3t", "force": 1}, {}, "id"
    )

    logged = logger.info.call_args.args[0]
    assert "s3cr3t" not in logged
    assert "api_token=%2A%2A%2AREDACTED%2A%2A%2A" in logged
    assert "force=1" in logged


def test_dump_response_redacts_api_token():
    logger = Mock()
    resp = Mock(headers={}, text="")

    dump_response(logger, "https://csbapi.zscaler.net/zscsb/submit", "POST", resp, {"api_token": "s3cr3t"}, "id", 0)

    assert "s3cr3t" not in logger.info.call_args.args[0]
