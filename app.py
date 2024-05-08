import gradio as gr
from main import main


interface = gr.Interface(title='Women in Machine Learning and Data Science - Papers project',
                         fn=main,
                         inputs=gr.Radio(["arxiv", "hf"]),
                         outputs=gr.Dataframe()
                         )

interface.launch()
