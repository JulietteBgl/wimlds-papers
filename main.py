def main():
    arxiv_papers = get_papers('arxiv')
    df = retrieve_women_papers(arxiv_papers)
    return df


if __name__ == "__main__":
    from get_papers import get_papers
    from get_gender import retrieve_women_papers
    papers = main()