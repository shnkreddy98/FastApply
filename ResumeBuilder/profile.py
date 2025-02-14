from defaultResume import getUserDetails
from dbmanagement import getData, addToDb, get_resume_counter
from resumeGenerator import ResumeGenerator
from webScrapper import getContent
from requestOpenAI import requestOpenAI
import json
import re

import streamlit as st
from datetime import datetime

def convert_datetime_in_string(json_string):
    # Pattern to match datetime.date(Y, M, D)
    date_pattern = re.compile(r"datetime\.date\((\d{4}),\s*(\d{1,2}),\s*(\d{1,2})\)")

    # Replace with "YYYY-MM-DD" format
    formatted_string = date_pattern.sub(r'"\1-\2-\3"', json_string)
    return formatted_string


def formatDate(date_str):
   date_obj = datetime.strptime(date_str, "%Y-%m-%d")
   formatted_date = date_obj.strftime("%b-%y")
   return formatted_date

def mainPage(jsonfile):
    if 'edit_toggle' not in st.session_state:
        st.session_state['edit_toggle'] = False
    
    st.title("User Profile")
    col1, col2 = st.columns(2)
    with col1:
        jd_url = st.text_input("Enter URL link for the Job Description")
    with col2:
        company_name = st.text_input("Company Name")

    if st.button("Get Job Description"):
        try:
            jd_desc = getContent(jd_url, company_name)
            jd_desc_container = st.container(height=500, border=True)
            jd_desc_container.write(f"""
                                     #### JobDescription                                     
                                     {jd_desc}
                                     """)

        except Exception as e:
            if len(jd_url) == 0:
                st.warning("Please enter valid JD URL")
            elif len(company_name) == 0:
                st.warning("Please enter valid company name")
            else:
                print(e)

    edit_on = st.toggle("Edit Profile")
    resume_no = get_resume_counter(jsonfile)
    data = getData(resume_no-1)

    users = data[0]
    skills = [skill[1] for skill in data[1]]
    workexp = data[2]
    edu = data[3]
    proj = data[4]
    workexp_list = []
    edu_list = []
    proj_list = []
        
    user_data = {
        "Name": users[0][1], 
        "Location": users[0][3], 
        "Phone": users[0][2], 
        "Email": users[0][0], 
        "LinkedIn": users[0][4], 
        "GitHub": users[0][5],
        "Skills": skills,
        "WorkExperience": workexp_list,
        "Education": edu_list,
        "Projects": proj_list
    }


    if edit_on:
        st.session_state.edit_toggle = True
    else:
        st.session_state.edit_toggle = False

    if st.session_state.edit_toggle:
        db_data = getUserDetails(user_data)

        if st.button("Add to the Database"):
            addToDb(db_data, jsonfile)
    else:
        personal_container = st.container(border=True)
        
        personal_container.write(f"""
                                **Name**: {users[0][1]}  
                                **Email**: {users[0][0]}  
                                **Phone**: {users[0][2]}  
                                **City**: {users[0][3]}  
                                **LinkedIn**: {users[0][4]}  
                                **GitHub**: {users[0][5]}  
                                """, unsafe_allow_html=True)
        
        
        skills_container = st.container(border=True)
        skills_container.write(f"""
                            **Skills**  
                            {', '.join(skills)}
                            """)
        
        st.subheader("Work Experience")
        for row in workexp:
            format_form = formatDate(row[4])
            format_to = formatDate(row[5])
            format_desc = "\n * ".join(row[6].split("\n"))
            workexp_container = st.container(border=True)
            workexp_container.write(f"""
                                    **Company**: {row[1]}  
                                    **Role**: {row[2]}  
                                    **Location**: {row[3]}  
                                    {format_form} - {format_to}  
                                    **Description**  
                                    {format_desc}  
                                    """, unsafe_allow_html=True)
            workexp_list.append({
                "workexp_company": row[1],
                "workexp_role": row[2],
                "workexp_location": row[3],
                "workexp_from": row[4],
                "workexp_to": row[5],
                "workexp_description": row[6]
            })
        
        st.subheader("Education")
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
            edu_list.append({
                "edu_institution": row[1],
                "edu_degree": row[2],
                "edu_major": row[3],
                "edu_from": row[4],
                "edu_to": row[5]
            })
        
        st.subheader("Projects")
        for row in proj:
            format_form = formatDate(row[3])
            format_to = formatDate(row[4])
            format_desc = "\n* ".join(row[5].split("\n"))
            proj_container = st.container(border=True)
            proj_container.write(f"""
                                **Project Title**: {row[1]}  
                                **Project Link**: {row[2]}  
                                {format_form} - {format_to}  
                                {format_desc}
                                """, unsafe_allow_html=True)
            proj_list.append({
                "proj_title": row[1],
                "proj_link": row[2],
                "proj_from": row[3],
                "proj_to": row[4],
                "proj_description": row[5]
            })
    
    if jd_url and company_name:
        if st.button("Craft new resume"):
            with open(f"./ResumeBuilder/Outputs/{company_name}/JD.txt", "r") as f:
                jd_desc = f.readlines()

            openaiobj = requestOpenAI()
            res = openaiobj.get_new_resume(user_data, jd_desc)
                    
            try:
                res = res.choices[0].message.content
            except json.JSONDecodeError as e:
                res = res.choices[0].message.content.replace("\'", "\"")
    
            formatted_res = convert_datetime_in_string(res)
            res_dict = json.loads(formatted_res)

            generator = ResumeGenerator(f"./ResumeBuilder/inputs/templates/template.docx")
            generator.generate(res_dict, f"./ResumeBuilder/outputs/{company_name}/{res_dict['Name']}.docx")
            st.toast(f"Resume created as '{res_dict['Name']}.docx' and '{res_dict['Name']}.pdf'")
