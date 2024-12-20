import os
from dotenv import load_dotenv
import streamlit as st

from modules.parseDocument import parseDocument
from modules.structureDocx import structureDocx
from modules.landingPageSections import landingPageSections
from modules.requestOpenAI import requestOpenAI
# from modules.accessDB import accessDB

load_dotenv()

if __name__=="__main__":
    openai_api = os.getenv('OPENAI_API')

    # Get resume and store in cache for faster access
    # jd_filename = "ResumeBuilder/jd/coherent.docx"
    # jd = parseDocument.read_file(jd_filename)
    jdfile = parseDocument.read_file("/Users/reddy/Documents/GitHub/FastApply/FastApply/jd/coherent.docx")
    jd_texts = [paragraph.text for paragraph in jdfile.paragraphs]
    jd_combined = "\n".join(paragraph.text for paragraph in jdfile.paragraphs)

    # accessDB.create_tables()
    # docx_file = SOURCEFILE
    uploaded_resume = st.file_uploader("Choose a Resume or start filling details")
    details = None
    if st.button("Parse Resume"):
        details = parseDocument.extract_details(uploaded_resume)

    if details!=None:
        user_data, work_exp_data, projects_data, education_data = landingPageSections.get_details(details)
    else:
        user_data, work_exp_data, projects_data, education_data = landingPageSections.get_details()

    st.write(user_data, work_exp_data, projects_data, education_data)

    if st.button("Create a new Resume"):
        resume_builder = requestOpenAI()
        res = resume_builder.get_new_resume(user_data, 
                                           work_exp_data, 
                                           projects_data, 
                                           education_data, 
                                           jd_combined)
        st.write(res.choices[0].message.content)



    # if st.button("Save Resume"):
        # accessDB.insert_values(user_data, work_exp_data, projects_data, education_data)

    # resume = st.text_area(label="Enter resume here.")

    # if st.button("Create docx"):
    #     structureDocx.create_document(resume, "Shashank")
    #     st.warning("New resume created successfully!")


    


