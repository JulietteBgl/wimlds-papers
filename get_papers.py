import feedparser
from datetime import datetime, timezone
import pandas as pd
import requests

from constants import SOURCE_HF, SOURCE_ARXIV, MAX_RESULTS_ARXIV


def extract_authors_info(input_data) -> list or tuple[list, list]:
    """
    Extracts authors' names and avatar from the input data, which can be in different formats.
    :param input_data: a list of dicts containing authors' names, or a dict containing a list of authors.
    :return: list of authors' first and last names or a tuple of authors names and avatar in a list format
    """
    if isinstance(input_data, list):
        # Case for arXiv format
        return [author['name'] for author in input_data]
    elif isinstance(input_data, dict) and 'authors' in input_data:
        # Case for Hugging Face format
        names = [author['name'] for author in input_data['authors']]
        avatar_urls = [author.get('user', {}).get('avatarUrl', None) for author in input_data['authors']]
        return names, avatar_urls
    else:
        raise ValueError("Unsupported input format")


def get_arxiv_link(paper: dict) -> str:
    """
    Create the arxiv publication link based on the Arxiv publication id.
    :param paper: dict containing paper info.
    :return: link for the publication.
    """
    arxiv_id = paper['id']
    return f'https://arxiv.org/abs/{arxiv_id}'


def get_arxiv_publications(max_results: int = 100) -> pd.DataFrame:
    """
    Returns arxiv publications in a pandas dataframe.
    from the last 2 weeks of this date. Default: today()
    :param max_results: max number of publications to returns from the arxiv api.
    """
    arxiv_categories = '(cat:cs+OR+cat:stat.CO+cat:stat.ME+cat:stat.ML+cat:stat.TH)'
    # arXiv categories available here: https://arxiv.org/category_taxonomy

    url_api = f'http://export.arxiv.org/api/query?search_query={arxiv_categories}&start=0&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending'
    results = feedparser.parse(url_api)

    df = pd.DataFrame.from_dict(results.entries)
    df["published"] = df["published"].apply(lambda x: datetime.fromisoformat(x[:-1]).astimezone(timezone.utc).date())
    df["category"] = df["arxiv_primary_category"].apply(lambda x: x['term'])
    df['authors'] = df['authors'].apply(extract_authors_info)
    df['title'] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
    columns = ['published', 'title', 'summary', 'authors', 'category']
    df = df[columns]
    df['source'] = SOURCE_ARXIV
    df['avatar_url'] = None

    return df


def get_hf_publications() -> pd.DataFrame:
    """
    Returns hugging face publications in a pandas dataframe.
    """

    url_api = f'https://huggingface.co/api/daily_papers'
    results = requests.get(url_api)
    df = pd.DataFrame.from_dict(results.json())
    df["published"] = df["publishedAt"].apply(lambda x: datetime.fromisoformat(x[:-1]).astimezone(timezone.utc).date())
    df["category"] = SOURCE_HF
    df[['authors', 'avatar_url']] = df['paper'].apply(lambda x: pd.Series(extract_authors_info(x)))
    df['link'] = df['paper'].apply(get_arxiv_link)
    df['title'] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
    df['summary'] = df['paper'].apply(lambda paper: paper['summary'])
    columns = ['published', 'title', 'summary', 'authors', 'avatar_url', 'category']
    df = df[columns]
    df['source'] = SOURCE_HF

    return df


def get_papers(source):
    if source == SOURCE_ARXIV:
        return get_arxiv_publications(max_results=MAX_RESULTS_ARXIV)
    elif source == SOURCE_HF:
        return get_hf_publications()
    else:
        raise ValueError("Unknown Source")
