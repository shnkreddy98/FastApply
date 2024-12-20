import sqlite3

class accessDB:
    def __init__(self):
        try:
            # Establish connection to SQLite database
            self.con = sqlite3.connect("/Users/reddy/Documents/GitHub/FastApply/FastApply/dbs/FastApply.db")
            self.con.execute('PRAGMA foreign_keys = ON;')  # Enforce foreign key constraints
            self.cur = self.con.cursor()
            print("Database connection established successfully.")
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")
            self.con = None
            self.cur = None

    def close_connection(self):
        if self.con:
            self.con.close()
            print("Database connection closed.")

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS user (
                        email_id VARCHAR(255) PRIMARY KEY,
                        name VARCHAR(255),
                        user_location VARCHAR(255),
                        linkedin_link VARCHAR(255),
                        phone VARCHAR(20),
                        summary TEXT,
                        skills TEXT);
                    """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS work (
                        work_exp_id INTEGER PRIMARY KEY,
                        company VARCHAR(255),
                        role VARCHAR(255),
                        work_location VARCHAR(255),
                        work_start_date DATE,
                        work_end_date DATE,
                        work_description TEXT,
                        user_id VARCHAR(255),
                        FOREIGN KEY(user_id) REFERENCES user(email_id) ON DELETE CASCADE);
                    """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS project (
                        project_id INTEGER PRIMARY KEY,
                        project_name VARCHAR(255),
                        project_link VARCHAR(255),
                        project_start_date DATE,
                        project_end_date DATE,
                        project_description TEXT,
                        user_id VARCHAR(255),
                        FOREIGN KEY(user_id) REFERENCES user(email_id) ON DELETE CASCADE);
                    """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS education (
                        education_id INTEGER PRIMARY KEY,
                        institution_name VARCHAR(255),
                        course VARCHAR(255),
                        education_start_date DATE,
                        education_end_date DATE,
                        user_id VARCHAR(255),
                        FOREIGN KEY(user_id) REFERENCES user(email_id) ON DELETE CASCADE);
                    """)

        self.cur.execute("""CREATE TABLE IF NOT EXISTS jobs (
                        job_id INTEGER PRIMARY KEY,
                        job_link VARCHAR(255),
                        job_description TEXT,
                        hiring_manager_fn VARCHAR(255),
                        hiring_manager_ln VARCHAR(255),
                        generated_questions TEXT,
                        chatgpt_checkpoint TEXT,
                        user_id VARCHAR(255),
                        FOREIGN KEY(user_id) REFERENCES user(email_id) ON DELETE CASCADE);
                    """)
        
    def insert_values(self, user_data, work_exp_data, projects_data, education_data):
        self.cur.execute(f"""INSERT INTO 
                         user (email_id, name, user_location, 
                         linkedin_link, phone, summary, skills)
                         VALUES ({user_data['user_name']}, {user_data['user_email']}, {user_data['user_phone']}', 
                         {user_data['user_city']}, {user_data['user_linkedin_link']}, 
                         {user_data['user_summary']}, {user_data['user_skills']});
                         """)
        self.cur.execute(f"""INSERT INTO 
                         work (work_exp_id, company, role, 
                         work_location, work_start_date, 
                         work_end_date, work_description, user_id)
                         VALUES ({work_exp_data['user_name']}, {user_data['user_email']}, {user_data['user_phone']}', 
                         {user_data['user_city']}, {user_data['user_linkedin_link']}, 
                         {user_data['user_summary']}, {user_data['user_skills']});
                         """)
        self.cur.execute(f"""INSERT INTO 
                         project (email_id, name, user_location, 
                         linkedin_link, phone, summary, skills)
                         VALUES (user_data{['user_name']}, {user_data['user_email']}, 'user_data{['user_phone']}', 
                         {user_data['user_city']}, {user_data['user_linkedin_link']}, 
                         {user_data['user_summary']}, {user_data['user_skills']});
                         """)
        self.cur.execute(f"""INSERT INTO 
                         education (email_id, name, user_location, 
                         linkedin_link, phone, summary, skills)
                         VALUES (user_data{['user_name']}, {user_data['user_email']}, 'user_data{['user_phone']}', 
                         {user_data['user_city']}, {user_data['user_linkedin_link']}, 
                         {user_data['user_summary']}, {user_data['user_skills']});
                         """)
        self.cur.execute(f"""INSERT INTO 
                         usejobsr (email_id, name, user_location, 
                         linkedin_link, phone, summary, skills)
                         VALUES (user_data{['user_name']}, {user_data['user_email']}, 'user_data{['user_phone']}', 
                         {user_data['user_city']}, {user_data['user_linkedin_link']}, 
                         {user_data['user_summary']}, {user_data['user_skills']});
                         """)
        

