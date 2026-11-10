# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: A Strong Napoletana
- Step 0.12, results of the three runs without a session (optional): Not run; optional step omitted.
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2 and 3. The defect is revealed by the block that excludes all 3 tools.

## Defect report
- Title: Excluding all three pizza-cutting tools returns an internal server error
- Request: POST /api/pizza with Authorization for the test user's own token and JSON body `{"excludedTools":["Knife","Pizza cutter","Scissors"]}`.
- Expected result: HTTP 400 with a JSON error message because no pizza can satisfy the request.
- Actual result: HTTP 500 with an empty response body.
- Severity: Medium. The API returns an unexpected server error and gives the calling application no structured explanation.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: GET = 404, PUT = 400, DELETE = 400. Each attempt was refused (4xx), and the owner's rating remained unchanged.

## Part B

1. API tests can find failures in the communication between the client and server, and failures involving the real server, load balancer, or stored data. A unit test with stubs cannot verify those real integrations. Unit tests with stubs are still useful because they run quickly and isolate the logic of one function.
2. Each test creates its own user so that it does not share ratings with other students or tests. The public token is shared, so another person could change shared data while a test is running. For the shop or hotel project, tests should create and use only data belonging to their own test user or group.
3. The session keeps the AWSALB cookie. QuickPizza uses several servers behind a load balancer, and the cookie helps route requests to the same server. This matters because the server that created a user must also receive the login request; otherwise login can fail even when the credentials are correct.
4. The block that excludes all three tools revealed the defect. A 500 with an empty body is worse for an API client than a 400 with a message because it looks like a server failure and gives the client no useful structured reason. The test stays as a strict xfail so the known defect remains visible and the suite will alert us if the API is fixed.
5. Base choice coverage needs 9 tests: 1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9. All combinations coverage needs 3 × 4 × 2 × 3 = 72 tests.
6. The other user received 404 when reading, 400 when changing and 400 when deleting. The lab requires each attempt to be refused with a 4xx status, so all three observed codes meet that rule. The owner could still read the unchanged rating after each attempt.
7. The read-only request using the made-up 16-character token returned HTTP 200 and a ratings list. This is a defect because an unissued token should not grant access. On a real system, a stranger could read ratings data that should require a valid token.
8. An API test checks status codes, response fields and API behavior directly without the browser, so it can run faster and is easier to repeat. Only a test through the web pages can check what a user actually sees and interacts with on the screen.
