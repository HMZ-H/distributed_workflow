async def _get_token(client):
    """Helper: register a user and return the access token."""
    res = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    return res.json()["access_token"]


async def test_create_workflow(client):
    token = await _get_token(client)
    response = await client.post(
        "/workflows/",
        json={"name": "payment workflow", "description": "handles payments"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "payment workflow"
    assert data["status"] == "draft"


async def test_create_duplicate_workflow(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    await client.post(
        "/workflows/",
        json={"name": "payment workflow"},
        headers=headers,
    )
    response = await client.post(
        "/workflows/",
        json={"name": "payment workflow"},
        headers=headers,
    )
    assert response.status_code == 409


async def test_list_workflows(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    await client.post("/workflows/", json={"name": "wf1"}, headers=headers)
    await client.post("/workflows/", json={"name": "wf2"}, headers=headers)

    response = await client.get("/workflows/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_workflow(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = await client.post(
        "/workflows/", json={"name": "my wf"}, headers=headers
    )
    wf_id = create_res.json()["id"]

    response = await client.get(f"/workflows/{wf_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "my wf"


async def test_get_workflow_not_found(client):
    token = await _get_token(client)
    response = await client.get(
        "/workflows/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


async def test_update_workflow(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = await client.post(
        "/workflows/", json={"name": "old name"}, headers=headers
    )
    wf_id = create_res.json()["id"]

    response = await client.put(
        f"/workflows/{wf_id}",
        json={"name": "new name", "status": "active"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "new name"
    assert response.json()["status"] == "active"


async def test_delete_workflow(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = await client.post(
        "/workflows/", json={"name": "to delete"}, headers=headers
    )
    wf_id = create_res.json()["id"]

    response = await client.delete(f"/workflows/{wf_id}", headers=headers)
    assert response.status_code == 204

    response = await client.get(f"/workflows/{wf_id}", headers=headers)
    assert response.status_code == 404


async def test_workflow_requires_auth(client):
    response = await client.post("/workflows/", json={"name": "no auth"})
    assert response.status_code == 401
