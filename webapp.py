import google.generativeai as genai
import os
import numpy as np
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image


#configure the model
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-2.5-flash-lite')

#upload file in sidebar
user_text=None

st.sidebar.title(':orange[Upload your MOM notes here:]')
st.sidebar.subheader('Only Upload Images,PDF and Docx')
user_file=st.sidebar.file_uploader('Upload your file',type=['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type=='application/pdf':
        user_text=text_extractor_pdf(user_file)
    elif user_file.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        user_text=text_extractor_docx(user_file)
    elif user_file.type in ['image/jpg','image/png','image/jpeg']:
        user_text=extract_text_image(user_file)
    else:
        st.sidebar.write('Upload your correct file')


#main page
st.title(':blue[Minutes of Meeting]: :green[AI assisted MOM generator in a Standarized form from meetimg notes]')    
tips='''Tips to use this app
* Upload your meeting in sidebar(image,pdf,docx)
* click on generate MOM and get the standardized MOM's'''
st.write(tips)

if st.button('Generate MOM'):
    if user_text is None:
        st.error('Text is not generated')
    else:
        with st.spinner('Processing your data.....'):
            prompt=f'''Assume you are expert in creating minutes of meeting.User has provided
            notes of meeting in text format.using this data you need to create a standarized minutes
            of meeting for the user. 
            keep the format stricly as mentioned below

            output must follow word/docx format,strictly in the following manner:
            title:Title of meeting
            Heading:Meeting agenda
            subheading:name of attendees(if attendees name is not there keep it NA)
            subheading:date of meeting and place of meeting (place means name of conference/meeting room if not provided keep it online)
            Body:the body must follow the following sequence of points
            * keypoints discussed
            * Highlight any decision that has been finalised
            * mention actionable items
            * Any additional notes
            * Any deadline that has been discussed
            * Any next meeting date that has been discussed.
            * 2 to 3 line of summary
            * use bullet points and highlight or bold important keywords such that context is clear
            
            the data provided by user is as follows{user_text}'''

            response=model.generate_content(prompt)
            st.write(response.text)
            
