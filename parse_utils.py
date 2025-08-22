import pandas as pd

def dur_to_min(s: str | None) -> int | None:
    if not isinstance(s, str):
        return None
    s = s.replace("PT","")
    hours = 0
    mins = 0
    if "H" in s:
        parts = s.split("H")
        try:
            hours = int(parts[0])
        except Exception:
            hours = 0
        s = parts[1] if len(parts) > 1 else ""
    if "M" in s:
        sm = s.replace("M","")
        try:
            mins = int(sm)
        except Exception:
            mins = 0
    return hours*60 + mins

def parse_offers_v2(payload: dict, origin: str, dest: str, depart: str, ret: str | None):
    data = payload.get("data", [])
    dicts = payload.get("dictionaries", {})
    carriers = dicts.get("carriers", {})
    rows = []
    for item in data:
        price = float(item["price"]["grandTotal"])
        currency = item["price"]["currency"]

        # Outbound
        itin0 = item["itineraries"][0]
        out_dur = itin0.get("duration")
        out_dur_min = dur_to_min(out_dur)
        seg0 = itin0.get("segments", [])
        out_stops = max(0, len(seg0) - 1)
        out_carriers = ",".join({carriers.get(s["carrierCode"], s["carrierCode"]) for s in seg0})
        out_depart = seg0[0]["departure"]["at"] if seg0 else None
        out_arrive = seg0[-1]["arrival"]["at"] if seg0 else None

        # Return (optional)
        ret_dur = ret_dur_min = ret_stops = ret_carriers = ret_depart = ret_arrive = None
        if len(item["itineraries"]) > 1:
            itin1 = item["itineraries"][1]
            ret_dur = itin1.get("duration")
            ret_dur_min = dur_to_min(ret_dur)
            seg1 = itin1.get("segments", [])
            ret_stops = max(0, len(seg1) - 1)
            ret_carriers = ",".join({carriers.get(s["carrierCode"], s["carrierCode"]) for s in seg1})
            ret_depart = seg1[0]["departure"]["at"] if seg1 else None
            ret_arrive = seg1[-1]["arrival"]["at"] if seg1 else None

        rows.append({
            "route": f"{origin}-{dest}",
            "depart_date": depart,
            "return_date": ret,
            "price": price,
            "currency": currency,
            "out_duration": out_dur,
            "out_duration_min": out_dur_min,
            "out_stops": out_stops,
            "out_carriers": out_carriers,
            "out_depart": out_depart,
            "out_arrive": out_arrive,
            "ret_duration": ret_dur,
            "ret_duration_min": ret_dur_min,
            "ret_stops": ret_stops,
            "ret_carriers": ret_carriers,
            "ret_depart": ret_depart,
            "ret_arrive": ret_arrive
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["price","out_duration_min"], ascending=[True, True]).reset_index(drop=True)
        df["carrier_main"] = df["out_carriers"].fillna("").str.split(",").str[0]
        df["total_duration_min"] = df[["out_duration_min","ret_duration_min"]].sum(axis=1, min_count=1)
        df["price_per_hour"] = df["price"] / (df["total_duration_min"]/60.0)
    return df

def pareto_frontier(pdf, price_col="price", dur_col="total_duration_min"):
    pdf = pdf.dropna(subset=[price_col, dur_col]).sort_values([price_col, dur_col]).reset_index(drop=True)
    frontier_idx = []
    best_dur = float("inf")
    for i, row in pdf.iterrows():
        if row[dur_col] < best_dur:
            frontier_idx.append(i)
            best_dur = row[dur_col]
    return pdf.loc[frontier_idx]
