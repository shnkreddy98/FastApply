import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

APIRUN = int(os.getenv("APIRUN"))

def replace_env(file, key, value):
    with open(file, "r") as f:
        lines = f.readlines()
    index=[i for i, line in enumerate(lines) if line.startswith(key)]
    lines[index[0]]=f"{key}={str(value)}\n"
    with open(file, "w") as f:
        f.writelines(lines)
    

class requestOpenAI:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API"),  # This is the default and can be omitted
        )
    
    def get_new_resume(self, data, jd):
        global APIRUN
        APIRUN += 1
        replace_env(".env", "APIRUN", APIRUN)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": f"""
                            Your task is to generate a resume that will help me secure a job. 
                            I will provide you with two sets of information. The first object includes my work experience, 
                            educational background, skills, and any relevant certifications or awards as a resume. 
                            The second object is a detailed description of the job I'm applying for, including the company name, 
                            job title, responsibilities, and required qualifications. Based on this information, create a resume
                            that highlights the skills and experiences that align most closely with the job requirements. 
                            Emphasize the value I can bring to the company and how my qualifications make me a strong candidate 
                            for the position. The language should be formal, concise, and positive.
                            Try to retain the present roles for experience and present description and links for projects section. 
                            Overall, once the resume is done, it should pass the ATS for the given job description and should be 
                            intruiging and realisitc so that if i get the interview you can also help me answer interview questions.
                            You will also help me come up with set of questions that are most likely to be asked 
                            in the technical interview. if the resume is short add more points."""
            },
            {
                "role": "user",
                "content": f""""Hello I have the data below in a dictionary format, please keep the same key 
                            but change the values according to the job description and reply with just the data 
                            and no extra content before or after the message. Make sure the content 
                            will pass ATS and keep the content length similar to what is already there. 
                            Here is the data: ({data}) 
                            and here is the Job Description: {jd}. Make sure the data has double quotes for dictionary 
                            and inside dictionary the content has single quotes."""
            }],
        )
        if isinstance(response, str):
            requestOpenAI.get_new_resume(data, jd)
        
        return response

