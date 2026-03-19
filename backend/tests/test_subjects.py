from app.db.session import SessionLocal
from app.models.entities import AuditLog


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_subject_crud_search_encounters_and_export(client, admin_token, subject):
    access = admin_token["access_token"]

    create = client.post(
        "/api/subjects",
        headers=_auth_headers(access),
        json={
            "first_name": "Avery",
            "middle_name": "B",
            "last_name": "Stone",
            "alias": "AS",
            "case_number": "CASE-2002",
            "intel_number": "INTEL-2002",
            "notes": "Created in test.",
        },
    )
    assert create.status_code == 201
    created_subject = create.json()
    assert created_subject["first_name"] == "Avery"

    search = client.get("/api/subjects", headers=_auth_headers(access), params={"q": "Avery"})
    assert search.status_code == 200
    assert any(item["first_name"] == "Avery" for item in search.json())

    update = client.patch(
        f"/api/subjects/{created_subject['id']}",
        headers=_auth_headers(access),
        json={"notes": "Updated note."},
    )
    assert update.status_code == 200
    assert update.json()["notes"] == "Updated note."

    encounter = client.post(
        f"/api/subjects/{subject.id}/encounters",
        headers=_auth_headers(access),
        json={
            "location": "North District",
            "summary": "Brief contact made.",
            "encountered_at": "2026-03-18T12:00:00Z",
        },
    )
    assert encounter.status_code == 201

    encounters = client.get(f"/api/subjects/{subject.id}/encounters", headers=_auth_headers(access))
    assert encounters.status_code == 200
    assert encounters.json()[0]["summary"] == "Brief contact made."

    photos = client.post(
        f"/api/photos/subjects/{subject.id}",
        headers=_auth_headers(access),
        files=[
            ("files", ("face1.jpg", b"fake-image-1", "image/jpeg")),
            ("files", ("face2.jpg", b"fake-image-2", "image/jpeg")),
        ],
    )
    assert photos.status_code == 201
    assert len(photos.json()["photos"]) == 2

    export = client.get(f"/api/subjects/{subject.id}/export", headers=_auth_headers(access))
    assert export.status_code == 200
    body = export.json()
    assert body["subject"]["id"] == subject.id
    assert len(body["encounters"]) == 1
    assert len(body["photos"]) == 2

    db = SessionLocal()
    try:
        audit_actions = [row.action for row in db.query(AuditLog).all()]
    finally:
        db.close()

    assert "create" in audit_actions
    assert "read" in audit_actions
    assert "update" in audit_actions
    assert "export" in audit_actions
