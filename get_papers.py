import feedparser
from datetime import datetime, timedelta, timezone
import pandas as pd

def extract_names(authors):
    return [d['name'] for d in authors]

def get_arxiv_publications(date_debut=None, max_results=100):
    arxiv_categories = '(cat:cs+OR+cat:stat.CO+cat:stat.ME+cat:stat.ML+cat:stat.TH)'  # https://arxiv.org/category_taxonomy

    if not date_debut:
        date_debut = (datetime.now() - timedelta(weeks=2)).strftime('%Y-%m-%d')

    url_api = f'http://export.arxiv.org/api/query?search_query={arxiv_categories}+AND+submittedDate:[{date_debut}+TO+9999999999999999]&start=0&max_results={max_results}'
    results = feedparser.parse(url_api)

    df = pd.DataFrame.from_dict(results.entries)
    df["published"] = df["published"].apply(lambda x: datetime.fromisoformat(x[:-1]).astimezone(timezone.utc).date())
    df["category"] = df["arxiv_primary_category"].apply(lambda x: x['term'])
    df['authors'] = df['authors'].apply(extract_names)
    columns = ['link', 'published', 'title', 'summary', 'authors', 'category']
    df = df[columns]

    return df


def get_papers(source, date_start=None):
    if source == 'arxiv':
        publications = get_arxiv_publications(date_start)
    return publications