import streamlit as st
from streamlit_tags import st_tags

skills_list = ["Python", "Java", "JavaScript", "C", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
               "R", "TypeScript", "Go", "Rust", "Shell Scripting", "Bash", "PowerShell", "SQL/NoSQL", 
               "HTML", "CSS", "React.js", "Angular", "Vue.js", "Next.js", "Node.js", "Django",
               "Flask", "Ruby on Rails", "ASP.NET", "Web APIs", "REST", "GraphQL", "WebSocket", 
               "Android Development (Java, Kotlin)", "iOS Development", "Swift", "Objective-C", 
               "Flutter", "React Native", "Xamarin", "Apache Cordova", "AWS", "EC2", "S3", "Lambda", 
               "Microsoft Azure", "Google Cloud Platform (GCP)","Kubernetes", "Docker", "Terraform", 
               "OpenShift", "CloudFormation", "Jenkins", "GitHub Actions", "CircleCI", "Ansible", 
               "Puppet", "Chef", "CI/CD Pipelines", "Prometheus", "Grafana", "Splunk", "ELK Stack", 
               "Version Control", "Git", "SVN", "SQL", "PostgreSQL", "MySQL", "Oracle", "NoSQL", "MongoDB", "Cassandra",  
               "Big Data Tools", "Hadoop", "Apache Spark", "Data Warehousing", "Redshift", "Snowflake", "BigQuery",
               "ETL Tools", "Apache Nifi", "Talend", "Apache Kafka", "Airflow", "TensorFlow", "PyTorch", 
               "Scikit-learn", "Keras", "spaCy", "NLTK", "Matplotlib", "Seaborn", "Tableau", "Power BI", 
               "Deep Learning Frameworks", "Reinforcement Learning", "Computer Vision (OpenCV)", "Penetration Testing", 
               "Metasploit", "Burp Suite", "Network Security", "Wireshark", "Snort", "DynamoDB",
               "SIEM", "Splunk", "QRadar", "Identity and Access Management (IAM)", "Encryption Protocols", 
               "Firewalls and Intrusion Detection Systems", "OWASP Practices", "Network Protocols", 
               "TCP/IP", "DNS", "HTTP", "FTP", "SDN (Software Defined Networking)", "Cisco Routers/Switches Configuration", 
               "Network Troubleshooting Tools", "Load Balancing", "NGINX", "HAProxy", "Selenium", "JUnit/TestNG", 
               "Postman", "Cypress", "Appium", "Load Testing", "JMeter", "LoadRunner", "Bug Tracking Tools", "JIRA", "Bugzilla", 
               "Problem-Solving", "Critical Thinking", "Communication Skills", "Time Management",
               "Collaboration and Teamwork", "Agile/Scrum Methodologies", "Agile Methodologies", "Scrum Master/Project Lead Skills", 
               "JIRA", "Trello", "Asana", "Monday.com", "Risk Management", "Roadmapping", "Blockchain", "AR/VR Development", 
               "Internet of Things (IoT)", "Quantum Computing", "Edge Computing", "Robotics", "API Design and Integration", 
               "Performance Optimization", "Debugging and Troubleshooting", "Cross-platform Development", "Legacy Code Refactoring"]

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

def getUserDetails():
    if "work_experiences" not in st.session_state:
        st.session_state["work_experiences"] = []
    if "education_institutions" not in st.session_state:
        st.session_state["education_institutions"] = []
    if "projects" not in st.session_state:
        st.session_state["projects"] = []
    
    st.title("Enter User Details")

    st.header("Personal Details")

    user_name = st.text_input("Name", placeholder="Enter Name here")
    user_city = st.text_input("Location", placeholder="Enter City here")
    user_phone = st.text_input("Phone", placeholder="Enter Phone no. here")
    user_email = st.text_input("Email", placeholder="Enter email here")
    user_linkedin = st.text_input("LinkedIn", placeholder="Enter linkedin url here")
    user_github = st.text_input("GitHub", placeholder="Enter github url here")
    user_skills = st_tags(label='Enter Skills',
                        text='Press enter \u23CE to add more',
                        value=None,
                        suggestions=skills_list,
                        maxtags = 400, key='1')

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

    st.header("Education")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Education"):
            addSection('edu')
    with col2:
        if st.button("Remove Educatiom"):
            removeSection('edu')

    for idx, edu_institution in enumerate(st.session_state["education_institutions"]):
        st.subheader(f"Work Experience {idx + 1}")
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
        st.subheader(f"Work Experience {idx + 1}")
        projects["proj_title"] = st.text_input(f"Title {idx + 1}", value=projects["proj_title"], key=f"proj_title_{idx}")
        projects["proj_link"] = st.text_input(f"Link {idx + 1}", value=projects["proj_link"], key=f"proj_link_{idx}")
        projects["proj_from"] = st.date_input(f"From {idx + 1}", value=projects["proj_from"], key=f"proj_from_{idx}", format="MM/DD/YYYY")
        projects["proj_to"] = st.date_input(f"To {idx + 1}", value=projects["proj_to"], key=f"proj_to_{idx}", format="MM/DD/YYYY")
        projects["proj_description"] = st.text_area(f"Description {idx + 1}", value=projects["proj_description"], key=f"proj_description_{idx}")

    user_data = {
        "Name": user_name, 
        "Location": user_city, 
        "Phone": user_phone, 
        "Email": user_email, 
        "LinkedIn": user_linkedin, 
        "GitHub": user_github,
        "Skills": user_skills,
        "WorkExperience": st.session_state['work_experiences'],
        "Eduction": st.session_state['education_institutions'],
        "Projects": st.session_state['projects']
    }

    return user_data

def addToDb(data_json):
    pass

def main():
    data = getUserDetails()
    addToDb(data)


if __name__=="__main__":
    main()