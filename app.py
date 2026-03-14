import streamlit as st
import random
import time
import json

# --- Constants & Settings ---
EMOJI_POOL = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐯', '🦁', '🐷', '🐸', '🐵', '🐔', '🐧']
RANKING_KEY = 'emoji_rank_v4'

# 세션 상태 초기화
if "screen" not in st.session_state: st.session_state.screen = 'START'
if "score" not in st.session_state: st.session_state.score = 0
if "cards" not in st.session_state: st.session_state.cards = []

def get_new_board():
    unique_emojis = random.sample(EMOJI_POOL, 8)
    pair = random.choice(unique_emojis)
    board = unique_emojis + [pair]
    random.shuffle(board)
    return [{"id": i, "emoji": e} for i, e in enumerate(board)]

# --- 화면별 함수 ---

def show_start():
    st.title("🍎 이모지 팡!")
    st.write("똑같은 이모지 2개를 찾아보세요!")
    name = st.text_input("닉네임을 적어주세요")
    if st.button("게임 시작!"):
        if name:
            st.session_state.nickname = name
            st.session_state.cards = get_new_board()
            st.session_state.score = 0
            st.session_state.screen = 'GAME'
            st.rerun()
        else:
            st.warning("닉네임을 입력하세요!")

def show_game():
    st.title(f"점수: {st.session_state.score}")
    
    # 3x3 그리드 형태
    cols = st.columns(3)
    for i, card in enumerate(st.session_state.cards):
        if cols[i % 3].button(card["emoji"], key=card["id"]):
            st.session_state.score += 10 # 간단한 클릭 점수 예시
            st.rerun()
            
    if st.button("게임 종료"):
        st.session_state.screen = 'RESULT'
        st.rerun()

def show_result():
    st.title("게임 종료!")
    st.write(f"최종 점수: {st.session_state.score}")
    if st.button("처음으로"):
        st.session_state.screen = 'START'
        st.rerun()

# --- 메인 루프 ---
if st.session_state.screen == 'START':
    show_start()
elif st.session_state.screen == 'GAME':
    show_game()
elif st.session_state.screen == 'RESULT':
    show_result()