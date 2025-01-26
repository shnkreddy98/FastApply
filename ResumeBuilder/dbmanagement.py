import sqlite3
import streamlit as st
import hashlib

INSERTQUERY = "INSERT OR IGNORE INTO {} VALUES ({});"

user_table_query = """CREATE TABLE IF NOT EXISTS user (
                      user_name TEXT NOT NULL,
                      user_email TEXT UNIQUE NOT NULL,
                      user_phone TEXT,
                      user_city TEXT,
                      user_linkedin_link TEXT,
                      user_github_link TEXT,
                      user_summary TEXT);
                  """

user_skill_table_query = """CREATE TABLE IF NOT EXISTS userskills (
                            skill_id TEXT PRIMARY KEY,
                            skill_name TEXT NOT NULL,
                            user_email TEXT,
                            FOREIGN KEY(user_email) REFERENCES user(user_email) ON DELETE CASCADE);
                         """

workexp_table_query = """CREATE TABLE IF NOT EXISTS workexp (
                         workexp_id TEXT PRIMARY KEY,
                         workexp_company TEXT NOT NULL,
                         workexp_role TEXT NOT NULL,
                         workexp_location TEXT,
                         workexp_from DATE,
                         workexp_to DATE,
                         workexp_description TEXT,
                         user_email TEXT NOT NULL,
                         FOREIGN KEY(user_email) REFERENCES user(user_email) ON DELETE CASCADE);
                      """

proj_table_query = """CREATE TABLE IF NOT EXISTS proj (
                      proj_id TEXT PRIMARY KEY,
                      proj_title TEXT NOT NULL,
                      proj_link TEXT,
                      proj_from DATE,
                      proj_to DATE,
                      proj_description TEXT,
                      user_email TEXT NOT NULL,
                      FOREIGN KEY(user_email) REFERENCES user(user_email) ON DELETE CASCADE);
                  """
      
edu_table_query = """CREATE TABLE IF NOT EXISTS edu ( 
                     edu_id TEXT PRIMARY KEY,
                     edu_institution TEXT NOT NULL,
                     edu_degree TEXT,
                     edu_course TEXT,
                     edu_from DATE,
                     edu_to DATE,
                     user_email TEXT NOT NULL,
                     FOREIGN KEY(user_email) REFERENCES user(user_email) ON DELETE CASCADE);
                 """

jobs_table_query = """CREATE TABLE IF NOT EXISTS jobs (
                      job_link TEXT NOT NULL,
                      job_description TEXT,
                      company_name TEXT,
                      user_email TEXT NOT NULL,
                      FOREIGN KEY(user_email) REFERENCES user(user_email) ON DELETE CASCADE);
                   """

companies_table_query = """CREATE TABLE IF NOT EXISTS companies (
                           company_name TEXT NOT NULL UNIQUE,
                           job_link TEXT NOT NULL,
                           FOREIGN KEY(job_link) REFERENCES jobs(job_link) ON DELETE CASCADE);
                        """

hiring_manager_table_query = """CREATE TABLE IF NOT EXISTS hiringmanagers (
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

def generate_hash(record):
    key = f"{record}"
    return hashlib.md5(key.encode()).hexdigest()

def createTables(cur, tables_present):
    global ALLTABLES, alter_user_table_query
    try:
        for key, value in ALLTABLES.items():
            if key not in tables_present:
                cur.execute(value)
    except Exception as e:
        st.error(f"Error at {key}")
        return

def insertToDb(con, cur, key, data):
    try:
        cur.execute(INSERTQUERY.format(key, data))
        con.commit()
    except Exception as e:
        st.error(f"{e}, {key}")

def insertValues(con, cur, user_data):
    global ALLTABLES, INSERTQUERY
    for key, value in ALLTABLES.items():
        if key == 'user':
            inp_data = f"""
                        '{user_data.get('Name', '')}',
                        '{user_data.get('Email', '')}',
                        '{user_data.get('Phone', '')}',
                        '{user_data.get('Location', '')}',
                        '{user_data.get('LinkedIn', '')}',
                        '{user_data.get('GitHub', '')}',
                        '{user_data.get('Summary', '')}'
                        """
            insertToDb(con, cur, key, inp_data)
        if key == 'userskills':
            for skill in user_data['Skills']:
                hash_key = generate_hash(skill)
                not_exists = cur.execute(f"SELECT * FROM userskills WHERE skill_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                '{hash_key}',
                                '{skill}',
                                '{user_data.get('Email', '')}'
                                """
                    insertToDb(con, cur, key, inp_data)
        if key == 'workexp':
            for work_experience in user_data['WorkExperience']:
                hash_key = generate_hash(work_experience)
                not_exists = cur.execute(f"SELECT * FROM workexp WHERE workexp_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                '{hash_key}',
                                '{work_experience.get('workexp_company', '')}',
                                '{work_experience.get('workexp_role', '')}',
                                '{work_experience.get('workexp_location', '')}',
                                '{work_experience.get('workexp_from', '')}',
                                '{work_experience.get('workexp_to', '')}',
                                '{work_experience.get('workexp_description', '')}',
                                '{user_data.get('Email', '')}'
                                """
                    insertToDb(con, cur, key, inp_data)
        if key == 'proj':
            for project in user_data['Projects']:
                hash_key = generate_hash(project)
                not_exists = cur.execute(f"SELECT * FROM proj WHERE proj_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                '{hash_key}',
                                '{project.get('proj_title', '')}',
                                '{project.get('proj_link', '')}',
                                '{project.get('proj_from', '')}',
                                '{project.get('proj_to', '')}',
                                '{project.get('proj_description', '')}',
                                '{user_data.get('Email', '')}'
                                """
                    insertToDb(con, cur, key, inp_data)
        if key == 'edu':
            for education in user_data['Education']:
                hash_key = generate_hash(education)
                not_exists = cur.execute(f"SELECT * FROM edu WHERE edu_id = '{hash_key}';")
                if not_exists:
                    inp_data = f"""
                                '{hash_key}',
                                '{education.get('edu_institution', '')}',
                                '{education.get('edu_degree', '')}',
                                '{education.get('edu_major', '')}',
                                '{education.get('edu_from', '')}',
                                '{education.get('edu_to', '')}',
                                '{user_data.get('Email', '')}'
                                """
                    insertToDb(con, cur, key, inp_data)

        cur.execute(f"SELECT * FROM {key};")
        st.write(cur.fetchall())


def addToDb(db_path, data):
    con = sqlite3.connect(db_path)
    con.execute('PRAGMA foreign_keys = ON;')
    cur = con.cursor()

    st.write(data)
    list_tables_query = """Select name FROM sqlite_master
                           WHERE type='table';"""

    cur.execute(list_tables_query)
    tables = [table[0] for table in cur.fetchall()]
    createTables(cur, tables_present=tables)

    insertValues(con, cur, data)
    

