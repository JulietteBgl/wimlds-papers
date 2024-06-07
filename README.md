# Women in Machine Learning and Data Science Researchers Project
_Work in progress_

## Overview
The Women in Machine Learning and Data Science Researchers Project is a Python-based tool for retrieving the latest research papers from the Arxiv API, filtering papers based on the main author's gender, and computing the ratio of women authors per paper.
In future releases, the tool will also propose:
- the use of the Hugging Face Daily Papers API
- the use of Google scholars profile pictures for gender recognotion - currently, the gender is detected based on first name only)
- the Linkedin link of women scientists
- a short summary of their papers

## Features
- Retrieve latest research papers from Arxiv API.
- Extract author names from the retrieved papers.
- Filter papers based on the gender of the main author.
- Compute the ratio of women authors per paper.

## Requirements
- Python 3.x

## Installation
Clone the repository:
```git clone https://github.com/JulietteBgl/wilmds-papers.git```

Install the required libraries:
```pip install -r requirements.txt```

## Usage
Run the script app.py to start the Gradio application and retrieve the latest research papers published on Arxiv and 
written by women:

```python app.py```

## Acknowledgments
This project was inspired by the need to promote gender diversity in academic research.
Thanks to the Arxiv API for providing access to research papers.
