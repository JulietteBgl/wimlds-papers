from get_papers import get_papers
from get_gender import retrieve_women_papers


def get_html_table(df):
    """
    Convert DataFrame to an HTML table string
    :param df: pandas dataframe to convert to html
    :return: a dataframe that can be used in a html webpage
    """
    return df.to_html(escape=False, index=False)


def main(source):
    """
    :param source: one of 'Arxiv', 'Hugging Face Selection'
    :return: html dataframe
    """
    papers = get_papers(source)
    df = retrieve_women_papers(papers)
    df_html = get_html_table(df)
    return df_html
