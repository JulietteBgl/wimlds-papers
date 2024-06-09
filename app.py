import gradio as gr
from main import main

wimlds_presentation = (
    "WiMLDS aims to support and promote women and gender minorities who are practicing, studying, or have an "
    "interest in machine learning and data science."
)

title_and_intro = (
    "# Women in Machine Learning and Data Science Researchers Project \n \n "
    "This tool helps you find the latest research papers in the field of data science that are written or co-written "
    "by at least one woman. \n \n "
)

with gr.Blocks() as papers:
    gr.Markdown(title_and_intro)
    inp = gr.Radio(choices=["Arxiv", "Hugging Face Selection"], value="Arxiv", label="Source")
    btn = gr.Button("Search")
    out = gr.HTML()
    gr.Markdown(wimlds_presentation)
    btn.click(fn=main, inputs=inp, outputs=out)

papers.launch(inbrowser=True)
