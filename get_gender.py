import gender_guesser.detector as gender
import logging
from deepface import DeepFace

from constants import SOURCE_HF, MAX_LINES_DF
from helpers import rename_columns_title_case

gd = gender.Detector()


def get_gender_from_name(first_name):
    """
    Get the gender inferred from the first name of the author.
    :param first_name: str
    :return: one of 'man', 'woman' or 'unknown'
    """
    try:
        author_gender = gd.get_gender(first_name)
        if author_gender in ['female', 'mostly_female']:
            gender = 'Woman'
        elif author_gender in ['male', 'mostly_male']:
            gender = 'Man'
        else:
            # case for androgynous names or unknown names
            gender = 'uUnknown'
        return gender

    except Exception as e:
        logging.exception("An error occurred during gender analysis.")
        return str(e)


def get_gender_from_picture(avatar_url):
    """
    Get the gender inferred from the picture url of the author.
    :param avatar_url: str
    :return: one of 'men', 'women' or 'unknown'
    """
    try:
        analysis = DeepFace.analyze(img_path=avatar_url, actions=['gender'], enforce_detection=False)
        return analysis[0]['dominant_gender']

    except Exception as e:
        logging.exception("An error occurred during gender analysis.")
        return str(e)


def is_main_author_female_(authors: list, source: str, hf_profile_url: list) -> list:
    #  Determine gender based on the first name using a gender detection library
    main_author_first_name = authors[0].split()[0]
    if get_gender_from_name(main_author_first_name) == 'Woman':
        return [True, 'name_analysis']
    # If gender is unknown or androgynous, and the source is Hugging Face with a valid profile URL,
    # attempt to predict gender using face recognition from the profile picture
    elif get_gender_from_name(main_author_first_name) == 'Unknown' and source == SOURCE_HF and hf_profile_url[0]:
        if hf_profile_url[0].startswith('http'):
            logging.info("Avatar url existing - trying face recognition")
            return [get_gender_from_picture(hf_profile_url[0]) == 'Woman', 'face_recognition']
    return [False, 'Unknown']


def get_authors_info(authors: list, source: str, profile_url: list) -> list:
    if profile_url is None:
        profile_url = [None] * len(authors)

    females_authors = list()
    for author, avatar in zip(authors, profile_url):
        first_name = author.split()[0]
        if get_gender_from_name(first_name) == 'Woman':
            females_authors.append(author)
        elif source == SOURCE_HF and avatar:
            if avatar.startswith('http') and get_gender_from_picture(avatar) == 'Woman':
                females_authors.append(author)
    return females_authors


def retrieve_women_papers(df):
    df = df.copy()
    df[['is_main_author_female', 'recognition_type']] = df.apply(
        lambda row: is_main_author_female_(row['authors'], row['source'], row['avatar_url']),
        axis=1, result_type='expand'
    )
    df = df[df['is_main_author_female']].drop(columns=['is_main_author_female'], inplace=False)
    df['females_authors'] = df.apply(lambda row: get_authors_info(row['authors'], row['source'], row['avatar_url']),
                                     axis=1)
    df['female_ratio'] = df.apply(lambda x: len(x['females_authors']) / len(x['authors']) * 100 if len(x['authors']) > 0 else 0, axis=1)
    df['female_ratio'] = df['female_ratio'].apply(lambda x: f'{x:.2f}%')
    df.drop(columns=['summary', 'category', 'source', 'avatar_url'], inplace=True)
    df.columns = [rename_columns_title_case(col) for col in df.columns]
    df = df[:MAX_LINES_DF]
    return df.sort_values(by=['Published', 'Female Ratio'], ascending=False)
