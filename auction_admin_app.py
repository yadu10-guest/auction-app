import time

import pandas as pd
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

cur = db_connection.cursor()

if "current_bid" not in st.session_state:
    st.session_state.current_bid = 1000  # starting bid

if "player_sold" not in st.session_state:
    st.session_state.player_sold = False


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
                cur.execute("SELECT * FROM players_list")
                st.session_state.players_data = cur.fetchall()
        elif username == "user" and password == "user123":
            st.session_state.role = "user"
        st.rerun()


def enter_player_id():
    st.session_state.image_placeholder = st.empty()
    st.session_state.image_placeholder.image("https://github.com/yadu10-guest/auction-app/blob/master/images/a557864d-fdb9-402c-ac57-d9796066633f.jpeg?raw=true")
    st.session_state.player_id = st.empty()
    player_id = st.sidebar.text_input("Enter player ID")
    print(type(player_id))
    st.session_state.player_id = player_id


def admin_view(player_id):
    print(type(player_id))
    result = st.session_state.get("players_data", [])
    if 'current_player' not in st.session_state:
        st.session_state.current_player = result[player_id - 1][1]
    image_url = result[player_id - 1][2]
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
            time.sleep(4)
            st.session_state.player_sold = True
            st.rerun()

    with col6:
        st.markdown("<br>", unsafe_allow_html=True)  # Adds vertical spacing
        if st.button("UNSOLD"):
            st.markdown('<script>document.querySelectorAll("button")[1].classList.add("unsold-button")</script>',
                        unsafe_allow_html=True)
            st.rerun()

    if st.session_state.get("player_sold", False):
        team_names = [
            "Hamras XI",
            "ElevenStar Kgm",
            "Smashes Cgm",
            "Black Knights",
            "SAS Koozhakode",
            "90s XI Pilassery",
            "NFC Kakkanad",
            "Al Arooz Kgm"
        ]

        st.markdown("<h3 style='color: white;'>Select Team</h3>", unsafe_allow_html=True)

        # Show buttons in two rows, each with 3 columns
        for i in range(0, len(team_names), int(len(team_names) / 2)):
            cols = st.columns(int(len(team_names) / 2))
            for j in range(int(len(team_names) / 2)):
                if i + j < len(team_names):
                    team = team_names[i + j]
                    with cols[j]:
                        if st.button(team, key=f"select_{team}"):
                            cur.execute(f'SELECT * FROM "{team}"')

                            players_in_team = cur.fetchall()
                            print(players_in_team)

                            if players_in_team:
                                st.session_state.balance_point = players_in_team[-1][3]
                            else:
                                st.session_state.balance_point = 30000

                            # Insert into db

                            cur.execute(
                                f'''
                                INSERT INTO "{team}" (player_name, auction_point, balance_point, player_id)
                                VALUES (%s, %s, %s, %s)
                                ''',
                                (
                                    st.session_state.current_player,
                                    st.session_state.current_bid,
                                    st.session_state.balance_point - st.session_state.current_bid,
                                    st.session_state.player_id
                                )
                            )

                            db_connection.commit()
                            st.success(f"{team} marked as SOLD!")
                            st.session_state.player_sold = False
                            st.session_state.current_bid = 1000
                            st.rerun()


def user_view():
    set_background(
        "https://raw.githubusercontent.com/yadu10-guest/auction-app/refs/heads/master/images/player%20auction.webp")
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: white;'>User Dashboard</h1>
            <h2 style='color: white;'>Welcome User</h2>
        </div>
    """, unsafe_allow_html=True)

    team_names = [
        "Hamras XI",
        "ElevenStar Kgm",
        "Smashes Cgm",
        "Black Knights",
        "SAS Koozhakode",
        "90s XI Pilassery",
        "NFC Kakkanad",
        "Al Arooz Kgm"
    ]

    for team_name in team_names:
        cur.execute(f'SELECT * FROM "{team_name}"')
        players = cur.fetchall()

        st.markdown(f"<h3 style='color: white; text-align: center;'>{team_name}</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)  # Adds vertical spacing

        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(players, columns=columns)

        # Filter and rename columns
        filtered_df = df[["player_name", "player_id", "auction_point", "balance_point"]].rename(columns={
            "player_name": "PLAYER NAME",
            "player_id": "PLAYER CARD ID",
            "auction_point": "PLAYER AUCTION POINT",
            "balance_point": "TEAM BALANCE POINT"
        })

        st.dataframe(filtered_df, use_container_width=True)

        print(players)


# Main routing logic
if "role" not in st.session_state:
    login()
elif st.session_state.role == "admin":
    enter_player_id()
    if st.session_state.player_id:
        st.session_state.image_placeholder.empty()
        admin_view(int(st.session_state.player_id))
else:
    user_view()
