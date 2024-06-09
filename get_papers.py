import feedparser
from datetime import datetime, timedelta, timezone
import pandas as pd
import requests


def extract_names(input_data) -> list:
    """
    Extracts authors' names from the input data, which can be in different formats.
    :param input_data: a list of dicts containing authors' names or a dict containing a list of authors.
    :return: list of authors' first and last names
    """
    if isinstance(input_data, list):
        # Case for arXiv format
        return [author['name'] for author in input_data]
    elif isinstance(input_data, dict) and 'authors' in input_data:
        # Case for Hugging Face format
        return [author['name'] for author in input_data['authors']]
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
    df['source'] = 'Arxiv'

    return df


def get_hf_publications() -> pd.DataFrame:
    """
    Returns hugging face publications in a pandas dataframe.
    :param start_date: date to start looking for the papers from. The function will return the publications
    from the last 2 weeks of this date. Default: today()
    :param max_results: max number of publications to returns from the arxiv api.
    """

    url_api = f'https://huggingface.co/api/daily_papers'
    results = requests.get(url_api)
    df = pd.DataFrame.from_dict(results.json())
    df["published"] = df["publishedAt"].apply(lambda x: datetime.fromisoformat(x[:-1]).astimezone(timezone.utc).date())
    df["category"] = 'Hugging Face Selection'
    df['authors'] = df['paper'].apply(extract_names)
    df['link'] = df['paper'].apply(get_arxiv_link)
    df['title'] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
    df['summary'] = df['paper'].apply(lambda paper: paper['summary'])
    columns = ['published', 'title', 'summary', 'authors', 'category']
    df = df[columns]
    df['source'] = 'Hugging Face Selection'

    return df


def get_papers(source, date_start=None):
    if source == 'Arxiv':
        return get_arxiv_publications(date_start)
    elif source == 'Hugging Face Selection':
        return get_hf_publications()
    else:
        raise ValueError("Source unknown")
