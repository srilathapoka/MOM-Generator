import google.generativeai as genai
import os
import cv2
import numpy as np

from PIL import Image

def extract_text_image(file_path):
    file_bytes=np.asarray(bytearray(file_path.read()),dtype=np.uint8)
    image=cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
    #image=cv2.imread('imageclass.png')
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)#to convert bgr to rgb
    image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#to convert BGR to Grey
    _,image_bw=cv2.threshold(image_grey,150,255,cv2.THRESH_BINARY)#TO CONVERT GREY TO black and white

    #image that cv2 gives in in numpy array format,we need to convert it to image object
    final_image=Image.fromarray(image_bw)

    key=os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=key)
    model=genai.GenerativeModel('gemini-2.5-flash-lite')


    prompt='''You act as an OCR Application on the given image and extract the text from it.
    Give only the text as output,do not give any other explanation or descrption.'''


    response=model.generate_content([prompt,final_image])
    output_text=response.text
    return output_text
