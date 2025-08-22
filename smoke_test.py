import os, argparse
from src.amadeus_client import get_token, search_flights
from src.parse_utils import parse_offers_v2, pareto_frontier

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--origin", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--depart", required=True)
    ap.add_argument("--return", dest="ret", required=False, default=None)
    ap.add_argument("--env", choices=["test","prod"], default="test")
    args = ap.parse_args()

    base = "https://test.api.amadeus.com" if args.env == "test" else "https://api.amadeus.com"
    token = get_token(base=base)
    payload = search_flights(token, args.origin, args.dest, args.depart, args.ret, base=base)
    df = parse_offers_v2(payload, args.origin, args.dest, args.depart, args.ret)

    print("Offers:", len(df))
    if len(df):
        front = pareto_frontier(df)
        print(front[["price","currency","total_duration_min","out_stops","carrier_main"]].head(10))

if __name__ == "__main__":
    if not os.getenv("AMADEUS_CLIENT_ID") or not os.getenv("AMADEUS_CLIENT_SECRET"):
        print("Missing env vars: AMADEUS_CLIENT_ID / AMADEUS_CLIENT_SECRET")
        raise SystemExit(1)
    main()
