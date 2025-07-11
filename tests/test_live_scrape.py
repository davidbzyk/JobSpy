import pandas as pd
import pytest

from jobspy import scrape_jobs


@pytest.mark.parametrize(
    "site",
    [
        "indeed",
        "linkedin",
        "zip_recruiter",
        "glassdoor",
        "google",
    ],
)
def test_live_scrape(site):
    df = scrape_jobs(
        site_name=site,
        search_term="software engineer",
        location="New York, NY",
        results_wanted=1,
        verbose=0,
    )
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 0
