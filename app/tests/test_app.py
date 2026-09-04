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
    back_bad = client.post("/api/auth/parent", json={"pin": "0000"})
    assert back_bad.status_code == 401
    back = client.post("/api/auth/parent", json={"pin": "2468"})
    assert back.status_code == 200
    assert back.json()["role"] == "parent"
    pin = client.put("/api/auth/pin", json={"current_pin": "2468", "new_pin": "1357"})
    assert pin.status_code == 200
    child2 = client.post("/api/auth/enfant", json={"pin": "2468", "device_id": "device-parent-bbbb"})
    assert child2.status_code == 401
    child3 = client.post("/api/auth/enfant", json={"pin": "1357", "device_id": "device-parent-bbbb"})
    assert child3.status_code == 200


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
    assert g.successor("CHK_T0000_P0000_C0001") == "CHK_T0000_P0000_END"
    assert g.successor("CHK_T0000_P0000_END") == "CHK_T0000_P0000_END_F0001"
    assert g.successor("CHK_T0000_P0000_END_F0001") is None
    assert g.default_path() == [c.chunk_id for c in chunks]


def test_graph_many_passages_linear():
    chunks = [
        Chunk(chunk_id="CHK_T0000_P0000", story_id="s", kind="passage_debut"),
        Chunk(chunk_id="CHK_T0000_P0001", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0000_P0002", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0000_P0003", story_id="s", kind="passage_fin"),
    ]
    g = StoryGraph(chunks)
    assert g.is_linear()
    assert g.default_path() == [
        "CHK_T0000_P0000",
        "CHK_T0000_P0001",
        "CHK_T0000_P0002",
        "CHK_T0000_P0003",
    ]


def test_graph_ramified_does_not_jump_sibling():
    chunks = [
        Chunk(chunk_id="CHK_T0000_P0000", story_id="s", kind="passage_debut"),
        Chunk(
            chunk_id="CHK_T0001_P0000",
            story_id="s",
            kind="transition_question",
            default_next="CHK_T0001_P0001",
            option_1_label="a",
            option_1_next="CHK_T0001_P0001",
            option_2_label="b",
            option_2_next="CHK_T0001_P0002",
        ),
        Chunk(chunk_id="CHK_T0001_P0001", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0001_P0001_Q0001", story_id="s", kind="passage_question", default_next="CHK_T0001_P0001_C0001"),
        Chunk(chunk_id="CHK_T0001_P0001_C0001", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0001_P0001_T0002_P0000", story_id="s", kind="transition_question", default_next="CHK_T0001_P0001_T0002_P0001"),
        Chunk(chunk_id="CHK_T0001_P0001_T0002_P0001", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0001_P0001_T0002_P0001_F0001", story_id="s", kind="passage_fin"),
        Chunk(chunk_id="CHK_T0001_P0002", story_id="s", kind="passage"),
        Chunk(chunk_id="CHK_T0001_P0002_F0001", story_id="s", kind="passage_fin"),
    ]
    g = StoryGraph(chunks)
    assert not g.is_linear()
    assert g.successor("CHK_T0000_P0000") == "CHK_T0001_P0000"
    assert g.successor("CHK_T0001_P0001") == "CHK_T0001_P0001_Q0001"
    assert g.successor("CHK_T0001_P0001_C0001") == "CHK_T0001_P0001_T0002_P0000"
    assert g.successor("CHK_T0001_P0001_T0002_P0001") == "CHK_T0001_P0001_T0002_P0001_F0001"
    path = g.default_path()
    assert "CHK_T0001_P0002" not in path
    assert path[-1] == "CHK_T0001_P0001_T0002_P0001_F0001"


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


def test_public_home_and_preview(client):
    s = client.get("/api/public/stats").json()
    assert s["stories"] >= 1
    assert s["preview_seconds"] == 10
    stories = client.get("/api/public/stories").json()
    one = next(x for x in stories if x["story_id"] == "ATOM-SAN.ALI.001-01")
    assert one["duration_s"] >= 45
    assert one["has_interaction"] is True
    graph = client.get("/api/public/preview/ATOM-SAN.ALI.001-01/graph")
    assert graph.status_code == 200
    assert graph.json()["preview_seconds"] == 10


def test_signup_welcome_and_buy(client):
    r = client.post(
        "/api/auth/signup",
        json={
            "email": "nouveau@acomytha.local",
            "password": "motdepasse",
            "display_name": "Léa",
            "device_id": "device-new-parent1",
        },
    )
    assert r.status_code == 200
    w = client.get("/api/shop/wallet").json()
    assert w["balance_a"] == 10
    buy = client.post("/api/shop/buy", json={"story_id": "ATOM-SAN.ALI.001-01"})
    assert buy.status_code == 200
    assert buy.json()["balance_a"] == 9
    assert "ATOM-SAN.ALI.001-01" in buy.json()["owned"]


def test_device_message_has_no_cle(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-alpha-1111"},
    )
    client.post("/api/auth/logout")
    b = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": "acomytha-parent", "device_id": "device-beta-2222"},
    )
    assert b.status_code == 409
    msg = b.json()["detail"]["message"]
    assert "clé" not in msg.lower()
    assert "appareil" in msg.lower()


def test_fx_and_admin_settings(client):
    from acomytha.commerce import eur_to_a

    assert eur_to_a(10) == 10
    assert eur_to_a(11) == round(11 * 1.25, 2)
    assert eur_to_a(200) == 1000
    admin = client.post(
        "/api/auth/login",
        json={"email": "admin@acomytha.local", "password": "acomytha-admin", "device_id": "device-admin-set1"},
    )
    assert admin.status_code == 200
    rows = client.get("/api/admin/settings").json()
    keys = {r["key"] for r in rows}
    assert "price_story_a" in keys
    assert "welcome_credit_eur" in keys
    put = client.put("/api/admin/settings", json={"values": {"preview_seconds": "8"}})
    assert put.status_code == 200
    assert any(r["key"] == "preview_seconds" and r["value"] == "8" for r in put.json())
