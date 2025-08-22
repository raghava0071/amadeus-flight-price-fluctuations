# ✈️ Flight Price & Timing Fluctuation Tracker (Amadeus)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](#)
[![Colab](https://img.shields.io/badge/Run%20in-Colab-orange)](https://colab.research.google.com/github/<raghava0071>/<amadeus-flight-price-fluctuations>/blob/main/notebooks/Amadeus_Flight_Price_Analysis.ipynb)

Analyze **flight price and timing fluctuations** with the Amadeus Self-Service APIs.
This repo includes a Colab-friendly notebook, modular Python helpers, and CI.
It’s designed to be **portfolio-quality** (clear structure, docs, tests, and badges).

## 🔥 Highlights
- End-to-end **Colab** notebook with charts and Pareto frontier (cheapest vs. fastest)
- Modular `src/` client for Amadeus (`get_token`, `search_flights`, `parse_offers_v2`)
- **No secrets committed** — use `.env` or environment variables
- Optional **daily snapshots** to track fluctuations over time
- Simple **pytest** for key utilities + GitHub Actions CI

## 🚀 Quickstart
1. **Create repo** on GitHub, clone locally.
2. Copy this project into your repo folder.
3. Create and fill **.env** (or set env vars in Colab):
   ```bash
   AMADEUS_CLIENT_ID=raghava0071
   AMADEUS_CLIENT_SECRET=amadeus-flight-price-fluctuations
   ```
4. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
5. Run a smoke test:
   ```bash
   python scripts/smoke_test.py --origin MIA --dest BOM --depart 2025-12-04 --return 2026-01-16
   ```
6. Open the notebook in **Colab** (badge above), run all cells.

> **Note:** In Amadeus, API Key = Client ID; API Secret = Client Secret.

## 🧭 Project Structure
```
.
├─ notebooks/
│  └─ Amadeus_Flight_Price_Analysis.ipynb   # Use/replace with your Colab notebook
├─ src/
│  ├─ amadeus_client.py                      # Token + search + parsing helpers
│  └─ parse_utils.py                         # Utilities (dur_to_min, Pareto, etc.)
├─ scripts/
│  ├─ smoke_test.py                          # Quick CLI to test a query
│  └─ track_snapshot.py                      # Append daily cheapest price to CSV
├─ tests/
│  └─ test_utils.py                          # Minimal unit tests
├─ .github/workflows/python-ci.yml           # CI: install + run tests
├─ .env.example
├─ requirements.txt
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ CITATION.cff
├─ LICENSE
└─ README.md
```

## 📊 What you’ll be able to show
- **134+ live offers** parsed into tidy DataFrames
- **Charts**: price histogram and price vs. duration
- **Pareto frontier** for cheapest vs. fastest
- **Carrier & stops** comparisons
- (Optional) **Time-series** of cheapest price for the route

## 🔑 Credentials
- Store secrets in `.env` (local) or **GitHub Actions → Secrets** (CI).
- In Colab, use:
  ```python
  import os
  os.environ["AMADEUS_CLIENT_ID"] = "YOUR_KEY"
  os.environ["AMADEUS_CLIENT_SECRET"] = "YOUR_SECRET"
  ```

## 🧪 Tests
```
pytest -q
```

## 🛠️ Make it “Top 1%” on GitHub
- Add a **social preview image** (repo Settings → Social preview).
- Pin the repo on your profile; add **topics**: `amadeus`, `flights`, `data-science`, `colab`.
- Create a **release** (v0.1.0) and add a short changelog in the README.
- Keep the README crisp with a **one-sentence value prop**, visuals, and the Colab badge.

## 📄 License
This project is MIT licensed. See **LICENSE**.

## 🙏 Acknowledgements
- Built with Amadeus Self-Service APIs.
