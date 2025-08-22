from datetime import datetime
import os, requests

AMAD_TEST_BASE = "https://test.api.amadeus.com"
AMAD_PROD_BASE = "https://api.amadeus.com"

def get_token(base: str = AMAD_TEST_BASE) -> str:
    r = requests.post(
        f"{base}/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("AMADEUS_CLIENT_ID"),
            "client_secret": os.getenv("AMADEUS_CLIENT_SECRET"),
        },
        timeout=60
    )
    r.raise_for_status()
    return r.json()["access_token"]

def search_flights(token: str, origin: str, dest: str, depart: str, ret: str | None = None,
                   adults: int = 1, currency: str = "USD", max_results: int = 50,
                   base: str = AMAD_TEST_BASE) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": dest,
        "departureDate": depart,
        "adults": adults,
        "currencyCode": currency,
        "max": max_results,
    }
    if ret:
        params["returnDate"] = ret
    url = f"{base}/v2/shopping/flight-offers"
    r = requests.get(url, headers=headers, params=params, timeout=60)
    r.raise_for_status()
    return r.json()
