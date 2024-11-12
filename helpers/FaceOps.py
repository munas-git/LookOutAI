import cv2
import numpy as np
import face_recognition


def cosine_similarity(array1: np.ndarray, array2: np.ndarray) -> float:

    dot_product = np.dot(array1, array2)
    
    norm1 = np.linalg.norm(array1)
    norm2 = np.linalg.norm(array2)

    if norm1 == 0 or norm2 == 0:
        raise ValueError("Input arrays must not be zero-vectors.")
    
    return dot_product / (norm1 * norm2)


def face_detector(image_path:str):
    """
    face_detector detects the faces within any image/frame given then returns the face number, location(s), and embeddig(s).   

    ### Input   
    - **image_path == str:** String representing image path.

    ### Outputs   
    - **face_details == dict:** dictioary containing arrays of information about each face accisible using `get` face_num, location, embedding.
    """

    image = cv2.imread(image_path)

    # image/video frame conversion to RGB format.... OpenCV default load is BGR
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # identifying faces
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    count = 0
    face_details = {} # array of face details

    face_details.setdefault("face_nums", [])
    face_details.setdefault("face_locations", [])
    face_details.setdefault("face_embeddings", [])


    for face_location, face_encoding in zip(face_locations, face_encodings):
        
        count += 1
        face_details["face_nums"].append(count)
        face_details["face_locations"].append((face_location))
        face_details["face_embeddings"].append(np.array(face_encoding))
        
    return face_details
    

def target_candidates_compare(target_embedding:np.ndarray, candidate_embeddings:list, return_best_match = False, confidence: float = None):
    """
    target_candidates_compare calculates the similarity between face embeddings given a single target embedding `target_embedding` and a list of embeddings `candidate_embeddings` to be compared against the `target_embedding`.
    The function then returns the embeddings as well as their respective similarity scores.   

    ### Input   
    - **target_embedding == list:** List containing the embedding of the target face or face of interest.
    - **candidate_embeddings == list:** List containing possible matching embeddings for comparison with target embedding.
    - **return_best_match == bool** Boolean value used to determine if only the *best* (most similar) matching score and array index should be returned. This must be above a certain confidence threshold.
    - **confidence == float** float threshold value between ***0.55 and 1*** which ***must*** be set if return_best_match is set to `True`

    ### Outputs   
    - **face_details == array:** 
    """

    # input validity check
    if return_best_match and confidence is None:
        raise ValueError("You must specify a float threshold value when return_best_match is True.")
    elif return_best_match and confidence is not None:
        if (confidence < 0.55 or confidence > 1) or (isinstance(confidence, float) == False):
            raise ValueError("Specify a valid confidence level... i.e **0.55 < confidence < 1**")
        
    similarity_scores_arr = np.zeros(len(candidate_embeddings)) # array of zeros same length as target embeddings

    for i, candidate_embedding in enumerate(candidate_embeddings):
        similarity_scores_arr[i] = cosine_similarity(target_embedding, candidate_embedding)
    
    if return_best_match:
        if similarity_scores_arr.max() >= confidence:
            return {
                "best_sim_score" : similarity_scores_arr.max(),
                "best_sim_score_index" : similarity_scores_arr.argmax()
            }
        else:
            raise Exception("'Best match score' less than confidence threshold or no faces are detected.")

    else:
        return {
            "sim_scores" : similarity_scores_arr,
            "best_sim_score_index" : similarity_scores_arr.argmax()
        }


def blur_regions(image: np.ndarray, face_locations: list, alpha: float):
    """
    blur_regions blurs specified regions in an image with a configurable blur intensity (alpha).

    ### Args:   
        - **image** == np.ndarray: The input image (e.g., RGB or BGR).
        - **face_locations** == list: List of bounding box coordinates [(top, right, bottom, left), ... (top, right, bottom, left)].
        - **alpha** == float: Blur intensity,  0 < blur, 1 <= full blur.

    ### Returns:
        np.ndarray: Image with the specified region(s) blurred based on alpha.
    """
    if not (0 <= alpha <= 1):
        raise ValueError("Alpha must be value between 0 and 1.")
    
    blended_image = image.copy() # copying image to avoid modifying original.... might change later
    
    for (top, right, bottom, left) in face_locations:

        roi = blended_image[top:bottom, left:right]
        blurred_roi = cv2.GaussianBlur(roi, (103, 103), 0)
        
        blended_roi = cv2.addWeighted(blurred_roi, alpha, roi, 1 - alpha, 0) # region blending
        blended_image[top:bottom, left:right] = blended_roi # region replacement
    
    return blended_image


# dets = face_detector("../GroupIMG.jpeg")
# embds = dets.get("face_embeddings")
# face_locs = dets.get("face_locations")

# print(target_candidates_compare(embds[2], embds, True, 0.8))


def emoji_replacment():
    pass