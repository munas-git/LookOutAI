#### Project Status: Semi-complete.

# Project Title: LookOutAI

**LookOutAI** is a cutting-edge tool designed for "looking out"; both literally and figuratively. It uses advanced image recognition technology to identify a person in a photo or video clip by matching their image. Once identified, the system can provide a detailed description of the individual, including their actions or behavior.   

LookOutAI also offers versatile features, such as selectively censoring a target or uncensoring only the target's face, ensuring privacy or clarity where needed.   

This tool is especially valuable for security applications, where video footage must be processed quickly and with high precision. It enables law enforcement or security teams to prepare evidence while protecting the privacy of uninvolved individuals by blurring their faces.   

### Tools and Libraries used:
* PIL
* cv2
* Difflib
* Gradio
* Docker
* Pixtral AI
* face_recognition

### How do run (Unix-like system or gitbash cli on windows):   
Initially
```
git clone https://github.com/munas-git/LookOutAI.git   
cd LookOutAI   
source setup.sh
```

Subsequently
```
source LookOutAIenv/Scripts/activate
python app/app.py
```

**NB:** You will have to create a `.env` file and include your **MISTRAL_API_KEY** if you wish to work with the "Describe (Target)" feature.   

The `Initially` commands above will clone the repo, navigate to the right path, create and activate a virtual environment for the system with all dependencies, and then run the **Gradio UI**. The `Subsequently` code assumes you have previously run `Initially` and have every system requirement setup and you're within the base dir... Have fun!   

## Snapshots of the System... ([Click for demo video](https://www.youtube.com/watch?v=0Q683n8gmIc)).
![Screenshot (479)](https://github.com/user-attachments/assets/49fab016-f4b5-4e56-a023-851e401bd5b9)
