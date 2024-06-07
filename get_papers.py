import feedparser
from datetime import datetime, timedelta, timezone
import pandas as pd


def extract_names(authors: list[dict]) -> list:
    """
    Extracts authors names from the paper.
    :param authors: authors names in a list of dict format
    :return: list of authors' first and last names
    """
    return [d['name'] for d in authors]


def get_arxiv_publications(start_date: str = None, max_results: int = 100) -> pd.DataFrame:
    """
    Returns arxiv publications in a pandas dataframe.
    :param start_date: date to start looking for the papers from. The function will return the publications
    from the last 2 weeks of this date. Default: today()
    :param max_results: max number of publications to returns from the arxiv api.
    """
    arxiv_categories = '(cat:cs+OR+cat:stat.CO+cat:stat.ME+cat:stat.ML+cat:stat.TH)'
    # arXiv categories available here: https://arxiv.org/category_taxonomy

    if not start_date:
        start_date = (datetime.now() - timedelta(weeks=2)).strftime('%Y-%m-%d')

    url_api = f'http://export.arxiv.org/api/query?search_query={arxiv_categories}+AND+submittedDate:[{start_date}+TO+9999999999999999]&start=0&max_results={max_results}'
    results = feedparser.parse(url_api)

    df = pd.DataFrame.from_dict(results.entries)
    df["published"] = df["published"].apply(lambda x: datetime.fromisoformat(x[:-1]).astimezone(timezone.utc).date())
    df["category"] = df["arxiv_primary_category"].apply(lambda x: x['term'])
    df['authors'] = df['authors'].apply(extract_names)
    df['title'] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
    columns = ['published', 'title', 'summary', 'authors', 'category']
    df = df[columns]
    df['source'] = 'arxiv'

    return df


def get_papers(source, date_start=None):
    if source == 'arxiv':
        publications = get_arxiv_publications(date_start)
    else:
        publications = pd.DataFrame()
    return publications
