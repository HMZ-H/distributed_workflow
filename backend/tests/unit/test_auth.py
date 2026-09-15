async def test_register_success(client):
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_register_duplicate_email(client):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "otherpassword"},
    )
    assert response.status_code == 409


async def test_register_invalid_email(client):
    response = await client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": "testpassword"},
    )
    assert response.status_code == 422


async def test_login_success(client):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client):
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


async def test_login_nonexistent_user(client):
    response = await client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "testpassword"},
    )
    assert response.status_code == 401


async def test_refresh_token(client):
    reg = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    refresh_token = reg.json()["refresh_token"]

    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_refresh_with_access_token_rejected(client):
    reg = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    access_token = reg.json()["access_token"]

    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": access_token},
    )
    assert response.status_code == 401
