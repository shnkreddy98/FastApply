import streamlit as st

class landingPageElements:

    def __init__(self):
        pass

    def get_details(information={}):
        # Initialize session state for work experience
        if information == {}:
            if "work_experience" not in st.session_state:
                st.session_state.work_experience = information.get('work_experience', [])
                st.session_state.project = information.get('project', [])
                st.session_state.education = information.get('education', [])
        else:
            st.session_state.work_experience = information.get('work_experience', [])
            st.session_state.project = information.get('project', [])
            st.session_state.education = information.get('education', [])

        # Function to add a new work experience entry
        def add_experience(element, dict):
            st.session_state[element].append({
                "company": "",
                "role": "",
                "date": "",
                "description": ""
            })

        # Function to remove the last work experience entry (minimum of 1)
        def remove_experience():
            if len(st.session_state.work_experience) > 1:
                st.session_state.work_experience.pop()
        # ---------------------------------------------------------------------------------------------------
        # Collect user details
        st.write("### Personal Details")
        user_name = st.text_input(
            "Enter name here",
            value=information.get('name', '')
        )
        user_email = st.text_input(
            "Enter email here",
            value=information.get('email', '')
        )
        user_phone = st.text_input(
            "Enter phone here",
            value=information.get('phone', '')
        )
        user_city = st.text_input(
            "Enter city here",
            value=information.get('location', '')
        )
        user_linkedin_link = st.text_input(
            "Enter LinkedIn profile link here",
            value=information.get('linkedin', '')
        )
        user_summary = st.text_area(
            "Enter summary here",
            value=information.get('summary', '')
        )
        user_skills = st.text_input(
            "Enter skills here",
            value=information.get('skills', '')
        )
        # ---------------------------------------------------------------------------------------------------
        # Display work experience
        st.write("### Work Experience")
        for i, element in enumerate(st.session_state.work_experience):
            st.session_state.work_experience[i]["company"] = st.text_input(
                f"Company Name for Work Experience {i + 1}",
                key=f"company_name_{i}",
                value=element.get('company', '')
            )
            st.session_state.work_experience[i]["role"] = st.text_input(
                f"Role for Work Experience {i + 1}",
                key=f"role_{i}",
                value=element.get('role', '')
            )
            st.session_state.work_experience[i]["date"] = st.text_input(
                f"Date for Work Experience {i + 1}",
                key=f"date_{i}",
                value=element.get('date', '')
            )
            st.session_state.work_experience[i]["description"] = st.text_area(
                f"Description for Work Experience {i + 1}",
                key=f"description_{i}",
                value=element.get('description', '')
            )
            st.markdown("---")  # Add a divider between experiences

        # Buttons to add or remove work experience
        st.button("Add Work Experience", on_click=add_experience, args=(st.session_state.work_experience))
        st.button("Remove Work Experience", on_click=remove_experience, args=(st.session_state.work_experience))
        # ---------------------------------------------------------------------------------------------------
        # Display Projects
        st.write("### Projects")
        for i, element in enumerate(st.session_state.projects):
            st.session_state.projects[i]["project"] = st.text_input(
                f"Project Name for Project {i + 1}",
                key=f"project_name_{i}",
                value=element.get('project', '')
            )
            st.session_state.projects[i]["date"] = st.text_input(
                f"Dates for Project {i + 1}",
                key=f"date_{i}",
                value=element.get('date', '')
            )
            st.session_state.projects[i]["description"] = st.text_input(
                f"Description for Project {i + 1}",
                key=f"description_{i}",
                value=element.get('description', '')
            )
            st.markdown("---")  # Add a divider between experiences

        # Buttons to add or remove work experience
        st.button("Add Project", on_click=add_experience, args=(st.session_state.projects))
        st.button("Remove Project", on_click=remove_experience, args=(st.session_state.projects))

        return user_name, user_email, user_phone, user_city, user_linkedin_link, user_summary, user_skills
