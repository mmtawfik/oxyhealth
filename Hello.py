import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import datetime
import tempfile
from pathlib import Path
import os
from fpdf import FPDF
import hashlib

# New function for creating the password page
def password_page(patient_name, birthday, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password == "correct_password_hash":
        create_prescription(patient_name, date, day, birthday, prescription)
    else:
        st.write("Incorrect password. Please try again.")
        password_page(patient_name, birthday, "")

def create_prescription(patient_name, date, day, birthday, prescription):
    image_path = 'prescription.png' # Replace this with the actual path to your prescription.png file
    image = Image.open(image_path)
    image = image.convert("RGB") # Convert image to RGB mode
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("Arial.ttf", 28)


    draw.text((220, 395), patient_name, (0, 0, 0), font=font)
    draw.text((745, 395), date, (0, 0, 0), font=font)
    draw.text((300, 455), birthday, (0, 0, 0), font=font)
    draw.text((120, 520), prescription, (0, 0, 0), font=font)

    image.save('prescription.jpg', format='JPEG') # Save as JPEG format
    st.image(image, caption='Prescription', use_column_width=True)

    # Convert the image to a PDF file
    create_pdf('prescription.jpg', patient_name + '.pdf')

def display_image(image_data):
    image = Image.open(BytesIO(image_data))
    st.image(image, caption='Input Image', use_column_width=True)

def create_pdf(image_file, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.image(image_file, x=0, y=0, w=210)
    pdf.output(pdf_file)

def create_app():
    st.title('Create Prescription App')
    st.markdown("This app helps you create a prescription by filling in the details.")

    option = st.radio("Choose an option:", ["Create Password", "Access Prescription"])

    if option == "Create Password":
        patient_name = st.text_input("Patient Name", "")
        birthday = st.date_input("Patient's Birthday", datetime.date(1980, 7, 6))
        password = st.text_input("Password", type='password')
        if st.button("Submit"):
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == "correct_password_hash":
                st.write("Password already exists.")
            else:
                st.write("Password created successfully.")
    elif option == "Access Prescription":
        patient_name = st.text_input("Patient Name", "")
        birthday = st.date_input("Patient's Birthday", datetime.date(1980, 7, 6))
        password = st.text_input("Password", type='password')
        if st.button("Submit"):
            password_page(patient_name, birthday, password)

if __name__ == '__main__':
    create_app()
