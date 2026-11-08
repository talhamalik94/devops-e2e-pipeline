from main import app

client = app.test_client()

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"

def test_ready():
    r = client.get("/ready")
    assert r.status_code == 200

def test_index():
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json()["service"] == "demo-app"
