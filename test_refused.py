# A second user with a username that is already taken is refused.
def test_duplicate_username_is_refused(api):
    user = {"username": "lab-" + __import__("uuid").uuid4().hex[:12], "password": "Pizza-2026"}
    first = api.post("/api/users", json=user)
    assert first.status_code == 201
    second = api.post("/api/users", json=user)
    assert second.status_code == 400
    assert second.json() == {"error": "username already taken"}


# Logging in with a wrong password is refused.
def test_wrong_password_is_refused(api):
    user = {"username": "lab-" + __import__("uuid").uuid4().hex[:12], "password": "Pizza-2026"}
    created = api.post("/api/users", json=user)
    assert created.status_code == 201
    wrong = {"username": user["username"], "password": "Wrong-2026"}
    res = api.post("/api/users/token/login", json=wrong)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# A user with an empty name is refused.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
