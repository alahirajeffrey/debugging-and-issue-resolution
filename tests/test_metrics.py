## SHOULD PASS: test to ensure total http request is in metrics response
def test_http_request_total(client):
    response = client.get("/metrics")
    assert b"http_requests_total" in response.data


## SHOULD PASS: test to ensure http request latency in seconds is in metrics response
def test_http_request_latency_seconds(client):
    response = client.get("/metrics")
    assert b"http_request_latency_seconds" in response.data


## SHOULD PASS: test to ensure total requests per second is in metrics response
def test_requests_per_second(client):
    response = client.get("/metrics")
    assert b"http_requests_per_second" in response.data


## SHOULD PASS: test to ensure metrics endpoint returns a 200 response code
def test_metrics_include_status_codes(client):
    response = client.get("/metrics")
    assert response.status_code == 200


## SHOULD FAIL: test to ensure http request per hour is not in metrics response
def test_http_request_per_hour(client):
    response = client.get("/metrics")
    assert b"http_request_per_hour" in response.data
