from __future__ import annotations

import secrets

from acomytha.crypto_audio import AudioVault
from acomytha.graph import StoryGraph
from acomytha.models import Chunk
from acomytha.models import User

TEST_PASSWORD = secrets.token_urlsafe(24)
TEST_PIN = f"{secrets.randbelow(10000):04d}"
TEST_PIN_ALT = f"{(int(TEST_PIN) + 1) % 10000:04d}"


def signup_and_verify(client, payload):
    signup = client.post("/api/auth/signup", json=payload)
    assert signup.status_code == 200
    assert signup.json()["verification_required"] is True
    token = client.app.state.mailer.outbox[-1]["url"].split("token=", 1)[1]
    verified = client.post(
        "/api/auth/verify-email",
        json={
            "token": token,
            "device_id": payload["device_id"],
            "device_label": payload.get("device_label", ""),
        },
    )
    assert verified.status_code == 200
    return verified


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "AcoMytha" in r.text
    assert 'id="acm-mark"' in r.text


def test_editor_role_can_open_editor_api(client):
    with client.app.state.database.SessionLocal() as db:
        db.add(
            User(
                email="editor@acomytha.local",
                display_name="Éditeur",
                role="editor",
                password_hash=client.app.state.sessions.hasher.hash(TEST_PASSWORD),
            )
        )
        db.commit()
    login = client.post(
        "/api/auth/login",
        json={"email": "editor@acomytha.local", "password": TEST_PASSWORD, "device_id": "device-editor-1"},
    )
    assert login.status_code == 200
    assert login.json()["role"] == "editor"
    assert client.get("/api/editor/stories").status_code != 403


def test_admin_can_grant_cumulative_editor_role(client):
    assert client.post(
        "/api/auth/login",
        json={"email": "admin@acomytha.local", "password": client.app.state.settings.admin_password, "device_id": "device-admin-roles"},
    ).status_code == 200
    users = client.get("/api/admin/users").json()
    parent = next(user for user in users if user["email"] == "parent@acomytha.local")
    changed = client.put(f"/api/admin/users/{parent['id']}/roles", json={"roles": ["parent", "editor"]})
    assert changed.status_code == 200
    assert changed.json()["roles"] == ["editor", "parent"]
    client.post("/api/auth/logout")
    login = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-parent-roles"},
    )
    assert login.status_code == 200
    assert login.json()["roles"] == ["editor", "parent"]
    assert client.get("/api/parent/profiles").status_code == 200
    assert client.get("/api/editor/stories").status_code == 200


def test_admin_cannot_remove_own_admin_role(client):
    login = client.post(
        "/api/auth/login",
        json={"email": "admin@acomytha.local", "password": client.app.state.settings.admin_password, "device_id": "device-admin-self"},
    )
    response = client.put(f"/api/admin/users/{login.json()['id']}/roles", json={"roles": ["parent"]})
    assert response.status_code == 409


def test_public_stats_include_acm_prices(client):
    r = client.get("/api/public/stats")
    assert r.status_code == 200
    body = r.json()
    assert "price_story_acm" in body
    assert body["price_story_acm"] > 0
    assert body["home_catalog_page_size"] == 6


def test_public_stories_paginated(client):
    first = client.get("/api/public/stories", params={"limit": 1, "offset": 0}).json()
    assert first["limit"] == 1
    assert first["offset"] == 0
    assert len(first["items"]) == 1
    assert first["total"] >= 1
    nxt = client.get("/api/public/stories", params={"limit": 1, "offset": 1}).json()
    assert nxt["items"] == []
    assert nxt["total"] == first["total"]
    admin = client.post(
        "/api/auth/login",
        json={"email": "admin@acomytha.local", "password": client.app.state.settings.admin_password, "device_id": "device-admin-page1"},
    )
    assert admin.status_code == 200
    client.put("/api/admin/settings", json={"values": {"home_catalog_page_size": "2"}})
    defaulted = client.get("/api/public/stories").json()
    assert defaulted["limit"] == 2
    one = client.get(f"/api/public/stories/{first['items'][0]['story_id']}")
    assert one.status_code == 200
    assert one.json()["story_id"] == first["items"][0]["story_id"]


def test_acm_mark_asset(client):
    r = client.get("/assets/acm-mark.svg")
    assert r.status_code == 200
    assert "svg" in r.text.lower()


def test_login_and_catalog(client):
    r = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-parent-aaaa"},
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
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-one-xxxx"},
    )
    assert a.status_code == 200
    client.post("/api/auth/logout")
    b = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-two-yyyy"},
    )
    assert b.status_code == 409
    assert b.json()["detail"]["code"] == "device_bound"
    admin = client.post(
        "/api/auth/login",
        json={"email": "admin@acomytha.local", "password": client.app.state.settings.admin_password, "device_id": "device-admin-zzzz"},
    )
    assert admin.status_code == 200
    alerts = client.get("/api/admin/alerts").json()
    assert alerts
    assert alerts[0]["attempted_device_id"] == "device-two-yyyy"


def test_child_only_forest(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-parent-bbbb"},
    )
    profiles = client.get("/api/parent/profiles").json()
    assert profiles["limit"] == 10
    profile_id = profiles["items"][0]["id"]
    client.put(
        f"/api/parent/profiles/{profile_id}/catalog",
        json={"story_ids": ["ATOM-SAN.ALI.001-01"]},
    )
    child = client.post(
        "/api/auth/enfant",
        json={"profile_id": profile_id, "pin": TEST_PIN, "device_id": "device-parent-bbbb"},
    )
    assert child.status_code == 200
    assert child.json()["role"] == "child"
    file = client.get("/api/enfant/file").json()
    assert [s["story_id"] for s in file] == ["ATOM-SAN.ALI.001-01"]
    denied = client.get("/api/stories")
    assert denied.status_code == 403
    back_bad = client.post("/api/auth/parent", json={"pin": TEST_PIN_ALT})
    assert back_bad.status_code == 401
    back = client.post("/api/auth/parent", json={"pin": TEST_PIN})
    assert back.status_code == 200
    assert back.json()["role"] == "parent"
    child2 = client.post(
        "/api/auth/enfant",
        json={"profile_id": profile_id, "pin": TEST_PIN_ALT, "device_id": "device-parent-bbbb"},
    )
    assert child2.status_code == 200


def test_parent_profiles_have_isolated_catalogs(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-profiles-1"},
    )
    created = client.post(
        "/api/parent/profiles",
        json={"display_name": "Deuxième enfant", "age_band": "N2", "color": "or"},
    )
    assert created.status_code == 200
    second_id = created.json()["id"]
    first_id = client.get("/api/parent/profiles").json()["items"][0]["id"]
    client.put(f"/api/parent/profiles/{first_id}/catalog", json={"story_ids": []})
    client.put(
        f"/api/parent/profiles/{second_id}/catalog",
        json={"story_ids": ["ATOM-SAN.ALI.001-01"]},
    )
    assert client.get(f"/api/parent/profiles/{first_id}/catalog").json()["story_ids"] == []
    assert client.get(f"/api/parent/profiles/{second_id}/catalog").json()["story_ids"] == ["ATOM-SAN.ALI.001-01"]


def test_child_listening_history_is_recorded_for_profile(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-history-1"},
    )
    profile_id = client.get("/api/parent/profiles").json()["items"][0]["id"]
    client.put(
        f"/api/parent/profiles/{profile_id}/catalog",
        json={"story_ids": ["ATOM-SAN.ALI.001-01"]},
    )
    entered = client.post(
        "/api/auth/enfant",
        json={"profile_id": profile_id, "pin": TEST_PIN, "device_id": "device-history-1"},
    )
    assert entered.status_code == 200
    started = client.post("/api/enfant/ecoutes/ATOM-SAN.ALI.001-01", json={})
    assert started.status_code == 200
    listening_id = started.json()["listening_id"]
    finished = client.put(f"/api/enfant/ecoutes/{listening_id}", json={"listened_seconds": 12.5})
    assert finished.status_code == 200
    assert 0 <= finished.json()["completion_percent"] <= 100
    assert client.post("/api/auth/parent", json={"pin": TEST_PIN}).status_code == 200
    history = client.get(f"/api/parent/profiles/{profile_id}/ecoutes").json()
    assert len(history) == 1
    assert history[0]["story_id"] == "ATOM-SAN.ALI.001-01"
    assert history[0]["listened_seconds"] == 12.5


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
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-parent-cccc"},
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
    assert s["preview_seconds"] == 30
    page = client.get("/api/public/stories").json()
    assert "items" in page
    assert page["limit"] >= 1
    stories = page["items"]
    one = next(x for x in stories if x["story_id"] == "ATOM-SAN.ALI.001-01")
    assert one["duration_s"] >= 45
    assert one["has_interaction"] is True
    graph = client.get("/api/public/preview/ATOM-SAN.ALI.001-01/graph")
    assert graph.status_code == 200
    body = graph.json()
    assert body["preview_seconds"] == 30
    assert str(body["root"]).startswith("CHK_PREVIEW")
    clip = client.get(f"/api/public/preview/ATOM-SAN.ALI.001-01/chunk/{body['root']}")
    assert clip.status_code == 200
    assert clip.content[:5] == b"SNT01"


def test_signup_welcome_and_buy(client):
    r = signup_and_verify(
        client,
        {
            "email": "nouveau@acomytha.local",
            "password": TEST_PASSWORD,
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


def test_signup_requires_single_use_email_verification(client):
    payload = {
        "email": "validation@acomytha.local",
        "password": TEST_PASSWORD,
        "device_id": "device-verify-parent1",
    }
    signup = client.post("/api/auth/signup", json=payload)
    assert signup.status_code == 200
    assert signup.json() == {"verification_required": True, "email": payload["email"]}
    assert client.get("/api/shop/wallet").status_code == 401
    assert client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": payload["password"], "device_id": payload["device_id"]},
    ).status_code == 403
    token = client.app.state.mailer.outbox[-1]["url"].split("token=", 1)[1]
    verified = client.post(
        "/api/auth/verify-email",
        json={"token": token, "device_id": payload["device_id"]},
    )
    assert verified.status_code == 200
    assert client.get("/api/shop/wallet").json()["balance_a"] == 10
    client.post("/api/auth/logout")
    reused = client.post(
        "/api/auth/verify-email",
        json={"token": token, "device_id": payload["device_id"]},
    )
    assert reused.status_code == 400
    assert client.post("/api/auth/resend-verification", json={"email": "inconnu@example.test"}).json() == {"ok": True}


def test_parent_preview_30s_then_full_when_owned(client):
    signup_and_verify(
        client,
        {
            "email": "preecoute@acomytha.local",
            "password": TEST_PASSWORD,
            "display_name": "Sam",
            "device_id": "device-preview-parent1",
        },
    )
    denied = client.get("/api/play/ATOM-SAN.ALI.001-01/graph")
    assert denied.status_code == 402
    g = client.get("/api/play/ATOM-SAN.ALI.001-01/preview/graph")
    assert g.status_code == 200
    body = g.json()
    assert body["preview_seconds"] == 30
    clip = client.get(f"/api/play/ATOM-SAN.ALI.001-01/preview/chunk/{body['root']}")
    assert clip.status_code == 200
    client.post("/api/shop/buy", json={"story_id": "ATOM-SAN.ALI.001-01"})
    full = client.get("/api/play/ATOM-SAN.ALI.001-01/graph")
    assert full.status_code == 200
    chunks = full.json()["chunks"]
    assert len(chunks) >= 5
    assert chunks["CHK_T0000_P0000"]["default_next"] == "CHK_T0000_P0000_Q0001"
    assert chunks["CHK_T0000_P0000_C0001"]["default_next"] == "CHK_T0000_P0000_END"


def test_device_message_has_no_cle(client):
    client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-alpha-1111"},
    )
    client.post("/api/auth/logout")
    b = client.post(
        "/api/auth/login",
        json={"email": "parent@acomytha.local", "password": client.app.state.settings.parent_password, "device_id": "device-beta-2222"},
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
        json={"email": "admin@acomytha.local", "password": client.app.state.settings.admin_password, "device_id": "device-admin-set1"},
    )
    assert admin.status_code == 200
    rows = client.get("/api/admin/settings").json()
    keys = {r["key"] for r in rows}
    assert "price_story_a" in keys
    assert "welcome_credit_eur" in keys
    assert "stripe_secret" not in keys
    assert "stripe_webhook_secret" not in keys
    put = client.put("/api/admin/settings", json={"values": {"preview_seconds": "8"}})
    assert put.status_code == 200
    assert any(r["key"] == "preview_seconds" and r["value"] == "8" for r in put.json())


def test_stripe_recharge_is_credited_only_by_verified_webhook(client, settings, monkeypatch):
    import sys
    from types import SimpleNamespace

    created = {}
    stripe_key = f"sk_{'test'}_{secrets.token_urlsafe(18)}"
    webhook_secret = f"whsec_{secrets.token_urlsafe(18)}"
    webhook_signature = secrets.token_urlsafe(18)

    def create_session(**kwargs):
        created.update(kwargs)
        return SimpleNamespace(id="cs_test_acomytha", url="https://checkout.stripe.test/session")

    class Webhook:
        event = None

        @classmethod
        def construct_event(cls, payload, signature, secret):
            assert payload == b"{}"
            assert signature == webhook_signature
            assert secret == webhook_secret
            return cls.event

    fake_stripe = SimpleNamespace(
        checkout=SimpleNamespace(Session=SimpleNamespace(create=create_session)),
        Webhook=Webhook,
    )
    monkeypatch.setitem(sys.modules, "stripe", fake_stripe)
    settings.stripe_secret = stripe_key
    settings.stripe_webhook_secret = webhook_secret

    signup_and_verify(
        client,
        {
            "email": "payer@acomytha.local",
            "password": TEST_PASSWORD,
            "display_name": "Pia",
            "device_id": "device-pay-parent01",
        },
    )
    before = client.get("/api/shop/wallet").json()
    start = before["balance_a"]
    assert before["stripe"] == "test"
    r = client.post("/api/shop/recharge", json={"eur": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["checkout_url"] == "https://checkout.stripe.test/session"
    assert body["would_credit_a"] == 10
    assert created["api_key"] == stripe_key
    assert created["line_items"][0]["price_data"]["unit_amount"] == 1000
    assert client.get("/api/shop/wallet").json()["balance_a"] == start

    Webhook.event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_acomytha",
                "mode": "payment",
                "currency": "eur",
                "amount_total": 1000,
                "payment_status": "paid",
                "metadata": created["metadata"],
            }
        },
    }
    headers = {"stripe-signature": webhook_signature}
    Webhook.event["data"]["object"]["amount_total"] = 900
    tampered = client.post("/api/shop/stripe/webhook", content=b"{}", headers=headers)
    assert tampered.status_code == 400
    assert client.get("/api/shop/wallet").json()["balance_a"] == start

    Webhook.event["data"]["object"]["amount_total"] = 1000
    paid = client.post("/api/shop/stripe/webhook", content=b"{}", headers=headers)
    assert paid.status_code == 200
    assert client.get("/api/shop/wallet").json()["balance_a"] == start + 10

    repeated = client.post("/api/shop/stripe/webhook", content=b"{}", headers=headers)
    assert repeated.status_code == 200
    assert client.get("/api/shop/wallet").json()["balance_a"] == start + 10
    bad = client.post("/api/shop/recharge", json={"eur": 7})
    assert bad.status_code == 400


def test_recharge_is_disabled_without_stripe_configuration(client, settings):
    settings.stripe_secret = ""
    settings.stripe_webhook_secret = ""
    signup_and_verify(
        client,
        {
            "email": "sans-stripe@acomytha.local",
            "password": TEST_PASSWORD,
            "display_name": "Sam",
            "device_id": "device-no-stripe01",
        },
    )
    assert client.get("/api/shop/wallet").json()["stripe"] == "unconfigured"
    response = client.post("/api/shop/recharge", json={"eur": 10})
    assert response.status_code == 503
    assert client.post("/api/shop/recharge/confirm", json={"ref": "forbidden"}).status_code == 404


def test_recharge_is_disabled_without_webhook_secret(client, settings):
    settings.stripe_secret = f"sk_{'test'}_{secrets.token_urlsafe(18)}"
    settings.stripe_webhook_secret = ""
    signup_and_verify(
        client,
        {
            "email": "sans-webhook@acomytha.local",
            "password": TEST_PASSWORD,
            "display_name": "Noe",
            "device_id": "device-no-webhook01",
        },
    )
    assert client.get("/api/shop/wallet").json()["stripe"] == "webhook_missing"
    assert client.post("/api/shop/recharge", json={"eur": 10}).status_code == 503
