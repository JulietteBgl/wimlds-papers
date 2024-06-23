# Women in Machine Learning and Data Science Researchers Project

## Overview
The Women in Machine Learning and Data Science Researchers Project is a Python-based tool for retrieving the latest research papers from the Arxiv API as well as the Hugging Face Daily Papers selection, filtering papers based on the main author's gender, and computing the ratio of women authors per paper.

<img width="1570" alt="Screenshot 2024-06-09 at 17 51 34" src="https://github.com/JulietteBgl/wilmds-papers/assets/40431471/e5ca2469-1dbf-4cae-96bf-4a4034686b88">

In future releases, the tool will also propose:
- the use of Google scholars profile pictures for gender recognotion - currently, the gender is detected based on first name only)
- the Linkedin link of women scientists
- a short summary of their papers

## Features
- Retrieve latest research papers from Arxiv API and Hugging Face Daily Papers.
- Extract author's gender from the retrieved papers, based on their names or their avatar in their hugging face account.
- Filter papers based on the gender of the main author.
- Compute the ratio of women authors per paper.

## Requirements
- Python 3.x

## Installation
Clone the repository:
```git clone https://github.com/JulietteBgl/wimlds-papers.git```

Install the required libraries:
```pip install -r requirements.txt```

## Usage
Run the script app.py to start the Gradio application and retrieve the latest research papers published on Arxiv or selected by Hugging Face and 
written by women:

```python app.py```

## Acknowledgments
This project was inspired by the need to promote gender diversity in academic research.
Thanks to the Arxiv API for providing access to research papers.
