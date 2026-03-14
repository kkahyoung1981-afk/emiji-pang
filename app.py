import streamlit as st
import random
import time

# 이모지 풀
EMOJI_POOL = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐯', '🦁', '🐷', '🐸', '🐵', '🐔']

st.title("🍎 이모지 짝 맞추기: Emiji Pang!")

# 게임 상태 초기화
if 'board' not in st.session_state:
    st.session_state.board = None
    st.session_state.score = 0
    st.session_state.selected = []

def generate_board():
    # 4x4 게임을 위한 8쌍의 이모지 생성
    sample = random.sample(EMOJI_POOL, 8)
    board = sample + sample
    random.shuffle(board)
    st.session_state.board = board
    st.session_state.score = 0
    st.session_state.selected = []

if st.button("새 게임 시작"):
    generate_board()

# 보드 출력
if st.session_state.board:
    st.write(f"### 현재 점수: {st.session_state.score}")
    
    # 4x4 그리드 구성
    cols = st.columns(4)
    for i, emoji in enumerate(st.session_state.board):
        if cols[i % 4].button(f"{emoji}", key=f"btn_{i}"):
            st.session_state.selected.append(i)
            
            if len(st.session_state.selected) == 2:
                idx1, idx2 = st.session_state.selected
                if st.session_state.board[idx1] == st.session_state.board[idx2]:
                    st.success("짝을 맞췄어요! 팡!")
                    st.session_state.score += 100
                else:
                    st.error("틀렸어요!")
                st.session_state.selected = []
                # 잠시 대기 후 결과 확인을 위해 페이지 새로고침 대신 알림 활용
                time.sleep(0.5)
                st.rerun()

st.info("카드를 클릭하여 똑같은 이모지 2개를 찾아보세요!")