"""Test that the list_projects() functions work"""
import pytest
import ppx


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
