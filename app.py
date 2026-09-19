import os
import sqlite3
import subprocess
import hashlib
import pickle
import yaml
import tempfile
import logging

# ============================================================
# SAST DEMONSTRATION PROJECT
# This file intentionally contains security vulnerabilities.
# ============================================================


# 1. HARDCODED PASSWORD
# Vulnerability: Password is directly written in source code.
DB_PASSWORD = "Admin@123"


# 2. HARDCODED SECRET KEY
# Vulnerability: Secret key should not be stored in source code.
SECRET_KEY = "my_super_secret_key_12345"


# 3. SQL INJECTION
# Vulnerability: User input is directly concatenated into SQL query.
def get_user(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"

    cursor.execute(query)
    return cursor.fetchall()


# 4. COMMAND INJECTION
# Vulnerability: User input is passed directly to a shell command.
def ping_host(host):
    command = "ping " + host
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout


# 5. INSECURE EVAL
# Vulnerability: eval() executes arbitrary Python expressions.
def calculate(expression):
    return eval(expression)


# 6. INSECURE DESERIALIZATION
# Vulnerability: pickle.loads() can execute malicious serialized code.
def load_user_data(data):
    return pickle.loads(data)


# 7. WEAK HASHING ALGORITHM
# Vulnerability: MD5 is cryptographically weak.
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# 8. SSL CERTIFICATE VERIFICATION DISABLED
# Vulnerability: Disabling certificate verification enables MITM attacks.
def insecure_request():
    import requests

    response = requests.get(
        "https://example.com",
        verify=False
    )

    return response.text


# 9. PATH TRAVERSAL
# Vulnerability: User-controlled filename can access unintended files.
def read_file(filename):
    with open("/var/www/" + filename, "r") as file:
        return file.read()


# 10. DEBUG MODE ENABLED
# Vulnerability: Debug mode may expose sensitive application details.
def start_application(app):
    app.run(
        host="0.0.0.0",
        debug=True
    )


# 11. INSECURE RANDOMNESS
# Vulnerability: Standard random generator is unsuitable for security tokens.
def generate_token():
    import random

    return str(random.randint(100000, 999999))


# 12. SENSITIVE INFORMATION IN LOGS
# Vulnerability: Password is written to application logs.
def login(username, password):
    logging.warning(
        "Login attempt: username=%s password=%s",
        username,
        password
    )

    return True


if __name__ == "__main__":
    print("SAST Vulnerability Demonstration Application")
