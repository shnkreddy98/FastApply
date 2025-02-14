import sqlite3
import streamlit as st
import hashlib
import json

ERRORS = 0
INSERTQUERY = "INSERT OR IGNORE INTO {} VALUES ({});"
DBPATH = "./dbs/ResumeBuilder.db"
CONN = sqlite3.connect(DBPATH)
cur = CONN.cursor()
CONN.execute('PRAGMA foreign_keys = ON;')

user_table_query = """CREATE TABLE IF NOT EXISTS user (
                      user_email_id TEXT PRIMARY KEY,
                      user_name TEXT NOT NULL,
                      user_phone TEXT,
                      user_city TEXT,
                      user_linkedin_link TEXT,
                      user_github_link TEXT,
                      user_summary TEXT,
                      resume_id INT NOT NULL);
                  """

user_skill_table_query = """CREATE TABLE IF NOT EXISTS userskills (
                            skill_id TEXT PRIMARY KEY,
                            skill_name TEXT NOT NULL,
                            resume_id INT NOT NULL,
                            email_id TEXT NOT NULL,
                            FOREIGN KEY(email_id) REFERENCES user(user_email_id) ON DELETE CASCADE);
                         """

workexp_table_query = """CREATE TABLE IF NOT EXISTS workexp (
                         workexp_id TEXT PRIMARY KEY,
                         workexp_company TEXT NOT NULL,
                         workexp_role TEXT NOT NULL,
                         workexp_location TEXT,
                         workexp_from DATE,
                         workexp_to DATE,
                         workexp_description TEXT,
                         resume_id INT NOT NULL,
                         email_id TEXT NOT NULL,
                         FOREIGN KEY(email_id) REFERENCES user(user_email_id) ON DELETE CASCADE);
                      """

proj_table_query = """CREATE TABLE IF NOT EXISTS proj (
                      proj_id TEXT PRIMARY KEY,
                      proj_title TEXT NOT NULL,
                      proj_link TEXT,
                      proj_from DATE,
                      proj_to DATE,
                      proj_description TEXT,
                      resume_id INT NOT NULL,
                      email_id TEXT NOT NULL,
                      FOREIGN KEY(email_id) REFERENCES user(user_email_id) ON DELETE CASCADE);
                  """
      
edu_table_query = """CREATE TABLE IF NOT EXISTS edu ( 
                     edu_id TEXT PRIMARY KEY,
                     edu_institution TEXT NOT NULL,
                     edu_degree TEXT,
                     edu_course TEXT,
                     edu_from DATE,
                     edu_to DATE,
                     resume_id INT NOT NULL,
                     email_id TEXT NOT NULL,
                     FOREIGN KEY(email_id) REFERENCES user(user_email_id) ON DELETE CASCADE);
                 """

jobs_table_query = """CREATE TABLE IF NOT EXISTS jobs (
                      job_id TEXT PRIMARY KEY,
                      job_link TEXT NOT NULL,
                      job_description TEXT,
                      company_name TEXT,
                      resume_id INT NOT NULL,
                      email_id TEXT NOT NULL,
                      FOREIGN KEY(email_id) REFERENCES user(user_email_id) ON DELETE CASCADE);
                   """

companies_table_query = """CREATE TABLE IF NOT EXISTS companies (
                           company_id TEXT PRIMARY KEY,
                           company_name TEXT NOT NULL UNIQUE,
                           job_link TEXT NOT NULL,
                           FOREIGN KEY(job_link) REFERENCES jobs(job_link) ON DELETE CASCADE);
                        """

hiring_manager_table_query = """CREATE TABLE IF NOT EXISTS hiringmanagers (
                                hiring_manager_id TEXT PRIMARY KEY,
                                hiring_manager_fn TEXT NOT NULL,
                                hiring_manager_ln TEXT NOT NULL,
                                company_name TEXT NOT NULL,
                                FOREIGN KEY(company_name) REFERENCES companies(company_name) ON DELETE CASCADE);
                             """

ALLTABLES = {'user': user_table_query, 
             'userskills': user_skill_table_query,
             'workexp': workexp_table_query, 
             'proj': proj_table_query, 
             'edu': edu_table_query, 
             'jobs': jobs_table_query,
             'companies': companies_table_query,
             'hiringmanagers': hiring_manager_table_query}

def getData(resumeNo):
    cur.execute(f"SELECT * FROM user WHERE resume_id={resumeNo};")
    users = cur.fetchall()

    cur.execute(f"SELECT * FROM userskills WHERE resume_id={resumeNo};")
    skills = cur.fetchall()
    
    cur.execute(f"SELECT * FROM workexp WHERE resume_id={resumeNo};")
    workexp = cur.fetchall()
    
    cur.execute(f"SELECT * FROM edu WHERE resume_id={resumeNo};")
    edu = cur.fetchall()
    
    cur.execute(f"SELECT * FROM proj WHERE resume_id={resumeNo};")
    proj = cur.fetchall()

    return (users, skills, workexp, edu, proj)


def get_resume_counter(jsonfile):
    f = open(jsonfile)
    data = json.load(f)
    counter = data['resume']

    return int(counter)

def put_resume_counter(resumecounter, jsonfile):
    diction = {"resume": int(resumecounter)}
    json_object = json.dumps(diction, indent=4)

    with open(jsonfile, "w") as f:
        f.write(json_object)


def generate_hash(record):
    key = f"{record}"
    return hashlib.md5(key.encode()).hexdigest()

def createTables(cur, tables_present):
    global ERRORS, ALLTABLES, alter_user_table_query
    try:
        for key, value in ALLTABLES.items():
            if key not in tables_present:
                cur.execute(value)
    except Exception as e:
        ERRORS = 1
        st.error(f"Error at {key}")
        return

def insertToDb(con, cur, key, data):
    global ERRORS
    data = data.replace("'", "")
    try:
        cur.execute(INSERTQUERY.format(key, data))
        con.commit()
    except Exception as e:
        ERRORS = 1
        st.error(f"{e}, {key}, {data}")

def insertValues(con, cur, user_data, resume_counter):
    global ALLTABLES, INSERTQUERY
    for key, value in ALLTABLES.items():
        if key == 'user':
            inp_data = f"""
                        "{user_data.get('Email', '')}",
                        "{user_data.get('Name', '')}",
                        "{user_data.get('Phone', '')}",
                        "{user_data.get('Location', '')}",
                        "{user_data.get('LinkedIn', '')}",
                        "{user_data.get('GitHub', '')}",
                        "{user_data.get('Summary', '')}",
                        "{resume_counter}"
                        """
            insertToDb(con, cur, key, inp_data)
        if key == 'userskills':
            for skill in user_data['Skills']:
                hash_key = generate_hash(skill)
                not_exists = cur.execute(f"SELECT * FROM userskills WHERE skill_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                "{hash_key}",
                                "{skill}",
                                "{resume_counter}",
                                "{user_data.get('Email', '')}"
                                """
                    insertToDb(con, cur, key, inp_data)
        if key == 'workexp':
            for work_experience in user_data['WorkExperience']:
                hash_key = generate_hash(work_experience)
                not_exists = cur.execute(f"SELECT * FROM workexp WHERE workexp_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                "{hash_key}",
                                "{work_experience.get('workexp_company', '')}",
                                "{work_experience.get('workexp_role', '')}",
                                "{work_experience.get('workexp_location', '')}",
                                "{work_experience.get('workexp_from', '')}",
                                "{work_experience.get('workexp_to', '')}",
                                "{work_experience.get('workexp_description', '')}",
                                "{resume_counter}",
                                "{user_data.get('Email', '')}"
                                """
                    insertToDb(con, cur, key, inp_data)
        if key == 'proj':
            for project in user_data['Projects']:
                hash_key = generate_hash(project)
                not_exists = cur.execute(f"SELECT * FROM proj WHERE proj_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                "{hash_key}",
                                "{project.get('proj_title', '')}",
                                "{project.get('proj_link', '')}",
                                "{project.get('proj_from', '')}",
                                "{project.get('proj_to', '')}",
                                "{project.get('proj_description', '')}",
                                "{resume_counter}",
                                "{user_data.get('Email', '')}"
                                """
                    insertToDb(con, cur, key, inp_data)
        if key == 'edu':
            for education in user_data['Education']:
                hash_key = generate_hash(education)
                not_exists = cur.execute(f"SELECT * FROM edu WHERE edu_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                "{hash_key}",
                                "{education.get('edu_institution', '')}",
                                "{education.get('edu_degree', '')}",
                                "{education.get('edu_major', '')}",
                                "{education.get('edu_from', '')}",
                                "{education.get('edu_to', '')}",
                                "{resume_counter}",
                                "{user_data.get('Email', '')}"
                                """
                    insertToDb(con, cur, key, inp_data)


def addToDb(data, jsonfile):
    global ERRORS

    resume_counter = get_resume_counter(jsonfile)

    try:
        list_tables_query = """SELECT name FROM sqlite_master
                           WHERE type='table';"""

        cur.execute(list_tables_query)
        tables = [table[0] for table in cur.fetchall()]
        createTables(cur, tables_present=tables)
    except:
        st.toast("No Databases found yet, turn on 'Edit Mode' and add data first")
    
    

    insertValues(CONN, cur, data, resume_counter)
    st.toast(f"Added data to database with resumeID: {resume_counter}")

    if not ERRORS:
        resume_counter += 1
        put_resume_counter(resume_counter, jsonfile)
    CONN.close()

