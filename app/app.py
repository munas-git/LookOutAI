# handling import path issues.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from helpers.FaceOps import *
from helpers.MultiModalAIOps import *


# all button operations pre-processing
def blur_target_actions(target_img, candidate_img, threshold):
    try:
    
        # extracting faces info
        target_img_details = face_detector(target_img)
        candidate_img_details = face_detector(candidate_img)

        # creating bounding box around detected target face
        target_bb_img = draw_bb(target_img, target_img_details.get("face_locations"))
        
        # checking for most similar face.
        best_match_details = target_candidates_compare(target_img_details.get("face_embeddings"), candidate_img_details.get("face_embeddings"), True, threshold)
        best_match_score = best_match_details.get("best_sim_score")
        target_match_loc = candidate_img_details.get("face_locations")[best_match_details.get("best_sim_score_index")]

        # bluring target face
        target_match_loc_array = [target_match_loc] # converting location tuple to list.... might handle this in function later
        blured_image = blur_regions(candidate_img, target_match_loc_array, 1.0)

        threshold_details = f"Selected Threshold: {threshold}\nFace Similarity Score: {100 * best_match_score:.2f}%"
        return target_bb_img, blured_image, threshold_details
    
    except Exception:
        message = f"""ERROR!!!: A 'single' target face has not been found at threshold value {threshold}. Kindly ensure you have uploaded a "target" image with only one indiidual and a clear "candidate image" as well.\
            \n\nIf you have already done so, try reducing the "Minimum Similarity Threshold" """
        return target_bb_img, candidate_img, message


def blur_others_actions(target_img, candidate_img, threshold):
    try:
        # extracting faces info
        target_img_details = face_detector(target_img)
        candidate_img_details = face_detector(candidate_img)

        # creating bounding box around detected target face
        target_bb_img = draw_bb(target_img, target_img_details.get("face_locations"))

        # checking for most similar face.
        best_match_details = target_candidates_compare(target_img_details.get("face_embeddings"), candidate_img_details.get("face_embeddings"), False, threshold)
        best_match_score = best_match_details.get("best_sim_score")
        all_similarity_scores = np.array(best_match_details.get("sim_scores"))

        # removing most similar face index
        indices = np.arange(all_similarity_scores.shape[0])
        other_faces_indices = indices[indices != best_match_details.get("best_sim_score_index")]

        # every other face's location
        other_faces_loc_array = np.array(candidate_img_details.get("face_locations"))[other_faces_indices]
        
        # bluring every other face except target face
        blured_image = blur_regions(candidate_img, other_faces_loc_array, 1.0)

        threshold_details = f"Selected Threshold: {threshold}\nFace Similarity Score: {100 * best_match_score:.2f}%"
        return target_bb_img, blured_image, threshold_details
    
    except Exception:
        message = f"""ERROR!!!: A 'single' target face has not been found at threshold value {threshold}. Kindly ensure you have uploaded a "target" image with only one indiidual and a clear "candidate image" as well.\
            \n\nIf you have already done so, try reducing the "Minimum Similarity Threshold" """
        return target_bb_img, candidate_img, message


def describe_target_actions(target_img, candidate_img, threshold):
    try:
        # extracting faces info
        target_img_details = face_detector(target_img)
        candidate_img_details = face_detector(candidate_img)

        # creating bounding box around detected target face
        target_bb_img = draw_bb(target_img, target_img_details.get("face_locations"))
        
        # checking for most similar face.
        best_match_details = target_candidates_compare(target_img_details.get("face_embeddings"), candidate_img_details.get("face_embeddings"), True, threshold)
        best_match_score = best_match_details.get("best_sim_score")
        target_match_loc = candidate_img_details.get("face_locations")[best_match_details.get("best_sim_score_index")]

        # drawing bounding box on identical face
        candidate_image_bb = draw_bb(candidate_img, [target_match_loc])

        # Making Pixtral inference
        image_url = image_to_data_url(candidate_image_bb)
        description = pixtral_describe_target(image_url)

        threshold_details = f"Selected Threshold: {threshold}\nFace Similarity Score: {100 * best_match_score:.2f}%\n\n{description}"
        return target_bb_img, candidate_image_bb, threshold_details
    
    except Exception:
        message = f"""ERROR!!!: A 'single' target face has not been found at threshold value {threshold}. Kindly ensure you have uploaded a "target" image with only one indiidual and a clear "candidate image" as well. \
            \n\nIf you have already done so, try reducing the "Minimum Similarity Threshold".. If issue still persists then your API key is no longer valid."""
        return target_bb_img, candidate_img, message


# UI
title = """
# **LookOutAI**👀  
#### *Find a target face in another image and choose to:*
- **Blur it**
- **Blur all other faces**
- **Describe the target face**

> **Minimum Similarity Threshold:** Use the slider to adjust detection sensitivity and watch ***LookOutAI*** look out for your target...
"""

with gr.Blocks() as demo:
    gr.Markdown(title)

    with gr.Row():
        with gr.Column(scale = 3): 
            target_img = gr.Image(label = "Target Image (single face)", type = "filepath", height = 300, width = 500)
        with gr.Column(scale = 3):
            candidate_img = gr.Image(label = "Candidate Image (multiple faces)", type = "filepath", height = 300, width = 500)
        with gr.Column(scale = 1, min_width = 200):
            threshold = gr.Slider(
                label = "Minimum Similarity Threshold",
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
        target_bb_img = gr.Image(label = "Preview Target Image", height = 300, width = 500)
        Output_image = gr.Image(label = "Preview Candidate Image", height = 300, width = 500)
        text_output = gr.Textbox(label = "Text Output")


    blur_target.click(
        blur_target_actions,
        inputs = [target_img, candidate_img, threshold],
        outputs = [target_bb_img, Output_image, text_output]
    )

    blur_others.click(
        blur_others_actions,
        inputs = [target_img, candidate_img, threshold],
        outputs = [target_bb_img, Output_image, text_output]
    )

    describe_target.click(
        describe_target_actions,
        inputs = [target_img, candidate_img, threshold],
        outputs = [target_bb_img, Output_image, text_output]
    )


if __name__ == "__main__":
    demo.launch()