import streamlit as st
import random
import time
import json

# --- Page Config ---
st.set_page_config(page_title="이모지 팡!", layout="centered")

# --- CSS: 이모지를 크게, 간격 좁게 ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        font-size: 50px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 10px !important;
        background-color: white !important;
        border: 2px solid #ddd !important;
    }
    .stApp { max-width: 500px; margin: auto; }
    </style>
""", unsafe_allow_html=True)

# --- Constants & State ---
EMOJI_POOL = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐯', '🦁', '🐷', '🐸', '🐵', '🐔']
if 'screen' not in st.session_state: st.session_state.screen = 'START'
if 'score' not in st.session_state: st.session_state.score = 0
if 'time_left' not in st.session_state: st.session_state.time_left = 15

# --- Sound Logic (HTML Audio) ---
def play_sound(type):
    audio_url = "https://actions.google.com/sounds/v1/ui/positive_tap.ogg" if type == 'correct' else "https://actions.google.com/sounds/v1/ui/error.ogg"
    st.markdown(f'<audio src="{audio_url}" autoplay="true"></audio>', unsafe_allow_html=True)

# --- Game Logic ---
def generate_board(difficulty):
    size = 16 if difficulty == 'EASY' else 25
    emojis = random.sample(EMOJI_POOL * 2, size - 1)
    pair = random.choice(emojis)
    board = emojis + [pair]
    random.shuffle(board)
    return [{'id': i, 'emoji': e} for i, e in enumerate(board)]

# --- UI Screens ---
def render_start():
    st.title("🌟 이모지 팡!")
    st.session_state.nickname = st.text_input("닉네임을 입력하세요", max_chars=8)
    st.session_state.difficulty = st.radio("난이도", ['EASY', 'NORMAL'])
    if st.button("게임 시작!"):
        if not st.session_state.nickname: st.warning("닉네임 필요!")
        else:
            st.session_state.cards = generate_board(st.session_state.difficulty)
            st.session_state.score = 0
            st.session_state.time_left = 15
            st.session_state.start_time = time.time()
            st.session_state.screen = 'GAME'
            st.rerun()

def render_game():
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = max(0, 15 - int(elapsed))
    
    if st.session_state.time_left <= 0:
        st.session_state.screen = 'RESULT'
        st.rerun()

    st.metric("남은 시간", f"{st.session_state.time_left}초")
    st.write(f"점수: {st.session_state.score}")
    
    cols = st.columns(4 if st.session_state.difficulty == 'EASY' else 5)
    
    # 카드 클릭 처리 (간소화)
    for i, card in enumerate(st.session_state.cards):
        if cols[i % (4 if st.session_state.difficulty == 'EASY' else 5)].button(card['emoji'], key=card['id']):
            # 여기에 매칭 로직 삽입 (성공 시 time_left += 3, play_sound('correct') 호출)
            st.session_state.score += 100
            st.session_state.start_time += 3 # 3초 추가
            play_sound('correct')
            st.rerun()

def render_result():
    st.title("게임 종료!")
    st.write(f"플레이어: {st.session_state.nickname}")
    st.write(f"최종 점수: {st.session_state.score}")
    
    # 랭킹 데이터 저장 (간이)
    rankings = json.loads(st.session_state.get('rankings', '[]'))
    rankings.append({'name': st.session_state.nickname, 'score': st.session_state.score})
    rankings = sorted(rankings, key=lambda x: x['score'], reverse=True)[:5]
    st.session_state.rankings = json.dumps(rankings)
    
    st.subheader("🏆 실시간 랭킹")
    for r in rankings:
        st.write(f"{r['name']} : {r['score']}점")
        
    if st.button("다시 하기"): st.session_state.screen = 'START'; st.rerun()

# --- Main ---
if st.session_state.screen == 'START': render_start()
elif st.session_state.screen == 'GAME': render_game()
else: render_result()