def test_login_refresh_and_logout(client, admin_user):
    login = client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "Password!123"},
    )
    assert login.status_code == 200
    payload = login.json()
    assert payload["access_token"]
    assert payload["refresh_token"]
    assert payload["session_id"]

    profile = client.get(
        "/api/subjects/me/profile",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )
    assert profile.status_code == 200
    assert profile.json()["email"] == admin_user.email

    refreshed = client.post("/api/auth/refresh", json={"refresh_token": payload["refresh_token"]})
    assert refreshed.status_code == 200
    refreshed_payload = refreshed.json()
    assert refreshed_payload["access_token"]
    assert refreshed_payload["refresh_token"] != payload["refresh_token"]

    logout = client.post("/api/auth/logout", json={"refresh_token": refreshed_payload["refresh_token"]})
    assert logout.status_code == 204

    revoked_profile = client.get(
        "/api/subjects/me/profile",
        headers={"Authorization": f"Bearer {refreshed_payload['access_token']}"},
    )
    assert revoked_profile.status_code == 401

    expired_refresh = client.post("/api/auth/refresh", json={"refresh_token": refreshed_payload["refresh_token"]})
    assert expired_refresh.status_code == 401
