import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuring the Key and initiating the model
genai.configure(api_key=os.getenv('GOOGLE-API-KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Front End

st.header("MeetScribe:blue[.ai]: Minutes of Meeting Generator", divider=True)
uploaded_file = st.file_uploader("Upload your Hand-Written Notes here",
                 type=['jpg','jpeg','png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)

    prompt = f'''
    You are an intelligent assistant tasked with generating structured Minutes of Meeting (MoM) based on handwritten notes and to-dos provided as images. Your job is to extract text from the images and organize the information into a clean, professional table with the following columns:

    | Particulars (To-Dos) | Deadline | Status (Completed / Pending / Not Started) | % Completion |

    Requirements:
    1. OCR: Accurately read and transcribe handwritten text from the uploaded images.

    2. Task Identification: Identify individual to-do items, action points, or tasks from the transcribed text.

    3. Deadline Detection: Detect any mentioned dates or inferred deadlines related to each task. If no deadline is present, leave the field blank or mark as “TBD.”

    4. Status Assignment: Based on context (e.g., checkmarks, strikethroughs, annotations like "done", "in progress", "to-do", etc.), assign a task status:

    ✅ Completed

    🕒 Pending

    ⏳ Not Started

    5. Completion %: Estimate a percentage completion (e.g., 0%, 50%, 100%) based on the language or markings (e.g., “half done”, “in progress”, “✓✓✓”, etc.).
    '''

    submit = st.button("🚀 Get AI-Powered Insights")
    if submit:
        with st.spinner("Extracting and Analysing.."):
            response = model.generate_content([img,prompt]).text
            st.success("Extraction Complete")
            st.markdown("####✨ Generated Output")
            st.write(response)