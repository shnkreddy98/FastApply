from defaultResume import getUserDetails
from dbmanagement import getData
from dbmanagement import addToDb
from resumeGenerator import ResumeGenerator

import streamlit as st
from datetime import datetime

def formatDate(date_str):
   date_obj = datetime.strptime(date_str, "%Y-%m-%d")
   formatted_date = date_obj.strftime("%b-%y")
   return formatted_date

def mainPage(jsonfile):
    st.title("User Profile")
    data = getData()

    if (len(data) > 1) and (len(data[0][0]) > 1):
        users = data[0]
        skills = [skill[1] for skill in data[1]]
        workexp = data[2]
        edu = data[3]
        proj = data[4]

        personal_container = st.container(border=True)
        personal_container.write(f"""
                                **Name**: {users[0][1]}  
                                **Email**: {users[0][0]}  
                                **Phone**: {users[0][2]}  
                                **City**: {users[0][3]}  
                                **LinkedIn**: {users[0][4]}  
                                **GitHub**: {users[0][5]}  
                                """, unsafe_allow_html=True)

        for row in workexp:
            format_form = formatDate(row[4])
            format_to = formatDate(row[5])
            workexp_container = st.container(border=True)
            workexp_container.write(f"""
                                    **Company**: {row[1]}  
                                    **Role**: {row[2]}  
                                    **Location**: {row[3]}  
                                    {format_form} - {format_to}  
                                    **Description**  
                                    {row[6]}  
                                    """, unsafe_allow_html=True)

        for row in edu:
            format_form = formatDate(row[4])
            format_to = formatDate(row[5])
            edu_container = st.container(border=True)
            edu_container.write(f"""
                                **Institution**: {row[1]}  
                                **Degree**: {row[2]}  
                                **Course**: {row[3]}  
                                {format_form} - {format_to}  
                                """, unsafe_allow_html=True)

        for row in proj:
            format_form = formatDate(row[3])
            format_to = formatDate(row[4])
            proj_container = st.container(border=True)
            proj_container.write(f"""
                                **Project Title**: {row[1]}  
                                **Project Link**: {row[2]}  
                                {format_form} - {format_to}  
                                {row[5]}
                                """, unsafe_allow_html=True)
            
        # user_data = {
        #     "Name": users[0][1], 
        #     "Location": users[0][3], 
        #     "Phone": users[0][2], 
        #     "Email": users[0][0], 
        #     "LinkedIn": users[0][4], 
        #     "GitHub": users[0][5],
        #     "Skills": skills,
        #     "WorkExperience": workexp,
        #     "Education": edu,
        #     "Projects": proj
        # }
    else:
        data = getUserDetails()

        if st.button("Add to the Database"):
            addToDb(data, jsonfile)

        if st.button("Generate Resume"):
            generator = ResumeGenerator(f"./ResumeBuilder/inputs/templates/template.docx")
            generator.generate(data, f"./ResumeBuilder/outputs/resumes/{data['Name']}.docx")
            st.toast(f"Resume created as '{data['Name']}.docx' and '{data['Name']}.pdf'")