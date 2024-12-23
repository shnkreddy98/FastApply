import streamlit as st

class landingPageSections:

    def __init__(self):
        pass

    def add_experience(section, section_elements):
        st.session_state[section].append(section_elements)

    # Function to remove the last work experience entry (minimum of 1)
    def remove_experience(section):
        if len(st.session_state[section]) > 1:
            st.session_state[section].pop()

    def get_details(information={}):
        # Initialize session state for work experience
        if information == {}:
            if 'name' not in st.session_state:
                st.session_state['name'] = information.get('name', '')
            if 'email' not in st.session_state:
                st.session_state['email'] = information.get('email', '')
            if 'phone' not in st.session_state:
                st.session_state['phone'] = information.get('phone', '')
            if 'location' not in st.session_state:
                st.session_state['location'] = information.get('location', '')
            if 'linkedin' not in st.session_state:
                st.session_state['linkedin'] = information.get('linkedin', '')
            if 'summary' not in st.session_state:
                st.session_state['summary'] = information.get('summary', '')
            if 'skills' not in st.session_state:
                st.session_state['skills'] = information.get('skills', '')
            if "work_experience" not in st.session_state:
                st.session_state.work_experience = information.get('work_experience', [])

            if "projects" not in st.session_state:
                st.session_state.projects = information.get('projects', [])
            
            if "education" not in st.session_state:
                st.session_state.education = information.get('education', [])
        else:
            st.session_state['name'] = information.get('name', '')
            st.session_state['email'] = information.get('email', '')
            st.session_state['phone'] = information.get('phone', '')
            st.session_state['location'] = information.get('location', '')
            st.session_state['linkedin'] = information.get('linkedin', '')
            st.session_state['summary'] = information.get('summary', '')
            st.session_state['skills'] = information.get('skills', '')
            st.session_state.work_experience = information.get('work_experience', [])
            st.session_state.projects = information.get('projects', [])
            st.session_state.education = information.get('education', [])

        work_exp_section_elements = {"exp_company":"",
                                     "exp_role":"",
                                     "exp_start_date":"",
                                     "exp_end_date":"",
                                     "exp_description":""}
        project_elements = {"proj_name": "", 
                            "proj_start_date": "", 
                            "proj_end_date": "", 
                            "proj_description": ""}
        education_elements = {"edu_course": "", 
                              "edu_institution": "", 
                              "edu_start_date": "",
                              "edu_end_date": ""}
        # ---------------------------------------------------------------------------------------------------
        # Collect user details
        st.session_state['name'] = st.text_input(
            "Enter name here", value=st.session_state['name']
        )
        st.session_state['email'] = st.text_input(
            "Enter email here", value=st.session_state['email']
        )
        st.session_state['phone'] = st.text_input(
            "Enter phone here", value=st.session_state['phone']
        )
        st.session_state['location'] = st.text_input(
            "Enter city here", value=st.session_state['location']
        )
        st.session_state['linkedin'] = st.text_input(
            "Enter LinkedIn profile link here", value=st.session_state['linkedin']
        )
        st.session_state['summary'] = st.text_area(
            "Enter summary here", value=st.session_state['summary']
        )
        st.session_state['skills'] = st.text_input(
            "Enter skills here", value=st.session_state['skills']
        )
        # ---------------------------------------------------------------------------------------------------
        # Display work experience
        st.write("### Work Experience")
        for i, section in enumerate(st.session_state.work_experience):
            st.session_state.work_experience[i]["exp_company"] = st.text_input(
                f"Company Name for Work Experience {i + 1}",
                key=f"exp_company_name_{i}",
                value=section.get('exp_company', '')
            )
            st.session_state.work_experience[i]["exp_role"] = st.text_input(
                f"Role for Work Experience {i + 1}",
                key=f"exp_role_{i}",
                value=section.get('exp_role', '')
            )
            st.session_state.work_experience[i]["exp_start_date"] = st.date_input(
                f"Start Date for Work Experience {i + 1}",
                key=f"exp_start_date_{i}",
                value=section.get('exp_start_date', '')
            )
            st.session_state.work_experience[i]["exp_end_date"] = st.date_input(
                f"End Date for Work Experience {i + 1}",
                key=f"exp_end_date_{i}",
                value=section.get('exp_end_date', '')
            )
            st.session_state.work_experience[i]["exp_description"] = st.text_area(
                f"Description for Work Experience {i + 1}",
                key=f"exp_description_{i}",
                value=section.get('exp_description', '')
            )
            st.markdown("---")  # Add a divider between experiences
        
        add_we, remove_we = st.columns(2)
        # Buttons to add or remove work experience
        with add_we:
            st.button("Add Work Experience", on_click=landingPageSections.add_experience, args=("work_experience", work_exp_section_elements))
        with remove_we:
            st.button("Remove Work Experience", on_click=landingPageSections.remove_experience, args=("work_experience",))
        # ---------------------------------------------------------------------------------------------------
        # Display Projects
        st.write("### Projects")
        for i, section in enumerate(st.session_state.projects):
            st.session_state.projects[i]["proj_name_"] = st.text_input(
                f"Project Name {i + 1}",
                key=f"proj_name_{i}",
                value=section.get('proj_name_', '')
            )
            st.session_state.projects[i]["proj_start_date"] = st.date_input(
                f"Start Date for Project {i + 1}",
                key=f"proj_start_date_{i}",
                value=section.get('proj_start_date', '')
            )
            st.session_state.projects[i]["proj_end_date"] = st.date_input(
                f"End Date for Project {i + 1}",
                key=f"proj_end_date_{i}",
                value=section.get('proj_end_date', '')
            )
            st.session_state.projects[i]["proj_description"] = st.text_input(
                f"Description for Project {i + 1}",
                key=f"proj_description{i}",
                value=section.get('proj_description', '')
            )
            st.markdown("---")  # Add a divider between experiences

        add_p, remove_p = st.columns(2)
        # Buttons to add or remove work experience
        with add_p:
            st.button("Add Project", on_click=landingPageSections.add_experience, args=("projects", project_elements))
        with remove_p:
            st.button("Remove Project", on_click=landingPageSections.remove_experience, args=("projects",))
        # ---------------------------------------------------------------------------------------------------
        # Display Education
        st.write("### Education")
        for i, section in enumerate(st.session_state.education):
            st.session_state.education[i]["edu_institution"] = st.text_input(
                f"Institution Name {i + 1}",
                key=f"edu_institution_name_{i}",
                value=section.get('proj_description', '')
            )
            st.session_state.education[i]["edu_course"] = st.text_input(
                f"Course selected {i + 1}",
                key=f"edu_course_{i}",
                value=section.get('edu_course', '')
            )
            st.session_state.education[i]["edu_start_date"] = st.date_input(
                f"Start Date for Course {i + 1}",
                key=f"edu_start_date_{i}",
                value=section.get('edu_start_date', '')
            )
            st.session_state.education[i]["edu_end_date"] = st.date_input(
                f"End Date for Course {i + 1}",
                key=f"edu_end_date_{i}",
                value=section.get('edu_end_date', '')
            )
            st.markdown("---")  # Add a divider between experiences

        add_e, remove_e = st.columns(2)
        # Buttons to add or remove work experience
        with add_e:
            st.button("Add Education", on_click=landingPageSections.add_experience, args=("education", education_elements))
        with remove_e:
            st.button("Remove Education", on_click=landingPageSections.remove_experience, args=("education",))

        user_data = {"user_name": st.session_state['name'],
                     "user_email": st.session_state['email'],
                     "user_phone": st.session_state['phone'],
                     "user_city": st.session_state['location'],
                     "user_linkedin_link": st.session_state['linkedin'],
                     "user_summary": st.session_state['summary'],
                     "user_skills": st.session_state['skills']}
        
        work_exp = {"experiences": st.session_state.work_experience}
        proj = {"projects": st.session_state.projects}
        edu = {"education": st.session_state.education}

        return user_data, work_exp, proj, edu
