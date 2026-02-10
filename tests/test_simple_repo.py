# test_simple_repo.py
import pytest
from simple_repo import UserRepository

@pytest.fixture
def repo():
    return UserRepository()

def test_create_user_normalt(repo):
    user = repo.create("Lars Test", "lars@test.dk")
    assert user.id == 1
    assert user.name == "Lars Test"
    assert user.email == "lars@test.dk"
    assert user.active is True

def test_create_tomt_navn_giver_fejl(repo):
    with pytest.raises(ValueError, match="Navn må ikke være tomt"):
        repo.create("   ", "test@eksempel.dk")

def test_create_ugyldig_email_giver_fejl(repo):
    with pytest.raises(ValueError, match="Ugyldig email"):
        repo.create("Niels", "ikke-en-email")

def test_read_eksisterende_bruger(repo):
    created = repo.create("Mette", "mette@eksempel.dk")
    fundet = repo.read(created.id)
    assert fundet is not None
    assert fundet.name == "Mette"

def test_read_findes_ikke_returnerer_None(repo):
    assert repo.read(999) is None

def test_list_all_tom_i_starten(repo):
    assert repo.list_all() == []

def test_list_all_efter_to_brugere(repo):
    repo.create("Ida", "ida@eksempel.dk")
    repo.create("Jens", "jens@eksempel.dk")
    alle = repo.list_all()
    assert len(alle) == 2
    assert alle[0].name == "Ida"