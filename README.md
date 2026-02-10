# Secure-Python-Password-Manager
A small cryptographically secure password manager written in python for use in the command line.

## What security does it use, how is it secure?
This password manager:
- Encrypts data using AES-256-GCM
- Uses a key derived from Argon2id using the master password and a randomly generated salt
- Encrypts data with a nonce in order to avoid relay attacks
- Uses atomic file writes to avoid data corruption

## Features:
- Store passwords for specific accounts/usernames
- Organize accounts under user-defined services
- Change passwords or service names
- Delete individual accounts or entire services
- Secure login via master password
- All operations performed from the command line

## Should I use this password manager?
This project is a hobby project made by a 15-year-old and is not intended for production use.
While it does have very good encryption, it has not been audited.
This project is also not very rich feature-wise.
**Use at your own risk**

## Getting Started
```bash
git clone https://github.com/TheAmazingCabbage/secure-python-password-manager
pip install cryptography argon2-cffi
python main.py
