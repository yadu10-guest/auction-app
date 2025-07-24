import psycopg2
import streamlit as st


# Background functions
def set_background(background_image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


db_connection = psycopg2.connect(
    host=st.secrets["DB_HOST"],
    port=st.secrets["DB_PORT"],
    database=st.secrets["DB_NAME"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"]
)

if "current_bid" not in st.session_state:
    st.session_state.current_bid = 1000  # starting bid


def login():
    st.markdown("<h1 style='color: black;'>Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    set_background("https://raw.githubusercontent.com/yadu10-guest/auction-app/refs/heads/master/images/auction.jpg")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.role = "admin"
            # Fetch players only once
            if "players_data" not in st.session_state:
                cur = db_connection.cursor()
                cur.execute("SELECT * FROM players_list")
                st.session_state.players_data = cur.fetchall()
        elif username == "user" and password == "user123":
            st.session_state.role = "user"
        st.rerun()


def admin_view():
    result = st.session_state.get("players_data", [])
    image_url = result[0][2]
    print(image_url)
    print("Result = ", result)
    print(type(result))
    set_background(
        "https://raw.githubusercontent.com/yadu10-guest/auction-app/refs/heads/master/images/player%20auction.webp")
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: white;'>Admin Dashboard</h1>
            <h2 style='color: white;'>Welcome Admin</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{image_url}" alt="Image" width="500" height="500" style="border-radius: 10px; border: 5px solid white;">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
        <div style='text-align: center;'>
        <h2 style='margin: 10px; color: white;'>₹{st.session_state.current_bid}</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 2.2, 2])
    with col2:
        if st.button("➖", help="Decrease bid"):
            if st.session_state.current_bid != 1000:
                if st.session_state.current_bid < 2000:
                    st.session_state.current_bid -= 100
                elif st.session_state.current_bid < 5000:
                    st.session_state.current_bid -= 200
                else:
                    st.session_state.current_bid -= 500
                st.rerun()

    with col3:
        if st.button("➕", help="Increase bid"):
            if st.session_state.current_bid < 2000:
                st.session_state.current_bid += 100
            elif st.session_state.current_bid < 5000:
                st.session_state.current_bid += 200
            else:
                st.session_state.current_bid += 500
            st.rerun()

    col4, col5, col6 = st.columns([1.1, 1.9, 2])

    # Styling for custom-colored buttons
    button_style = """
        <style>
        div.stButton > button:first-child {
            font-size: 18px;
            padding: 0.5em 2em;
            border-radius: 8px;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    with col5:
        st.markdown("<br>", unsafe_allow_html=True)  # Adds vertical spacing
        if st.button("SOLD"):
            st.markdown(
                """
                <audio autoplay>
                    <source src="https://raw.githubusercontent.com/yadu10-guest/auction-app/master/images/bj0iu39w9a-truck-horn-sfx-1.mp3" type="audio/mpeg">
                </audio>
                """,
                unsafe_allow_html=True
            )
            st.markdown('<script>document.querySelectorAll("button")[0].classList.add("sold-button")</script>',
                        unsafe_allow_html=True)

    with col6:
        st.markdown("<br>", unsafe_allow_html=True)  # Adds vertical spacing
        if st.button("UNSOLD"):
            st.markdown('<script>document.querySelectorAll("button")[1].classList.add("unsold-button")</script>',
                        unsafe_allow_html=True)
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
