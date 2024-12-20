import streamlit as st
import os

from modules.emailRecipients import emailRecipients

if __name__ == "__main__":
    recruitername = st.text_input("Enter the full name of the employee")
    company = st.text_input("Enter the company name")
    domain = st.text_input("Default to .com change if required")

    FROMADDR = st.text_input("Email Address to send the email from")

    subject = st.text_input("Enter Subject here")
    body = st.text_input("Enter the body content")
    resumeuploadfile = st.file_uploader("Choose a Resume or start filling details")

    if st.button("Send"):

        attachmentfilepath = f"FastApply/outputs/{resumeuploadfile.name}"

        b = resumeuploadfile.getvalue()
        with open(attachmentfilepath, "wb") as f:
            f.write(b)

        possible_emails = emailRecipients.get_possible_emails(recruitername, company, domain)
        valid_ids = emailRecipients.get_valid_emails(possible_emails, from_addr=FROMADDR)

        if len(valid_ids)==0:
            st.write(f"None of the emails were validated, trying all emails")
            res = emailRecipients.send_emails(FROMADDR, possible_emails, subject, body, attachmentfilepath)

        else:
            res = emailRecipients.send_emails(FROMADDR, valid_ids, subject, body, attachmentfilepath)

        if res:
            st.write(f"Email successfully sent")
        else:
            st.write(f"None of the emails worked")



