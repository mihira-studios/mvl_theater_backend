import os, requests, time

KC_BASE = os.getenv("KC_BASE", "http://10.100.1.30:8080")
MASTER_ADMIN_USER = os.getenv("KC_MASTER_ADMIN_USER", "admin")
MASTER_ADMIN_PASS = os.getenv("KC_MASTER_ADMIN_PASS", "secretadmin")

# tiny in-memory cache
_cached = {"token": None, "exp": 0}

def _realm_openid_config(base: str, realm: str):
    # try new-style first
    urls = [
        f"{base}/realms/{realm}/.well-known/openid-configuration",
        f"{base}/auth/realms/{realm}/.well-known/openid-configuration",
    ]
    last_err = None
    for u in urls:
        try:
            r = requests.get(u, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
    raise last_err

def get_master_admin_token() -> str:
    now = time.time()
    if _cached["token"] and now < _cached["exp"] - 5:
        return _cached["token"]

    cfg = _realm_openid_config(KC_BASE, "master")
    token_url = cfg["token_endpoint"]

    r = requests.post(
        token_url,
        data={
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": MASTER_ADMIN_USER,
            "password": MASTER_ADMIN_PASS,
        },
        timeout=10,
    )
    r.raise_for_status()
    payload = r.json()

    _cached["token"] = payload["access_token"]
    _cached["exp"] = now + payload.get("expires_in", 60)
    return _cached["token"]

def kc_admin_get(path: str):
    token = get_master_admin_token()
    r = requests.get(
        f"{KC_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()
