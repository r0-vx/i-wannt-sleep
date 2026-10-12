from fastapi.testclient import TestClient


def test_create_and_owner_scoping(client: TestClient, headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/investigations",
        headers=headers,
        json={"text": "A sufficiently long factual statement for investigation."},
    )
    assert response.status_code == 201
    investigation_id = response.json()["id"]

    mine = client.get("/api/v1/investigations", headers=headers)
    assert mine.status_code == 200
    assert [item["id"] for item in mine.json()] == [investigation_id]

    other = client.get(
        f"/api/v1/investigations/{investigation_id}/status",
        headers={"X-ForwardCheck-Session": "another-session-00000000002"},
    )
    assert other.status_code == 404


def test_short_or_blank_text_is_rejected(client: TestClient, headers: dict[str, str]) -> None:
    response = client.post("/api/v1/investigations", headers=headers, json={"text": "too short"})
    assert response.status_code == 422


def test_missing_provider_configuration_fails_honestly(
    client: TestClient, headers: dict[str, str]
) -> None:
    created = client.post(
        "/api/v1/investigations",
        headers=headers,
        json={"text": "This message claims a public policy changed nationwide yesterday."},
    ).json()
    response = client.post(f"/api/v1/investigations/{created['id']}/verify", headers=headers)
    assert response.status_code == 200
    status_response = client.get(f"/api/v1/investigations/{created['id']}/status", headers=headers)
    assert status_response.json()["status"] == "failed"
    assert status_response.json()["failure_code"] == "provider_not_configured"
