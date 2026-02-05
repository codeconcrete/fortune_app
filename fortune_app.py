import streamlit as st
import google.generativeai as genai
import datetime

# 1. 화면 디자인 및 설정
st.set_page_config(page_title="2026년 AI 신년 운세", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    /* 전체 배경 흰색 (라이트 모드 강제) */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    /* 타이틀 및 헤더 검은색 */
    h1, h2, h3 {
        color: #000000 !important;
        font-family: 'Gowun Batang', serif;
        text-align: center;
    }
    p, label, div {
        color: #000000 !important;
    }
    /* 입력창 스타일: 흰 배경, 검은 글씨, 테두리 */
    .stTextInput input, .stSelectbox, .stDateInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }
    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #4CAF50; /* 무난한 녹색 또는 파란색 */
        color: white !important;
        border: none; 
        font-weight: bold; 
        padding: 10px; 
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("✨ 2026년(병오년) AI 운세")
st.markdown("<p style='text-align: center; color: #666;'>2026년 붉은 말의 해, 당신의 운세를 AI가 명쾌하게 풀이해 드립니다.</p>", unsafe_allow_html=True)

# 2. API 키 가져오기 (safety_app과 동일 로직)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = st.text_input("🔑 API 키 입력 (설정 파일이 없는 경우)", type="password")

st.divider()

# 3. 사용자 정보 입력
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("이름 (닉네임)", placeholder="홍길동")
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)

with col2:
    birth_date = st.date_input("생년월일", min_value=datetime.date(1940, 1, 1), value=datetime.date(1990, 1, 1))
    birth_time = st.time_input("태어난 시간 (모르면 12:00)", value=datetime.time(12, 0))

st.markdown("### ❓ 가장 궁금한 2026년 운세는?")
concern = st.selectbox(
    "가장 궁금한 2026년 운세는?",
    ["💰 금전운 (재물, 투자)", "💘 연애/결혼운", "🏢 직장/사업운", "🎓 학업/합격운", "💪 건강운", "🗓️ 오늘의 운세"],
    label_visibility="collapsed"
)

detail_concern = st.text_area("구체적인 고민이 있다면 적어주세요", placeholder="예: 2026년에 이직을 계획 중입니다. 시기가 언제가 좋을까요?")

solve_btn = st.button("🔮 2026년 운세 확인하기", use_container_width=True)

# 4. 운세 풀이 로직
if solve_btn:
    if not name:
        st.warning("이름을 입력해주세요.")
    elif not api_key:
        st.error("API 키가 필요합니다.")
    else:
        with st.spinner("2026년 병오년(丙午年)의 기운을 읽고 있습니다... 🐎"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-flash-latest')
                
                prompt = f"""
                당신은 명리학의 대가입니다. 지금은 2026년(병오년, 붉은 말의 해)입니다.
                아래 사주 정보를 바탕으로 2026년 기준의 신년 운세를 봐주세요.
                
                [내담자 정보]
                - 이름: {name}
                - 성별: {gender}
                - 생년월일: {birth_date.strftime('%Y년 %m월 %d일')}
                - 태어난 시간: {birth_time.strftime('%H시 %M분')}
                - 주요 관심사: {concern}
                - 구체적 고민: {detail_concern}
                
                [요청사항]
                1. 2026년 병오년(丙午年)의 총운을 설명해주세요.
                2. 질문한 '{concern}'에 대해 2026년의 구체적인 흐름과 월별 조언을 해주세요.
                3. 고민 내용({detail_concern})에 대해 명확한 답변을 주세요.
                4. 마지막으로 2026년 행운의 색상과 숫자를 추천해주세요.
                
                말투는 정중하고 희망차게 작성해주세요.
                답변 형식은 가독성 좋은 Markdown으로 작성하세요.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f"###   {name}님의 2026년 운세 풀이")
                st.markdown(response.text)
                st.balloons()
                
            except Exception as e:
                st.error(f"천기를 읽는 중 오류가 발생했습니다: {e}")