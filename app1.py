import streamlit as st
import json
import os
from datetime import date
from PIL import Image
import io
import base64

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

def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def save_upload_file(uploaded_file):
    """Save uploaded file and return base64 encoded path"""
    file_path = f"uploads/{uploaded_file.name}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

if check_password():
    st.set_page_config(layout="wide")
    st.title("💌 Letters to Bub")
    
    # Initialize storage
    LETTERS_FILE = "letters.json"
    MEMORIES_FILE = "memories.json"
    FLOWERS_FILE = "flowers.json"
    
    for file in [LETTERS_FILE, MEMORIES_FILE, FLOWERS_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump([], f)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["💌 Letters to Bub", "🌅 Our Memories", "🌸 Flowers for just for you"])
    
    # ===== TAB 1: LETTERS TO BUB =====
    with tab1:
        st.header("✍️ Write a Letter")
        
        with st.form("letter_form"):
            d = st.date_input("Date", date.today())
            title = st.text_input("Entry Title")
            msg = st.text_area("Message", height=200)
            submitted = st.form_submit_button("Post Letter")
            
            if submitted and title and msg:
                letters = load_json(LETTERS_FILE)
                letters.insert(0, {
                    "date": str(d),
                    "title": title,
                    "content": msg,
                    "id": len(letters)
                })
                save_json(LETTERS_FILE, letters)
                st.success("Letter posted! 💌")
                st.rerun()
        
        st.divider()
        st.header("📖 Your Letters")
        
        letters = load_json(LETTERS_FILE)
        if letters:
            for idx, letter in enumerate(letters):
                with st.expander(f"{letter['date']} | {letter['title']}"):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(letter['content'])
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_letter_{idx}"):
                            letters.pop(idx)
                            save_json(LETTERS_FILE, letters)
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("No letters yet. Write your first letter! 💌")
    
    # ===== TAB 2: OUR MEMORIES =====
    with tab2:
        st.header("📸 Upload Your Memory")
        
        with st.form("memory_form"):
            caption = st.text_input("Memory Caption")
            uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "gif"])
            submitted = st.form_submit_button("Upload Memory")
            
            if submitted and uploaded_file and caption:
                file_path = save_upload_file(uploaded_file)
                memories = load_json(MEMORIES_FILE)
                memories.insert(0, {
                    "caption": caption,
                    "file": file_path,
                    "id": len(memories)
                })
                save_json(MEMORIES_FILE, memories)
                st.success("Memory saved! 🌅")
                st.rerun()
        
        st.divider()
        st.header("💭 Our Memories")
        
        memories = load_json(MEMORIES_FILE)
        if memories:
            cols = st.columns(3)
            for idx, memory in enumerate(memories):
                with cols[idx % 3]:
                    if os.path.exists(memory['file']):
                        st.image(memory['file'], use_column_width=True)
                        st.caption(memory['caption'])
                        if st.button("🗑️ Delete", key=f"delete_memory_{idx}"):
                            memories.pop(idx)
                            save_json(MEMORIES_FILE, memories)
                            if os.path.exists(memory['file']):
                                os.remove(memory['file'])
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("No memories yet. Upload your first one! 📸")
    
    # ===== TAB 3: FLOWERS =====
    with tab3:
        st.header("🌸 Upload a Flower Photo")
        
        with st.form("flower_form"):
            caption = st.text_input("Flower Caption/Story")
            uploaded_file = st.file_uploader("Choose a flower image", type=["jpg", "jpeg", "png", "gif"], key="flower_uploader")
            submitted = st.form_submit_button("Upload Flower")
            
            if submitted and uploaded_file and caption:
                file_path = save_upload_file(uploaded_file)
                flowers = load_json(FLOWERS_FILE)
                flowers.insert(0, {
                    "caption": caption,
                    "file": file_path,
                    "id": len(flowers)
                })
                save_json(FLOWERS_FILE, flowers)
                st.success("Flower added! 🌸")
                st.rerun()
        
        st.divider()
        st.header("🌹 Flowers Just for You")
        
        flowers = load_json(FLOWERS_FILE)
        if flowers:
            cols = st.columns(3)
            for idx, flower in enumerate(flowers):
                with cols[idx % 3]:
                    if os.path.exists(flower['file']):
                        st.image(flower['file'], use_column_width=True)
                        st.caption(flower['caption'])
                        if st.button("🗑️ Delete", key=f"delete_flower_{idx}"):
                            flowers.pop(idx)
                            save_json(FLOWERS_FILE, flowers)
                            if os.path.exists(flower['file']):
                                os.remove(flower['file'])
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("No flowers yet. Upload your first one! 🌸")
