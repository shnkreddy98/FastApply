import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class requestOpenAI:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API"),  # This is the default and can be omitted
        )
    
    def get_new_resume(self, user_data, work_exp_data, projects_data, education_data, jd):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": """You are a Resume Builder Assistant I will give you my resume and a 
                            Job Description. please help me create a new resume which covers almost 
                            all technologies and tasks mentioned in the Job Description. Try to retain the present 
                            roles and descriptions for experience and projects section, but if much can't 
                            be done to match the job description change the roles and description for project 
                            and work experience. Overall, once the resume is done, it should pass the 
                            ATS for the given job description and should be intruiging and realisitc 
                            so that if i get the interview you can also help me answer interview questions.
                            You will also help me come up with set of questions that are most likely to be asked 
                            in the technical interview."""
            },
            {
                "role": "user",
                "content": f""""Hello I have the data below in a dictionary format, please keep the same key 
                            but change the values according to the job description and reply with just the data 
                            and no extra content before or after the message. Make sure the content 
                            will pass ATS and keep the content length similar to what is already there. 
                            Here is the data: ({user_data}, {work_exp_data}, {projects_data}, {education_data}) 
                            and here is the Job Description: {jd}"""
            }],
        )
        return response

