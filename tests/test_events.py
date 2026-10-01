from tests.helpers import auth, make_event

READ, WRITE = "security:read", "security:write"


def _post(client, event):
    return client.post("/events", json=event, headers=auth(WRITE))


def _findings(client, **params):
    resp = client.get("/findings", params=params, headers=auth(READ))
    assert resp.status_code == 200
    return resp.json()


def test_finding_event_creates_finding(client):
    event = make_event()
    resp = _post(client, event)
    assert resp.status_code == 202
    assert resp.json() == {"eventId": event["eventId"], "findingCreated": True}

    body = _findings(client)
    assert body["total"] == 1
    assert body["countsBySeverity"] == {"HIGH": 1}
    finding = body["findings"][0]
    assert finding["title"] == "Hardcoded password"
    assert finding["source"] == "ingest-studio"
    assert finding["reportedBy"] == "test-user"


def test_non_finding_event_is_stored_without_finding(client, store):
    resp = _post(client, make_event("Scan.Action", payload={"scanner": "trivy"}))
    assert resp.status_code == 202
    assert resp.json()["findingCreated"] is False
    assert store.event_count() == 1
    assert _findings(client)["total"] == 0


def test_duplicate_event_id_is_409(client):
    event = make_event()
    assert _post(client, event).status_code == 202
    assert _post(client, event).status_code == 409


def test_filter_by_severity_and_limit(client):
    _post(client, make_event(payload={"severity": "CRITICAL", "title": "a"}))
    _post(client, make_event(payload={"severity": "LOW", "title": "b"}))
    _post(client, make_event(payload={"severity": "LOW", "title": "c"}))

    assert _findings(client)["countsBySeverity"] == {"LOW": 2, "CRITICAL": 1}
    low = _findings(client, severity="LOW")
    assert low["total"] == 2 and low["countsBySeverity"] == {"LOW": 2}
    assert [f["title"] for f in low["findings"]] == ["c", "b"]  # newest first
    assert len(_findings(client, limit=1)["findings"]) == 1


def test_invalid_event_type_is_422(client):
    assert _post(client, make_event("not-an-event-type")).status_code == 422


def test_unknown_top_level_field_is_422(client):
    assert _post(client, make_event(unexpected="x")).status_code == 422


def test_metadata_extras_must_be_strings(client):
    assert _post(client, make_event(metadata={"schemaVersion": "v1.0", "n": 1})).status_code == 422
    assert _post(client, make_event(metadata={"schemaVersion": "v1.0", "env": "prod"})).status_code == 202


def test_finding_payload_with_bad_severity_is_422(client):
    resp = _post(client, make_event(payload={"severity": "SCARY", "title": "x"}))
    assert resp.status_code == 422
    assert "payload" in resp.json()["detail"]


def test_invalid_limit_is_422(client):
    assert client.get("/findings", params={"limit": 0}, headers=auth(READ)).status_code == 422
