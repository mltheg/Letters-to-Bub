import streamlit as st
import json
import os
from datetime import date

# --- SET YOUR PASSWORD HERE ---
MY_PASSWORD = "10282025" 

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("🔒 Access Protected")
        pwd = st.text_input("Enter Password to View Journal", type="password")
        if st.button("Unlock"):
            if pwd == MY_PASSWORD:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Wrong password!")
        return False
    return True

if check_password():
    st.title("💌 Letter to Bub")
    
    # Initialize storage
    DB_FILE = "journal.json"
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: json.dump([], f)

    # Input Section
    with st.expander("✍️ Write Today's Letter", expanded=True):
        d = st.date_input("Date", date.today())
        title = st.text_input("Entry Title")
        msg = st.text_area("Message")
        if st.button("Post to Journal"):
            entries = json.load(open(DB_FILE))
            entries.insert(0, {"title": f"{d} | {title}", "content": msg})
            json.dump(entries, open(DB_FILE, "w"))
            st.success("Posted!")
            st.rerun()

    # Display Section
    st.divider()
    for e in json.load(open(DB_FILE)):
        with st.expander(e['title']):
            st.write(e['content'])
