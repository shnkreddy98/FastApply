from defaultResume import getUserDetails
from dbmanagement import addToDb
from resumeGenerator import ResumeGenerator

import streamlit as st
import sqlite3
import streamlit as st

db_path = "./dbs/ResumeBuilder.db"

con = sqlite3.connect(db_path)





data = getUserDetails()

if st.button("Add to the Database"):
    addToDb(con, data)

if st.button("Generate Resume"):
    generator = ResumeGenerator(f"./ResumeBuilder/inputs/templates/template.docx")
    generator.generate(data, f"./ResumeBuilder/outputs/resumes/{data['Name']}.docx")
    st.toast(f"Resume created as '{data['Name']}.docx' and '{data['Name']}.pdf'")