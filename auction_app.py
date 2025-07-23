import base64

import psycopg2
import streamlit as st


# Helper function to convert image to base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# Background functions
def set_background(image_path):
    img_base64 = get_base64(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# db_connection = psycopg2.connect(
#     host="localhost",  # or your DB host
#     port=5432,
#     database="auction_app",
#     user="postgres",
#     password="auction"
# )

if "current_bid" not in st.session_state:
    st.session_state.current_bid = 1000  # starting bid


def login():
    st.markdown("<h1 style='color: black;'>Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    set_background("/home/yadukrishnan/Downloads/auction.jpg")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.role = "admin"
            # Fetch players only once
            if "players_data" not in st.session_state:
                # cur = db_connection.cursor()
                # cur.execute("SELECT * FROM players_list")
                st.session_state.players_data = [(1, 'Nikil', '/home/yadukrishnan/Desktop/PLayercards/KMPL_S5/1.jpg')]
        elif username == "user" and password == "user123":
            st.session_state.role = "user"
        st.rerun()


def admin_view():
    result = st.session_state.get("players_data", [])
    image_url = result[0][2]
    print(image_url)
    print("Result = ", result)
    print(type(result))
    set_background("/home/yadukrishnan/Downloads/player auction.webp")
    st.markdown("<h1 style='color: white;'>Admin Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: white;'>Welcome Admin</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src='data:image/png;base64,{get_base64(image_url)}' style='width: 300px; height: 300px;'>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
        <div style='text-align: center;'>
        <p style='font-size: 20px; font-weight: bold; color: white;'>{result[0][1]}</p>
        <h2 style='margin: 10px; color: white;'>₹{st.session_state.current_bid}</h2>
        </div>
    """, unsafe_allow_html=True)

    # Centered plus button
    if st.button("➕", help="Increase bid by 500"):
        if st.session_state.current_bid < 2000:
            st.session_state.current_bid += 100
        elif st.session_state.current_bid < 5000:
            st.session_state.current_bid += 200
        else:
            st.session_state.current_bid += 500
        st.rerun()


def user_view():
    st.title("User Dashboard")
    st.write("Welcome, User!")


# Main routing logic
if "role" not in st.session_state:
    login()
elif st.session_state.role == "admin":
    admin_view()
else:
    user_view()
