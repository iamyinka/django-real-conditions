"""The env helpers decide whether the app starts at all, so test each failure mode."""

import pytest
from django.core.exceptions import ImproperlyConfigured

from config.env import env, env_bool, env_list


def test_required_variable_missing_raises_with_its_name(monkeypatch):
    monkeypatch.delenv("TELECOM_TEST_VAR", raising=False)
    with pytest.raises(ImproperlyConfigured, match="TELECOM_TEST_VAR"):
        env("TELECOM_TEST_VAR")


def test_empty_value_counts_as_unset(monkeypatch):
    monkeypatch.setenv("TELECOM_TEST_VAR", "")
    assert env("TELECOM_TEST_VAR", "fallback") == "fallback"


@pytest.mark.parametrize(
    "raw, expected",
    [("true", True), ("1", True), ("ON", True), ("false", False), ("0", False), ("No", False)],
)
def test_env_bool_accepts_common_spellings(monkeypatch, raw, expected):
    monkeypatch.setenv("TELECOM_TEST_VAR", raw)
    assert env_bool("TELECOM_TEST_VAR") is expected


def test_env_bool_rejects_typos_instead_of_treating_them_as_false(monkeypatch):
    # "ture" silently becoming False could turn DEBUG off, or a safety check off, by accident.
    monkeypatch.setenv("TELECOM_TEST_VAR", "ture")
    with pytest.raises(ImproperlyConfigured, match="true or false"):
        env_bool("TELECOM_TEST_VAR")


def test_env_list_splits_and_strips(monkeypatch):
    monkeypatch.setenv("TELECOM_TEST_VAR", " localhost, 127.0.0.1 ,,example.test ")
    assert env_list("TELECOM_TEST_VAR") == ["localhost", "127.0.0.1", "example.test"]
