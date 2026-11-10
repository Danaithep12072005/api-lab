# API lab results

ITDS362 — API Testing with pytest and requests

This repository contains the individual API testing lab for the QuickPizza API.

## Requirements

- Python 3.10 or newer
- Git
- curl
- Visual Studio Code or another editor with a terminal

## Install

On Windows PowerShell, from this repository folder:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the tests

```powershell
pytest -v
```

Create the self-contained HTML report required for submission:

```powershell
pytest -v --html=report.html --self-contained-html
```

## Test files

- `test_names.py` — list pizza names
- `test_tools.py` — list tools with a token
- `test_pizza.py` — vegetarian pizza and missing-token refusal
- `test_users.py` — new user has no ratings
- `test_ratings.py` — create, read, update and delete a rating
- `test_refused.py` — duplicate username, wrong password and empty username
- `test_excluded_tools.py` — excluded-tool partitions and the known defect
- `test_create_rating.py` — input space partitioning for POST ratings
- `test_update_rating.py` — boundary values for PUT ratings
- `test_rating_owner.py` — another user cannot read, change or delete a rating
- `conftest.py` — shared API session and independent data fixtures

## Input domain model for POST /api/ratings

The request has two body fields, `pizza_id` and `stars`, plus an Authorization token.

| Characteristic | Blocks | Values used | Test covering the block |
|---|---|---|---|
| C1: Value of stars | below 1 | 0 | `test_stars_out_of_range[0]` |
| C1: Value of stars | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| C1: Value of stars | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2: Type of stars | whole number (base) | 3 | `test_base_choice_is_saved` |
| C2: Type of stars | decimal | 3.5 | `test_decimal_stars_are_refused` |
| C2: Type of stars | text | "3" | `test_text_stars_are_refused` |
| C2: Type of stars | missing | no field | `test_missing_stars_are_refused` |
| C3: Pizza | exists (base) | fixture pizza | `test_base_choice_is_saved` |
| C3: Pizza | does not exist | 999999999 | `test_unknown_pizza_is_refused` |
| C4: Token | user's own (base) | `auth` fixture | `test_base_choice_is_saved` |
| C4: Token | none | no header | `test_missing_token_is_refused` |
| C4: Token | wrong length | short token | `test_short_token_is_refused` |

Base choice coverage needs 9 tests: 1 base test plus 2 other C1 blocks, 3 other C2 blocks, 1 other C3 block and 2 other C4 blocks. All combinations coverage needs 72 tests (3 × 4 × 2 × 3).

## Known defect

When all three tools are excluded, QuickPizza answers HTTP 500 with an empty body. The expected behavior stated in the lab is HTTP 400 with a JSON error message. The test remains marked as a strict xfail until the API is fixed.

## Safety

The tests create their own users and use the token returned by login for ratings. Do not use the public practice token to create, change or delete ratings. Do not commit real passwords, private tokens or credentials. The files `auth.txt` and `madeup.txt` are the practice files specified by the lab; the former contains only the published practice token and the latter contains a made-up token.
