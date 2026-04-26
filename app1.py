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
    
    # Custom CSS for turquoise pastel theme
    st.markdown("""
    <style>
    :root {
        --primary-color: #7DD3C0;
        --secondary-color: #FFB6D9;
        --accent-color: #FFE5B4;
    }
    
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #F0FFFE 0%, #F5F0FF 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #4A9B8E !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #E8F8F5;
        border-radius: 8px;
        color: #4A9B8E;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #7DD3C0 !important;
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #7DD3C0;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #5DBDA8;
        box-shadow: 0 4px 12px rgba(125, 211, 192, 0.3);
    }
    
    /* Form inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #F0FFFE !important;
        border: 2px solid #7DD3C0 !important;
        border-radius: 8px;
        color: #2D6A60 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #E8F8F5;
        border-radius: 8px;
        border-left: 4px solid #7DD3C0;
    }
    
    /* Success/Info messages */
    .stSuccess {
        background-color: #D4F9F5 !important;
        border-left: 4px solid #7DD3C0;
    }
    
    .stInfo {
        background-color: #FFF0F5 !important;
        border-left: 4px solid #FFB6D9;
    }
    
    /* Dividers */
    .stDivider {
        border-color: #7DD3C0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("💌 Letters to Bub")
    
    # Initialize storage
    LETTERS_FILE = "letters.json"
    MEMORIES_FILE = "memories.json"
    FLOWERS_FILE = "flowers.json"
    REMINDERS_FILE = "reminders.json"
    
    for file in [LETTERS_FILE, MEMORIES_FILE, FLOWERS_FILE, REMINDERS_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump([], f)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💌 Letters to Bub", 
        "🌅 Our Memories", 
        "🌸 Flowers for just for you",
        "✨ Everything that reminds me of you"
    ])
    
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
    
    # ===== TAB 4: EVERYTHING THAT REMINDS ME OF YOU =====
    with tab4:
        st.header("✨ Everything That Reminds Me of You")
        st.markdown("_Share poems, pictures, and memories all in one beautiful place_")
        
        st.subheader("📝 Add a New Entry")
        
        with st.form("reminder_form"):
            col1, col2 = st.columns(2)
            with col1:
                reminder_type = st.radio("What would you like to add?", 
                                        ["📝 Poem", "🖼️ Picture"])
            with col2:
                st.write("")
            
            if reminder_type == "📝 Poem":
                title = st.text_input("Poem Title")
                content = st.text_area("Write your poem", height=200)
                caption = st.text_input("Caption (optional)")
                submitted = st.form_submit_button("📝 Post Poem")
                
                if submitted and title and content:
                    reminders = load_json(REMINDERS_FILE)
                    reminders.insert(0, {
                        "type": "poem",
                        "title": title,
                        "content": content,
                        "caption": caption,
                        "id": len(reminders)
                    })
                    save_json(REMINDERS_FILE, reminders)
                    st.success("Poem added! 📝")
                    st.rerun()
            
            else:  # Picture
                picture_title = st.text_input("Picture Title")
                picture_caption = st.text_input("Picture Caption")
                uploaded_file = st.file_uploader("Choose a picture", type=["jpg", "jpeg", "png", "gif"], key="reminder_uploader")
                submitted = st.form_submit_button("🖼️ Post Picture")
                
                if submitted and uploaded_file and picture_title:
                    file_path = save_upload_file(uploaded_file)
                    reminders = load_json(REMINDERS_FILE)
                    reminders.insert(0, {
                        "type": "picture",
                        "title": picture_title,
                        "caption": picture_caption,
                        "file": file_path,
                        "id": len(reminders)
                    })
                    save_json(REMINDERS_FILE, reminders)
                    st.success("Picture added! 🖼️")
                    st.rerun()
        
        st.divider()
        st.subheader("💫 Your Collection")
        
        reminders = load_json(REMINDERS_FILE)
        if reminders:
            for idx, reminder in enumerate(reminders):
                if reminder["type"] == "poem":
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(125, 211, 192, 0.1), rgba(255, 182, 217, 0.1));
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 5px solid #7DD3C0;
                        margin-bottom: 15px;
                    ">
                        <h4 style="color: #4A9B8E; margin: 0 0 10px 0;">📝 {reminder['title']}</h4>
                        <p style="color: #2D6A60; white-space: pre-wrap; line-height: 1.6;">{reminder['content']}</p>
                        {f"<p style='color: #FFB6D9; font-size: 0.9em; margin-top: 10px;'>{reminder['caption']}</p>" if reminder.get('caption') else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_reminder_{idx}"):
                            reminders.pop(idx)
                            save_json(REMINDERS_FILE, reminders)
                            st.success("Deleted!")
                            st.rerun()
                
                else:  # Picture
                    if os.path.exists(reminder['file']):
                        st.image(reminder['file'], use_column_width=True)
                        st.markdown(f"<h4 style='color: #4A9B8E;'>{reminder['title']}</h4>", unsafe_allow_html=True)
                        if reminder.get('caption'):
                            st.markdown(f"<p style='color: #FFB6D9;'>{reminder['caption']}</p>", unsafe_allow_html=True)
                        
                        if st.button("🗑️ Delete", key=f"delete_reminder_{idx}"):
                            reminders.pop(idx)
                            save_json(REMINDERS_FILE, reminders)
                            if os.path.exists(reminder['file']):
                                os.remove(reminder['file'])
                            st.success("Deleted!")
                            st.rerun()
                        
                        st.divider()
        else:
            st.info("No entries yet. Start adding your memories! ✨")
