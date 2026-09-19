import json
import sqlite3
import sys
import types

import pytest

import app


def test_get_user(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE users (id INTEGER, username TEXT)"
    )

    cursor.execute(
        "INSERT INTO users VALUES (1, 'savi')"
    )

    connection.commit()
    connection.close()

    result = app.get_user("savi")

    assert result == [(1, "savi")]


def test_ping_host(monkeypatch):
    class FakeResult:
        stdout = "PING SUCCESS"

    def fake_run(*args, **kwargs):
        assert kwargs["shell"] is False
        return FakeResult()

    monkeypatch.setattr(app.subprocess, "run", fake_run)

    result = app.ping_host("localhost")

    assert result == "PING SUCCESS"


def test_calculate_add():
    assert app.calculate(10, 5, "add") == 15


def test_calculate_subtract():
    assert app.calculate(10, 5, "subtract") == 5


def test_calculate_multiply():
    assert app.calculate(10, 5, "multiply") == 50


def test_calculate_divide():
    assert app.calculate(10, 5, "divide") == 2


def test_calculate_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        app.calculate(10, 0, "divide")


def test_calculate_invalid_operation():
    with pytest.raises(ValueError, match="Invalid operation"):
        app.calculate(10, 5, "invalid")


def test_load_user_data_string():
    data = '{"username": "savi", "role": "student"}'

    result = app.load_user_data(data)

    assert result["username"] == "savi"
    assert result["role"] == "student"


def test_load_user_data_bytes():
    data = b'{"username": "savi"}'

    result = app.load_user_data(data)

    assert result["username"] == "savi"


def test_hash_password():
    result = app.hash_password("password123")

    salt, password_hash = result.split(":")

    assert len(salt) == 32
    assert len(password_hash) == 64


def test_secure_request(monkeypatch):
    fake_requests = types.SimpleNamespace()

    class FakeResponse:
        text = "Example response"

    def fake_get(url, verify, timeout):
        assert url == "https://example.com"
        assert verify is True
        assert timeout == 10

        return FakeResponse()

    fake_requests.get = fake_get

    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    result = app.secure_request()

    assert result == "Example response"


def test_read_file_valid(monkeypatch):
    class FakeRequestedFile:
        def resolve(self):
            return self

        def is_file(self):
            return True

        def read_text(self, encoding):
            assert encoding == "utf-8"
            return "Hello from secure file"

        def relative_to(self, base):
            return self

    class FakeBaseDirectory:
        def resolve(self):
            return self

        def __truediv__(self, filename):
            assert filename == "test.txt"
            return FakeRequestedFile()

    class FakePath:
        def __init__(self, value):
            assert value == "/var/www"

        def resolve(self):
            return FakeBaseDirectory()

    monkeypatch.setattr(app, "Path", FakePath)

    result = app.read_file("test.txt")

    assert result == "Hello from secure file"


def test_read_file_path_traversal(monkeypatch):
    class FakeRequestedFile:
        def resolve(self):
            return self

        def relative_to(self, base):
            raise ValueError("outside base directory")

    class FakeBaseDirectory:
        def resolve(self):
            return self

        def __truediv__(self, filename):
            return FakeRequestedFile()

    class FakePath:
        def __init__(self, value):
            assert value == "/var/www"

        def resolve(self):
            return FakeBaseDirectory()

    monkeypatch.setattr(app, "Path", FakePath)

    with pytest.raises(ValueError, match="Invalid file path"):
        app.read_file("../secret.txt")


def test_read_file_missing(monkeypatch):
    class FakeRequestedFile:
        def resolve(self):
            return self

        def relative_to(self, base):
            return self

        def is_file(self):
            return False

    class FakeBaseDirectory:
        def resolve(self):
            return self

        def __truediv__(self, filename):
            return FakeRequestedFile()

    class FakePath:
        def __init__(self, value):
            assert value == "/var/www"

        def resolve(self):
            return FakeBaseDirectory()

    monkeypatch.setattr(app, "Path", FakePath)

    with pytest.raises(FileNotFoundError, match="File does not exist"):
        app.read_file("missing.txt")


def test_start_application():
    class FakeApp:
        def __init__(self):
            self.called = False

        def run(self, host, debug):
            self.called = True
            assert host == "0.0.0.0"
            assert debug is False

    fake_app = FakeApp()

    app.start_application(fake_app)

    assert fake_app.called is True


def test_generate_token():
    token = app.generate_token()

    assert len(token) == 64


def test_login():
    assert app.login("savi") is True
