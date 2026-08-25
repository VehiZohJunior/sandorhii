from concurrent.futures import ThreadPoolExecutor

MANIPULATIVE_TEXT = (
    "URGENT !!! Partagez avant qu'il ne soit trop tard !!! Les experts "
    "affirment que TOUS les responsables sont corrompus et qu'ils nous "
    "cachent la verite."
)


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_submission_runs_analysis(client):
    res = client.post("/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"})
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "en_attente_validation"
    assert body["linguistic_analysis"]["score"] > 0
    assert len(body["linguistic_analysis"]["signals"]) > 0


def test_submission_too_short_is_rejected(client):
    res = client.post("/api/submissions", json={"texte": "trop court", "langue": "fr"})
    assert res.status_code == 422


def test_duplicate_submission_returns_same_analysis(client):
    first = client.post("/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"})
    second = client.post("/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"})
    assert first.json()["id"] == second.json()["id"]


def test_newsroom_requires_admin_password(client):
    res = client.get("/api/newsroom/queue")
    assert res.status_code == 401


def test_newsroom_rejects_wrong_password(client):
    res = client.get("/api/newsroom/queue", headers={"X-Admin-Password": "wrong"})
    assert res.status_code == 401


def test_full_publish_flow_appears_in_public_feed(client, admin_headers):
    submission = client.post(
        "/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"}
    ).json()

    queue = client.get("/api/newsroom/queue", headers=admin_headers).json()
    assert any(s["id"] == submission["id"] for s in queue)

    publish_res = client.post(
        f"/api/newsroom/{submission['id']}/publish",
        json={
            "verdict": "trompeur",
            "resume": "Ce message utilise plusieurs techniques de manipulation connues.",
            "auteur": "Equipe SandorHii",
        },
        headers=admin_headers,
    )
    assert publish_res.status_code == 200
    assert publish_res.json()["statut"] == "publie"

    feed = client.get("/api/feed").json()
    assert any(item["submission_id"] == submission["id"] for item in feed)

    detail = client.get(f"/api/feed/{submission['id']}")
    assert detail.status_code == 200
    assert detail.json()["fact_check"]["verdict"] == "trompeur"


def test_reject_removes_submission_from_queue(client, admin_headers):
    submission = client.post(
        "/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"}
    ).json()

    client.post(f"/api/newsroom/{submission['id']}/reject", headers=admin_headers)

    queue = client.get("/api/newsroom/queue", headers=admin_headers).json()
    assert not any(s["id"] == submission["id"] for s in queue)


def test_simultaneous_duplicate_submissions_do_not_crash(client):
    # Cas reel : un contenu viral soumis par deux personnes a quelques
    # millisecondes d'intervalle. Doit degrader proprement vers "meme
    # soumission pour les deux", jamais une erreur 500.
    def submit():
        return client.post(
            "/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"}
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: submit(), range(2)))

    for res in results:
        assert res.status_code == 200
    ids = {res.json()["id"] for res in results}
    assert len(ids) == 1


def test_submission_rate_limit_kicks_in(client):
    # 20/minute autorisees ; la 21e doit etre bloquee, pas planter.
    for i in range(20):
        res = client.post(
            "/api/submissions",
            json={"texte": f"{MANIPULATIVE_TEXT} variante numero {i}", "langue": "fr"},
        )
        assert res.status_code == 200
    blocked = client.post(
        "/api/submissions",
        json={"texte": f"{MANIPULATIVE_TEXT} variante numero 20", "langue": "fr"},
    )
    assert blocked.status_code == 429


def test_unpublished_submission_not_in_feed(client):
    submission = client.post(
        "/api/submissions", json={"texte": MANIPULATIVE_TEXT, "langue": "fr"}
    ).json()
    res = client.get(f"/api/feed/{submission['id']}")
    assert res.status_code == 404
