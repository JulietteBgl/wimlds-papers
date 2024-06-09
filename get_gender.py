import gender_guesser.detector as gender
gd = gender.Detector()


def rename_columns_title_case(col: str) -> str:
    return col.replace('_', ' ').title()


def is_main_author_female_(authors: list) -> bool:
    main_author_first_name = authors[0].split()[0]
    gender = gd.get_gender(main_author_first_name)
    if gender in ['female', 'mostly_female']:
        return True
    return False


def get_authors_info(authors: list) -> list:
    females_authors = list()
    for author in authors:
        first_name = author.split()[0]
        gender = gd.get_gender(first_name)
        if gender in ['female', 'mostly_female']:
            females_authors.append(author)
    return females_authors


def retrieve_women_papers(df):
    df = df.copy()
    df['is_main_author_female'] = df['authors'].apply(lambda raw: is_main_author_female_(raw))
    df = df[df['is_main_author_female']].drop(columns=['is_main_author_female'], inplace=False)
    df['females_authors'] = df['authors'].apply(lambda raw: get_authors_info(raw))
    df['female_ratio'] = df.apply(lambda x: len(x['females_authors']) / len(x['authors']) * 100 if len(x['authors']) > 0 else 0, axis=1)
    df['female_ratio'] = df['female_ratio'].apply(lambda x: f'{x:.2f}%')
    df.drop(columns=['summary', 'category', 'source'], inplace=True)
    df.columns = [rename_columns_title_case(col) for col in df.columns]
    return df.sort_values(by=['Published', 'Female Ratio'], ascending=False)
