import os
import sqlite3
import subprocess
import hashlib
import secrets
import json
import logging
from pathlib import Path


# ============================================================
# SECURE SAST DEMONSTRATION PROJECT
# ============================================================


# 1. Hardcoded password - FIXED
DB_PASSWORD = os.environ.get("DB_PASSWORD")


# 2. Hardcoded secret - FIXED
SECRET_KEY = os.environ.get("SECRET_KEY")


# 3. SQL injection - FIXED
def get_user(username):
    connection = sqlite3.connect("users.db")

    try:
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"

        cursor.execute(query, (username,))

        return cursor.fetchall()

    finally:
        connection.close()


# 4. Command injection - FIXED
def ping_host(host):
    result = subprocess.run(
        ["ping", "-n", "4", host],
        shell=False,
        capture_output=True,
        text=True,
        check=False
    )

    return result.stdout


# 5. eval injection - FIXED
def calculate(a, b, operation):
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")

        return a / b

    raise ValueError("Invalid operation")


# 6. Insecure deserialization - FIXED
def load_user_data(data):
    if isinstance(data, bytes):
        data = data.decode("utf-8")

    return json.loads(data)


# 7. Weak hashing - FIXED
def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()


# 8. SSL verification disabled - FIXED
def secure_request():
    import requests

    response = requests.get(
        "https://example.com",
        verify=True,
        timeout=10
    )

    return response.text


# 9. Path traversal - FIXED
def read_file(filename):
    base_directory = Path("/var/www").resolve()

    requested_file = (base_directory / filename).resolve()

    try:
        requested_file.relative_to(base_directory)
    except ValueError as error:
        raise ValueError("Invalid file path") from error

    if not requested_file.is_file():
        raise FileNotFoundError("File does not exist")

    return requested_file.read_text(encoding="utf-8")


# 10. Debug mode - FIXED
def start_application(app):
    app.run(
        host="0.0.0.0",
        debug=False
    )


# 11. Insecure randomness - FIXED
def generate_token():
    return secrets.token_hex(32)


# 12. Sensitive information in logs - FIXED
def login(username, password):
    logging.info(
        "Login attempt for username=%s",
        username
    )

    return True


if __name__ == "__main__":
    print("SAST Secure Application")
