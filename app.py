import streamlit as st
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="HomeBrain Pro-Registry", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 2. SIDEBAR: BUSINESS REGISTRATION ---
with st.sidebar:
    st.header("For Businesses")
    with st.form("biz_form"):
        st.subheader("Register Your Card")
        biz_name = st.text_input("Business Name")
        spec = st.selectbox("Specialty", ["Plumbing", "Electrical", "Landscaping", "Civil Engineering"])
        phone = st.text_input("Phone")
        bio = st.text_area("Bio/Details")
        submit_biz = st.form_submit_button("Join Registry")

        if submit_biz:
            # Create a small dataframe to save
            new_data = pd.DataFrame([{"Business Name": biz_name, "Specialty": spec, "Phone": phone, "Bio": bio}])
            # Logic to append to your Google Sheet
            # (Streamlit GSheets connection makes this easy!)
            st.success("Card Published!")

# --- 3. MAIN PAGE: NEIGHBOR SEARCH ---
st.title("🏡 HomeBrain: Neighborhood Pro-Registry")

# Load the existing cards from the sheet
existing_data = conn.read(worksheet="Sheet1")

search_query = st.text_input("Ask the Neighborhood AI:", placeholder="E.g., 'I have a leak in my front yard and need a landscape engineer'")

if search_query:
    # Use Gemini to find the best match from your data
    context = existing_data.to_string()
    prompt = f"""
    Below is a list of local businesses:
    {context}
    
    A neighbor is asking: '{search_query}'
    Which business should they contact and why? Answer like a helpful neighbor.
    """
    
    with st.spinner("AI is thinking..."):
        response = model.generate_content(prompt)
        st.write(response.text)

# --- 4. DISPLAY ALL CARDS ---
st.divider()
st.subheader("Available Local Pros")
st.dataframe(existing_data, use_container_width=True)
