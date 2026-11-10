import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Excluding all three tools should return a clear client error, not a server error.
@pytest.mark.xfail(reason="Defect 1: excluding all three tools returns HTTP 500 with an empty body instead of HTTP 400 with a JSON error", strict=True)
def test_all_tools_excluded_returns_client_error(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "no pizza can satisfy the excluded tools"}
