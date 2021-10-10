import streamlit as st
import requests
import time
from typing import Any
from PIL import Image
from streamlit.legacy_caching.caching import cache
from class_play_game import Playgame

st.title("Welcome to Hit&Blow Game!")
col1, col2, col3 = st.columns(3)
col2.write("よろしくね！")


st.title('Counter Example using Callbacks with args')
if 'count' not in st.session_state:
    st.session_state.count = 0

@st.cache(allow_output_mutation=True)
def cache_lst():
    lst = []
    return lst
lst = []
input = st.text_input('何か入力して下さい')
if input:
    lst.append(input)
st.table(lst)

url = "https://damp-earth-70561.herokuapp.com"


def get_room(session:requests.Session,room_id) -> Any:
    url_get_room = url + "/rooms/" + str(room_id)
    result = session.get(url_get_room)
    return result.json()


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
