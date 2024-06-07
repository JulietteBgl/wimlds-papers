import gradio as gr
from main import main

wimlds_presentation = (
    "WiMLDS aims to support and promote women and gender minorities who are practicing, studying, or have an "
    "interest in machine learning and data science.\n \n "
    "This tool helps you find the latest research papers in the field of data science that are written or co-written "
    "by at least one woman.")

with gr.Blocks() as papers:
    gr.Markdown(wimlds_presentation)
    inp = gr.Radio(choices=["arxiv", "hugging face (not available yet)"], value="arxiv", label="Source")
    btn = gr.Button("Search")
    out = gr.HTML()
    btn.click(fn=main, inputs=inp, outputs=out)

papers.launch(inbrowser=True)
