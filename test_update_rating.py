import pytest


# Boundary values 0, 1, 5 and 6 are checked, including that a refused update changes nothing.
@pytest.mark.parametrize(("stars", "expected_status"), [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_rating_boundary_values(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status
    if expected_status == 200:
        assert res.json()["stars"] == stars
    else:
        unchanged = api.get(path, headers=auth)
        assert unchanged.status_code == 200
        assert unchanged.json()["stars"] == 3
