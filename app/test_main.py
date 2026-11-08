from main import app

client = app.test_client()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"


def test_ready():
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ready"


def test_index():
    r = client.get("/")
    assert r.status_code == 200
    body = r.get_json()
    assert body["service"] == "demo-app"
    assert body["status"] == "ok"
    # The version field is what lets us prove which build is running.
    assert body["version"]


def test_unknown_route_returns_404():
    r = client.get("/does-not-exist")
    assert r.status_code == 404
