"""Test the utility functions"""
import pytest
import requests

import ppx


def test_listify():
    """Test that listify works"""
    assert ppx.utils.listify("ABC") == ["ABC"]
    assert ppx.utils.listify(["ABC"]) == ["ABC"]
    assert ppx.utils.listify(123) == [123]
    assert ppx.utils.listify((1, 2)) == [1, 2]


def test_test_url():
    """Test the URL test function"""
    massive = "http://www.google.com"
    assert ppx.utils.test_url(massive) == massive

    wrong = "http://willfondrie.com/blah"
    with pytest.raises(requests.HTTPError):
        ppx.utils.test_url(wrong)


def test_glob(tmp_path):
    """Test glob"""
    files = ["a.txt", "a.csv", "b/c.txt", "d/e.csv", ".ignore"]
    paths = []
    for fname in files:
        path = tmp_path / fname
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch()
        paths.append(path)

    dirs = [tmp_path / "b", tmp_path / "d"]

    assert ppx.utils.glob(tmp_path) == sorted(paths[:-1] + dirs)
    assert ppx.utils.glob(tmp_path, "a.*") == sorted(paths[:2])
    assert ppx.utils.glob(tmp_path, "**/*.txt") == sorted([paths[0], paths[2]])
    assert ppx.utils.glob(tmp_path, "**/*") == sorted(paths + dirs)
