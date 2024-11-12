import gradio as gr
from helpers import *


with gr.Blocks() as demo:
    gr.Markdown("# 'LookOutAI': Find a target face in another image and choose to blur it, blur all other faces, or describe the target face in the second image")


    with gr.Row():
        with gr.Column(scale=3): 
            image1 = gr.Image(label = "Target Image", type = "filepath", height = 300, width = 500)
        with gr.Column(scale=3):
            image2 = gr.Image(label = "Candidate Image", type = "filepath", height = 300, width = 500)
        with gr.Column(scale = 1, min_width = 200):
            threshold = gr.Slider(
                label = "Similarity Threshold",
                minimum = 0.55,
                maximum = 1,
                value = 0.55,
                step = 0.01
            )
            
            with gr.Row():
                blur_target = gr.Button("Blur (Target)")
            with gr.Row():
                blur_others = gr.Button("Blur (Others)")
            with gr.Row():
                describe_target = gr.Button("Describe (Target)")
                

    with gr.Row():
        output1 = gr.Image(label = "Preview Target Image", height = 300, width = 500)
        output2 = gr.Image(label = "Preview Candidate Image", height = 300, width = 500)
        threshold_display = gr.Textbox(label = "Selected Threshold")


    blur_target.click(
        pass,
        inputs = [image1, image2, threshold],
        outputs = [output1, output2, threshold_display]
    )

    blur_others.click(
        pass,
        inputs = [image1, image2, threshold],
        outputs = [output1, output2, threshold_display]
    )

    describe_target.click(
        pass,
        inputs = [image1, image2, threshold],
        outputs = [output1, output2, threshold_display]
    )


if __name__ == "__main__":
    demo.launch()