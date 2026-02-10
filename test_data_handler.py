import os
import pytest
from data_handler import Data_handler


@pytest.fixture
def handler():
    filename = "test_users.json"

    # cleanup før test
    if os.path.exists(filename):
        os.remove(filename)

    dh = Data_handler(filename)
    yield dh

    # cleanup efter test
    if os.path.exists(filename):
        os.remove(filename)


def test_create_user(handler):
    user = handler.create_user(
        "John", "Doe", "Main Street", 10, "1234"
    )

    assert user.person_id == 0
    assert handler.get_number_of_users() == 1
    assert user.enabled is True


def test_get_user_by_id(handler):
    handler.create_user("John", "Doe", "Main Street", 10, "1234")

    user = handler.get_user_by_id(0)

    assert user is not None
    assert user.first_name == "John"


def test_disable_user(handler):
    handler.create_user("John", "Doe", "Main Street", 10, "1234")

    handler.disable_user(0)

    user = handler.get_user_by_id(0)
    assert user.enabled is False


def test_enable_user(handler):
    handler.create_user("John", "Doe", "Main Street", 10, "1234")
    handler.disable_user(0)

    handler.enable_user(0)

    assert handler.get_user_by_id(0).enabled is True


def test_delete_user(handler):
    handler.create_user("John", "Doe", "Main Street", 10, "1234")

    result = handler.delete_user(0)

    assert result is True
    assert handler.get_number_of_users() == 0


def test_delete_non_existing_user(handler):
    result = handler.delete_user(999)

    assert result is False
