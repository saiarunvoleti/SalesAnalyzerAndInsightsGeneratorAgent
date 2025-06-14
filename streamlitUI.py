import streamlit as st
import random
import requests
import imghdr
from io import BytesIO
import base64

# ---------- Setup ----------
st.set_page_config(layout="wide")

st.markdown(
    "<h1 style='text-align: left;'>Sales Insights Agent</h1>",
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "widgets" not in st.session_state:
    st.session_state.widgets = [
        {"label": "Widget 1", "image": "./sales_profit_quarters.png"},
        {"label": "Widget 2", "image": f"./profit_trends.png"}
    ]

url = "https://saiarunvoleti1.pythonanywhere.com/testLLM"

# ---------- Layout ----------
left_col, right_col = st.columns([2, 1])

# ---------- Right: Chat Interface ----------
with right_col:
    st.markdown("### 🤖 Chatbot")
    with st.container(height=400, border=True):
        for msg in st.session_state.messages:
            st.markdown(f"**You:** {msg['user']}")
            st.markdown(f"**Bot:** {msg['bot']}")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            # Simulate a response (you can replace this with API call)
            data = user_input
            response = requests.post(url, data=data).text  # or use data=data for form-encoded
            bot_response = response
            st.session_state.messages.append({"user": user_input, "bot": bot_response})
            st.rerun()

# ---------- Right: Widgets + Add Widget ----------
with left_col:
    st.markdown("### 🧩 Widgets")

    for widget in st.session_state.widgets:
        with st.container(border=True,height=400):
            try:
                st.markdown(f"**{widget['label']}**")
                st.image(widget['image'], width=500)
            except Exception as e:
                print(e)

    # Add new widget
    with st.expander("➕ Add Widget"):
        new_label = st.text_input("Enter widget label", key="new_widget_label")
        if st.button("Add", key="add_widget_button") and new_label:
            print(new_label)
            data = new_label
            # st.button(disabled=True)
            response = requests.post(url, data=data).text  # or use data=data for form-encoded
            try:
                # response = response.strip()
                image_data = base64.b64decode(response)
                # Detect format (returns 'png', 'jpeg', etc.)
                image_format = imghdr.what(None, h=image_data)
                new_image = response
                print(new_image)
                new_image = f"data:image/{image_format};base64,{response}"
                st.session_state.widgets.append({"label": new_label, "image": new_image})
                st.rerun()
                # st.markdown(f"**{new_label}**")
                # st.image(new_image, width=500)
            except Exception as e:
                print(e)
