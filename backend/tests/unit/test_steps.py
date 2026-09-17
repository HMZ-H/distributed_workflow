async def _get_token(client):
    res = await client.post(
        "/auth/register",
        json={"email": "step@example.com", "password": "testpassword"},
    )
    return res.json()["access_token"]


async def _create_workflow(client, headers):
    res = await client.post(
        "/workflows/",
        json={"name": "test workflow"},
        headers=headers,
    )
    return res.json()["id"]


async def test_create_step(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    response = await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "Run tests", "type": "script", "position": 0},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Run tests"
    assert data["type"] == "script"
    assert data["position"] == 0
    assert data["workflow_id"] == wf_id


async def test_create_duplicate_step(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "Run tests", "type": "script", "position": 0},
        headers=headers,
    )
    response = await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "Run tests", "type": "script", "position": 1},
        headers=headers,
    )
    assert response.status_code == 409


async def test_list_steps(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "Step 1", "type": "script", "position": 0},
        headers=headers,
    )
    await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "Step 2", "type": "http", "position": 1},
        headers=headers,
    )

    response = await client.get(f"/workflows/{wf_id}/steps/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_step(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    create_res = await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "My step", "type": "email", "position": 0},
        headers=headers,
    )
    step_id = create_res.json()["id"]

    response = await client.get(f"/workflows/{wf_id}/steps/{step_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "My step"


async def test_get_step_not_found(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    response = await client.get(
        f"/workflows/{wf_id}/steps/00000000-0000-0000-0000-000000000000",
        headers=headers,
    )
    assert response.status_code == 404


async def test_update_step(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    create_res = await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "Old name", "type": "script", "position": 0},
        headers=headers,
    )
    step_id = create_res.json()["id"]

    response = await client.put(
        f"/workflows/{wf_id}/steps/{step_id}",
        json={"name": "New name", "type": "http"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New name"
    assert response.json()["type"] == "http"


async def test_delete_step(client):
    token = await _get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    wf_id = await _create_workflow(client, headers)

    create_res = await client.post(
        f"/workflows/{wf_id}/steps/",
        json={"name": "To delete", "type": "script", "position": 0},
        headers=headers,
    )
    step_id = create_res.json()["id"]

    response = await client.delete(
        f"/workflows/{wf_id}/steps/{step_id}", headers=headers
    )
    assert response.status_code == 204

    response = await client.get(f"/workflows/{wf_id}/steps/{step_id}", headers=headers)
    assert response.status_code == 404


async def test_step_requires_auth(client):
    response = await client.post(
        "/workflows/00000000-0000-0000-0000-000000000000/steps/",
        json={"name": "No auth", "type": "script", "position": 0},
    )
    assert response.status_code == 401
