from src.parse_utils import dur_to_min, pareto_frontier
import pandas as pd

def test_dur_to_min():
    assert dur_to_min("PT2H30M") == 150
    assert dur_to_min("PT12H") == 720
    assert dur_to_min("PT45M") == 45
    assert dur_to_min(None) is None

def test_pareto_frontier():
    df = pd.DataFrame({
        "price": [100, 120, 90, 110],
        "total_duration_min": [600, 500, 700, 400]
    })
    front = pareto_frontier(df)
    assert len(front) >= 1
