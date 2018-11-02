from init_db import db_init
import os
import pytest


def generator():
    yield "127.0.0.1"
    yield "root"
    yield None
    yield "admin"
    yield "test@admin"
    yield "12345"


input_generator = generator()


@pytest.mark.first
def test_db_init(monkeypatch):
    os.system('mysql -u root -e "DROP DATABASE pytatki"')
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    db_init()
