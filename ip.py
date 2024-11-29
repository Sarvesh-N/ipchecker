import socket
from googlesearch import search
import streamlit as st

def get_first_website(website_name):
    query = f"{website_name} official website"
    websites = [] 
    try:
        for url in search(query, num_results=5):
            websites.append(url)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    return websites

def executer(website_name, sus):
    legitIp = {}
    try:
        susIp = socket.gethostbyname(sus.split("//")[1].split("/")[0])
    except Exception as e:
        st.error("Error occurred while resolving suspect link.")
        return
    
    websites = get_first_website(website_name)
    if websites:
        for i in websites:
            try:
                j = (i.split("//")[1]).split("/")[0]
                resolved_ip = socket.gethostbyname(j)
                legitIp[i] = resolved_ip
            except Exception as e:
                st.error(f"Error occurred while resolving website IP: {e}")
                continue
        
        if susIp in legitIp.values():
            st.success("It's legit..!")
        else:
            st.warning("Sus!!")
        
        st.info(f"Suspect IP: {susIp}")  # Display suspect IP
        for site, ip in legitIp.items():
            st.info(f"Visited website: {site}, Resolved IP: {ip}")  # Display visited website and resolved IP
    else:
        st.warning(f"No websites found for {website_name}")

# Streamlit UI
st.title("IP Legitimacy Checker")

website_name = st.text_input("Website Name", "")
suspect_link = st.text_input("Suspect Link", "")

if st.button("CHECK"):
    if website_name and suspect_link:
        executer(website_name, suspect_link)
    else:
        st.error("Please fill in both fields")
