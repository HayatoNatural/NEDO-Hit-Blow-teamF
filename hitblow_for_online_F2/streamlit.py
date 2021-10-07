# import streamlit as st
# import requests
# import time
# from typing import Any
# from PIL import Image
# from class_play_game import Playgame

# st.write('Count = ' + st.session_state.count)
# st.title("Welcome to Hit&Blow Game!")
# col1, col2, col3 = st.columns(3)
# col2.write("よろしくね！")
# col2.image("f007.png",use_column_width=True)
# col3.image("花火大会_gifmagazine.gif",use_column_width=True)

# url = "https://damp-earth-70561.herokuapp.com"

# def get_room(session:requests.Session,room_id) -> Any:
#     url_get_room = url + "/rooms/" + str(room_id)
#     result = session.get(url_get_room)
#     return result.json()


# def main():
#     session = requests.Session()
#     st.title('Counter Example')
#     if 'count' not in st.session_state:
#         st.session_state.count = 0
#     increment = st.button('Increment')
#     if increment:
#         st.session_state.count += 1
#     st.write('Count = ', st.session_state.count)


# if __name__ =="__main__":
#     main()
