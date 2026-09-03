from __future__ import annotations

from acomytha.crypto_audio import AudioVault
from acomytha.graph import StoryGraph
from acomytha.models import Chunk


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "AcoMytha" in r.text


def test_login_and_catalog(client):
    r = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-parent-aaaa"},
    )
    assert r.status_code == 200
    assert r.json()["role"] == "parent"
    stories = client.get("/api/stories").json()
    assert any(s["story_id"] == "ATOM-SAN.ALI.001-01" for s in stories)
    filtered = client.get("/api/stories", params={"age_band": "N1"}).json()
    assert filtered


def test_device_conflict_alerts_admin(client):
    a = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-one-xxxx"},
    )
    assert a.status_code == 200
    client.post("/api/auth/logout")
    b = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-two-yyyy"},
    )
    assert b.status_code == 409
    assert b.json()["detail"]["code"] == "device_bound"
    admin = client.post(
        "/api/auth/login",
        json={"email": "admin@acomytha.local", "password": "acomytha-admin", "device_id": "device-admin-zzzz"},
    )
    assert admin.status_code == 200
    alerts = client.get("/api/admin/alerts").json()
    assert alerts
    assert alerts[0]["attempted_device_id"] == "device-two-yyyy"


def test_child_only_forest(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-parent-bbbb"},
    )
    client.put("/api/parent/forest", json={"story_ids": ["ATOM-SAN.ALI.001-01"]})
    child = client.post("/api/auth/enfant", json={"pin": "2468", "device_id": "device-parent-bbbb"})
    assert child.status_code == 200
    assert child.json()["role"] == "child"
    file = client.get("/api/enfant/file").json()
    assert [s["story_id"] for s in file] == ["ATOM-SAN.ALI.001-01"]
    denied = client.get("/api/stories")
    assert denied.status_code == 403


def test_crypto_roundtrip(settings):
    vault = AudioVault(settings)
    mp3 = b"ID3fake-mp3-bytes-for-test"
    blob = vault.wrap("ATOM-SAN.ALI.001-01", "CHK_T0000_P0000", mp3)
    assert blob.startswith(b"SNT01")
    assert vault.unwrap(blob, "ATOM-SAN.ALI.001-01") == mp3


def test_graph_root_and_fin():
    chunks = [
        Chunk(chunk_id="CHK_T0000_P0000", story_id="s", kind="passage_debut"),
        Chunk(chunk_id="CHK_T0000_P0000_Q0001", story_id="s", kind="passage_question", default_next="CHK_T0000_P0000_C0001"),
        Chunk(chunk_id="CHK_T0000_P0000_C0001", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0000_P0000_END", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0000_P0000_END_F0001", story_id="s", kind="passage_fin"),
    ]
    g = StoryGraph(chunks)
    assert g.root == "CHK_T0000_P0000"
    assert g.successor("CHK_T0000_P0000") == "CHK_T0000_P0000_Q0001"
    assert g.successor("CHK_T0000_P0000_END_F0001") is None


def test_encrypted_chunk_endpoint(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-parent-cccc"},
    )
    graph = client.get("/api/play/ATOM-SAN.ALI.001-01/graph").json()
    assert graph["key"]
    assert graph["root"] == "CHK_T0000_P0000"
    blob = client.get("/api/play/ATOM-SAN.ALI.001-01/chunk/CHK_T0000_P0000")
    assert blob.status_code == 200
    assert blob.content[:5] == b"SNT01"
