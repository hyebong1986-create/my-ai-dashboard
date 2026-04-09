import streamlit as st
from google import genai
from PIL import Image
import io

# ---------------------------------------------------------
# 1. API 클라이언트 설정 (에러 방지 처리)
# ---------------------------------------------------------
try:
    # Streamlit Cloud의 Settings > Secrets에 등록한 이름을 사용합니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("⚠️ API 키 설정 오류가 발생했습니다.")
    st.info("Streamlit Cloud 설정(Secrets)에 'GEMINI_API_KEY'가 정확히 입력되었는지 확인해 주세요.")
    st.stop()

# ---------------------------------------------------------
# 2. 페이지 레이아웃 및 디자인 (CSS)
# ---------------------------------------------------------
st.set_page_config(page_title="사내 이미지 생성기", page_icon="🍌", layout="centered")

# 디자이너의 감각에 맞는 깔끔한 스타일 적용
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #FFD700;
        color: #1E1E1E;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFC800;
        border: 1px solid #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍌 우리 회사 전용 이미지 생성기")
st.write("나노바나나 2(Gemini 3.1 Flash) 엔진을 활용한 고성능 생성기입니다.")

# ---------------------------------------------------------
# 3. 사이드바 설정 (스타일 가이드)
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎨 스타일 가이드")
    style_choice = st.radio(
        "원하는 비주얼 스타일을 선택하세요:",
        (
            "3D Pixar Style (애니메이션, 입체감)",
            "Corporate Minimal (깔끔한 기업 홍보용)",
            "Isometric Infra (교량/터널 등 인프라 3D)",
            "Photo Realistic (실사 사진 느낌)"
        )
    )
    st.divider()
    st.caption("제작: 사내 디자인팀 전용 도구")

# ---------------------------------------------------------
# 4. 사용자 입력창
# ---------------------------------------------------------
prompt = st.text_area(
    "어떤 이미지를 만들까요?", 
    placeholder="예: 안전모를 쓰고 웃고 있는 귀여운 강아지 캐릭터",
    height=120
)

# ---------------------------------------------------------
# 5. 생성 로직 (에러 핸들링 포함)
# ---------------------------------------------------------
if st.button("이미지 생성 시작하기"):
    if not prompt:
        st.warning("그릴 내용을 입력해 주세요!")
    else:
        with st.spinner("엔진이 가동 중입니다. 잠시만 기다려 주세요..."):
            try:
                # 스타일과 내용을 합친 최종 명령문
                final_prompt = f"Style: {style_choice}. Subject: {prompt}. High resolution, 4k, professional composition."
                
                # 모델 호출
                response = client.models.generate_content(
                    model="gemini-3.1-flash-image-preview",
                    contents=[final_prompt]
                )
                
                # 결과물 확인 및 출력
                image_found = False
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        image_data = part.inline_data.data
                        image = Image.open(io.BytesIO(image_data))
                        
                        st.divider()
