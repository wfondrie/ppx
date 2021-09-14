"""Test that the list_projects() functions work"""
import pytest
import ppx
import requests


def test_pride():
    """Test that we can get pride projects"""
    proj = ppx.pride.list_projects()
    assert len(proj) > 10000
    assert all((p.startswith("PXD") or p.startswith("PRD")) for p in proj)


def test_massive():
    """Test that we can get massive projects"""
    proj = ppx.massive.list_projects()
    assert len(proj) > 10000
    assert all((p.startswith("MSV") or p.startswith("RMS")) for p in proj)


def test_massive_fallback(no_requests):
    """Test that we can get massive projects"""
    proj = ppx.massive.list_projects()
    assert len(proj) > 10000
    assert all((p.startswith("MSV") or p.startswith("RMS")) for p in proj)


@pytest.fixture
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""

    def mock_get(*args, **kwargs):
        raise OSError

    monkeypatch.setattr(requests, "get", mock_get)
