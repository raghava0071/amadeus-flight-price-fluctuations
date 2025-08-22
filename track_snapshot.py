import os, argparse
import pandas as pd
from datetime import datetime
from src.amadeus_client import get_token, search_flights
from src.parse_utils import parse_offers_v2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--origin", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--depart", required=True)
    ap.add_argument("--return", dest="ret", required=False, default=None)
    ap.add_argument("--csv", required=True, help="Path to snapshot CSV")
    ap.add_argument("--env", choices=["test","prod"], default="prod")
    ap.add_argument("--currency", default="USD")
    args = ap.parse_args()

    base = "https://test.api.amadeus.com" if args.env == "test" else "https://api.amadeus.com"
    token = get_token(base=base)
    payload = search_flights(token, args.origin, args.dest, args.depart, args.ret, currency=args.currency, base=base)
    df = parse_offers_v2(payload, args.origin, args.dest, args.depart, args.ret)

    if df.empty:
        print("No offers returned; not appending.")
        return

    row = pd.DataFrame([{
        "timestamp_utc": datetime.utcnow().isoformat(),
        "origin": args.origin, "dest": args.dest,
        "depart": args.depart, "return": args.ret,
        "cheapest_price": float(df["price"].min())
    }])

    try:
        prev = pd.read_csv(args.csv)
        out = pd.concat([prev, row], ignore_index=True)
    except Exception:
        out = row

    out.to_csv(args.csv, index=False)
    print("Appended snapshot to", args.csv, " current min:", float(df["price"].min()))

if __name__ == "__main__":
    if not os.getenv("AMADEUS_CLIENT_ID") or not os.getenv("AMADEUS_CLIENT_SECRET"):
        print("Missing env vars: AMADEUS_CLIENT_ID / AMADEUS_CLIENT_SECRET")
        raise SystemExit(1)
    main()
