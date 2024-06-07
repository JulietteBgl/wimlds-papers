from get_papers import get_papers
from get_gender import retrieve_women_papers


def get_html_table(df):
    # Convert DataFrame to an HTML table string
    return df.to_html(escape=False, index=False)


def main(source):
    """
    :param source: one of 'arxiv', 'hf'
    :return: html dataframe
    """
    arxiv_papers = get_papers(source)
    df = retrieve_women_papers(arxiv_papers)
    df_html = get_html_table(df)
    return df_html
