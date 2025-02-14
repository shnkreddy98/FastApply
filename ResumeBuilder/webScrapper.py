from selenium import webdriver
from html2text import html2text
from bs4 import BeautifulSoup
import json
import os
import streamlit as st

def writeJD(text_content, company_name):
    company_path = f"./ResumeBuilder/outputs/{company_name}"
    if not os.path.exists(company_path):
        os.mkdir(company_path)
    with open(f"{company_path}/JD.txt", "w+") as f:
        f.write(text_content)
    st.toast(f"JD created at {company_path}")

def getContent(url, company_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    
    text_content = html2text(html_content)
    if len(text_content) > 10:
        writeJD(text_content, company_name)
        return text_content
    else:
        soup = BeautifulSoup(html_content, features="lxml")

        data = json.loads(soup.find('script', type='application/ld+json').string)
        writeJD(data['description'], company_name)
        return data['description']

