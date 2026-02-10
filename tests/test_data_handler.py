import pytest
import os
#from src.flat_file.data_handler import DataHandler, User
from flat_file.data_handler import DataHandler, User

# ────────────────────────────────────────────────
# Konfiguration
# ────────────────────────────────────────────────

TEST_DB_FILENAME = "db_flat_file_test.json"


def delete_test_db():
    if os.path.exists(TEST_DB_FILENAME):
        os.remove(TEST_DB_FILENAME)


@pytest.fixture(autouse=True)
def cleanup_test_file():
    """Sørger for at test-databasen slettes før og efter hver test."""
    delete_test_db()
    yield
    delete_test_db()


# ────────────────────────────────────────────────
# Tests
# ────────────────────────────────────────────────

def test_create_user_and_retrieve_by_id():
    # Given
    dh = DataHandler(TEST_DB_FILENAME)
    assert dh.get_number_of_users() == 0

    # When
    created = dh.create_user(
        first_name="Emma",
        last_name="Jensen",
        address="Solbækvej",
        street_number=42,
        password="hemmeligt123",
    )

    # Then
    assert dh.get_number_of_users() == 1
    assert created.person_id == 0

    fetched = dh.get_user_by_id(0)
    assert fetched is not None
    assert fetched.first_name == "Emma"
    assert fetched.last_name == "Jensen"
    assert fetched.address == "Solbækvej"
    assert fetched.street_number == 42
    assert fetched.password == "hemmeligt123"
    assert fetched.enabled is True


def test_multiple_users_get_sequential_ids():
    # Given
    dh = DataHandler(TEST_DB_FILENAME)

    # When
    dh.create_user("Anders", "Nielsen", "Hovedgaden", 5, "pw1")
    dh.create_user("Sara", "Larsen", "Parkvej", 17, "pw2")
    dh.create_user("Freja", "Møller", "Skovstien", 8, "pw3", enabled=False)

    # Then
    assert dh.get_number_of_users() == 3
    assert dh.get_user_by_id(0).first_name == "Anders"
    assert dh.get_user_by_id(1).first_name == "Sara"
    assert dh.get_user_by_id(2).first_name == "Freja"
    assert dh.get_user_by_id(2).enabled is False


def test_enable_disable_cycle():
    # Given
    dh = DataHandler(TEST_DB_FILENAME)
    dh.create_user("Test", "Bruger", "Testvej", 99, "testpw")
    dh.create_user("Anden", "Bruger", "Andenvej", 100, "andenpw")

    u0 = dh.get_user_by_id(0)
    u1 = dh.get_user_by_id(1)
    assert u0.enabled is True
    assert u1.enabled is True

    # When – disable første
    success = dh.disable_user(0)
    # Then
    assert success is True
    assert dh.get_user_by_id(0).enabled is False
    assert dh.get_user_by_id(1).enabled is True

    # When – disable anden, enable første igen
    dh.disable_user(1)
    dh.enable_user(0)

    # Then
    assert dh.get_user_by_id(0).enabled is True
    assert dh.get_user_by_id(1).enabled is False


def test_operations_on_non_existing_user():
    # Given
    dh = DataHandler(TEST_DB_FILENAME)

    # When + Then (skal ikke crashe)
    assert dh.enable_user(4711) is False
    assert dh.disable_user(4711) is False
    assert dh.get_user_by_id(4711) is None
    assert dh.get_number_of_users() == 0