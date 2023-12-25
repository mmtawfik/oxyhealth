import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF
import streamlit as st

# App data
prescriptions = []

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
    # Save the created prescription to the list
    prescriptions.append({'name': patient_name, 'date': date, 'day': day, 'birthday': birthday, 'prescription': prescription})

def display_prescriptions():
    st.subheader('Review The Datials of Patient')
    for prescription in prescriptions:
        st.write(f"**Patient Name:** {prescription['name']}")
        st.write(f"**Date:** {prescription['date']}")
        st.write(f"**Day:** {prescription['day']}")
        st.write(f"**Birthday:** {prescription['birthday']}")
        st.write(f"**Prescription:** {prescription['prescription']}")
        st.write("---")

def create_pdf(image_file, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.image(image_file, x=0, y=0, w=210)
    pdf.output(pdf_file)

def create_app():
    st.title('Create Prescription App')
    st.markdown("This app helps you create a prescription by filling in the details.")

    patient_name = st.text_input("Patient Name", "")
    prescription_date = datetime.date.today().strftime("%d-%m-%Y")
    day = datetime.datetime.today().strftime("%A")
    birthday = st.date_input("Patient's Birthday", datetime.date(2020, 1, 1), datetime.date(1940, 12, 31))
    prescription = st.text_area(":blue[My text here :]",height=2000)

    # Add a password input
    password = st.text_input("Password", type='password')

    submit = st.button("Create Prescription")

    if submit:
        if password == "engyoxyhealth5049": # Replace 'your_password_here' with the actual password
            create_prescription(patient_name, prescription_date, day, str(birthday), prescription)
            pdf_file = patient_name + '.pdf'
            if os.path.exists(pdf_file):
                st.download_button(label="Download Prescription", data=open(pdf_file, 'rb'), file_name=pdf_file, mime='application/pdf')
            display_prescriptions()
        else:
            st.error("Incorrect password. Please try again.")

if __name__ == '__main__':
    create_app()
