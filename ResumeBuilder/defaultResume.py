import streamlit as st
from streamlit_tags import st_tags
import pickle
import re

with open('./vars/skills_list.pkl', 'rb') as file:
    SKILLSLIST = pickle.load(file)

def clean_starting_characters(input_string):
    cleaned_lines = [re.sub(r'^[^a-zA-Z]+', '', line) for line in input_string.split('\n')]
    cleaned_string = '\n'.join(cleaned_lines)
    return cleaned_string

def addSection(sec):
    if sec=='workexp':
        st.session_state["work_experiences"].append({
            "workexp_company": "",
            "workexp_role": "",
            "workexp_location": "",
            "workexp_from": None,
            "workexp_to": None,
            "workexp_description": ""
        })
    if sec=='edu':
        st.session_state["education_institutions"].append({
            "edu_institution": "",
            "edu_degree": "",
            "edu_major": "",
            "edu_from": None,
            "edu_to": None,
        })
    if sec=='proj':
        st.session_state["projects"].append({
            "proj_title": "",
            "proj_link": "",
            "proj_from": None,
            "proj_to": None,
            "proj_description": ""
        })

def removeSection(sec):
    if sec=='workexp':
        section = "work_experiences"
    if sec=='edu':
        section = "education_institutions"
    if sec=='proj':
        section = "projects"
    if st.session_state[section]:
        st.session_state[section].pop()

def getUserDetails(data=None):
    global SKILLSLIST
    if "work_experiences" not in st.session_state:
        st.session_state["work_experiences"] = data.get("WorkExperience", []) if data else []
    if "education_institutions" not in st.session_state:
        st.session_state["education_institutions"] = data.get("Education", []) if data else []
    if "projects" not in st.session_state:
        st.session_state["projects"] = data.get("Projects", []) if data else []
    
    st.title("Add Resume")

    st.header("Personal Details")

    user_name = st.text_input("Name", value=data.get("Name", "") if data else "")
    user_city = st.text_input("Location", value=data.get("Location", "") if data else "")
    user_phone = st.text_input("Phone", value=data.get("Phone", "") if data else "")
    user_email = st.text_input("Email", value=data.get("Email", "") if data else "")
    user_linkedin = st.text_input("LinkedIn", value=data.get("LinkedIn", "") if data else "")
    user_github = st.text_input("GitHub", value=data.get("GitHub", "") if data else "")
    user_skills = st_tags(label='Enter Skills',
                           text='Press enter ⏎ to add more',
                           value=data.get("Skills", []) if data else [],
                           suggestions=SKILLSLIST,
                           maxtags=400, key='1')

    st.header("Work Experience")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Work Experience"):
            addSection('workexp')
    with col2:
        if st.button("Remove Work Experience"):
            removeSection('workexp')

    for idx, work_exp in enumerate(st.session_state["work_experiences"]):
        st.subheader(f"Work Experience {idx + 1}")
        work_exp["workexp_company"] = st.text_input(f"Company {idx + 1}", value=work_exp["workexp_company"], key=f"workexp_company_{idx}")
        work_exp["workexp_role"] = st.text_input(f"Role {idx + 1}", value=work_exp["workexp_role"], key=f"workexp_role_{idx}")
        work_exp["workexp_location"] = st.text_input(f"Location {idx + 1}", value=work_exp["workexp_location"], key=f"workexp_location_{idx}")
        work_exp["workexp_from"] = st.date_input(f"From {idx + 1}", value=work_exp["workexp_from"], key=f"workexp_from_{idx}", format="MM/DD/YYYY")
        work_exp["workexp_to"] = st.date_input(f"To {idx + 1}", value=work_exp["workexp_to"], key=f"workexp_to_{idx}", format="MM/DD/YYYY")
        work_exp["workexp_description"] = st.text_area(f"Description {idx + 1}", value=work_exp["workexp_description"], key=f"description_{idx}")
        work_exp["workexp_description"] = clean_starting_characters(work_exp["workexp_description"])

    st.header("Education")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Education"):
            addSection('edu')
    with col2:
        if st.button("Remove Educatiom"):
            removeSection('edu')

    for idx, edu_institution in enumerate(st.session_state["education_institutions"]):
        st.subheader(f"Education {idx + 1}")
        edu_institution["edu_institution"] = st.text_input(f"Institution {idx + 1}", value=edu_institution["edu_institution"], key=f"edu_instituion_{idx}")
        edu_institution["edu_degree"] = st.text_input(f"Degree {idx + 1}", value=edu_institution["edu_degree"], key=f"edu_degree_{idx}")
        edu_institution["edu_major"] = st.text_input(f"Major {idx + 1}", value=edu_institution["edu_major"], key=f"edu_major_{idx}")
        edu_institution["edu_from"] = st.date_input(f"From {idx + 1}", value=edu_institution["edu_from"], key=f"edu_from_{idx}", format="MM/DD/YYYY")
        edu_institution["edu_to"] = st.date_input(f"To {idx + 1}", value=edu_institution["edu_to"], key=f"edu_to_{idx}", format="MM/DD/YYYY")
        

    st.header("Projects")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Projects"):
            addSection('proj')
    with col2:
        if st.button("Remove Projects"):
            removeSection('proj')

    for idx, projects in enumerate(st.session_state["projects"]):
        st.subheader(f"Project {idx + 1}")
        projects["proj_title"] = st.text_input(f"Title {idx + 1}", value=projects["proj_title"], key=f"proj_title_{idx}")
        projects["proj_link"] = st.text_input(f"Link {idx + 1}", value=projects["proj_link"], key=f"proj_link_{idx}")
        projects["proj_from"] = st.date_input(f"From {idx + 1}", value=projects["proj_from"], key=f"proj_from_{idx}", format="MM/DD/YYYY")
        projects["proj_to"] = st.date_input(f"To {idx + 1}", value=projects["proj_to"], key=f"proj_to_{idx}", format="MM/DD/YYYY")
        projects["proj_description"] = st.text_area(f"Description {idx + 1}", value=projects["proj_description"], key=f"proj_description_{idx}")
        projects["proj_description"] = clean_starting_characters(projects["proj_description"])

    user_data = {
        "Name": user_name, 
        "Location": user_city, 
        "Phone": user_phone, 
        "Email": user_email, 
        "LinkedIn": user_linkedin, 
        "GitHub": user_github,
        "Skills": user_skills,
        "WorkExperience": st.session_state['work_experiences'],
        "Education": st.session_state['education_institutions'],
        "Projects": st.session_state['projects']
    }

    return user_data
