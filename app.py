import streamlit as st
from google import genai
from PIL import Image
import io

# ---------------------------------------------------------
# 1. API 클라이언트 설정
# ---------------------------------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("⚠️ API 키 설정 오류가 발생했습니다.")
    st.stop()

# ---------------------------------------------------------
# 2. 페이지 레이아웃
# ---------------------------------------------------------
st.set_page_config(page_title="사내 이미지 생성기", page_icon="🍌")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #FFD700;
        color: #1E1E1E;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍌 우리 회사 전용 이미지 생성기")

# ---------------------------------------------------------
# 3. 사이드바 스타일 선택
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎨 스타일 가이드")
    style_choice = st.radio(
        "원하는 비주얼 스타일을 선택하세요:",
        (
            "3D Pixar Style",
            "Corporate Minimal",
            "Isometric Infra",
            "Photo Realistic"
        )
    )

# ---------------------------------------------------------
# 4. 사용자 입력창
# ---------------------------------------------------------
prompt = st.text_area("무엇을 그릴까요?", placeholder="예: 미래형 교량 설계도", height=120)

# ---------------------------------------------------------
# 5. 생성 로직 (이 부분의 들여쓰기가 중요합니다!)
# ---------------------------------------------------------
if st.button("이미지 생성 시작하기"):
    if not prompt:
        st.warning("그릴 내용을 입력해 주세요!")
    else:
        with st.spinner("이미지를 생성하는 중..."):
            try:
                # 여기서부터 'try' 블록 시작 (안쪽으로 한 칸 들여쓰기)
                final_prompt = f"Style: {style_choice}. Subject: {prompt}. Professional quality."
                
                response = client.models.generate_content(
                    model="gemini-3.1-flash-image-preview",
                    contents=[final_prompt]
                )
                
                image_found = False
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        image_data = part.inline_data.data
                        image = Image.open(io.BytesIO(image_data))
                        
                        st.divider() # 이 줄의 위치가 try 안쪽에 있어야 합니다.
                        st.image(image, caption="생성 결과", use_container_width=True)
                        
                        buf = io.BytesIO()
                        image.save(buf, format="PNG")
                        st.download_button(
                            label="💾 이미지 저장하기",
                            data=buf.getvalue(),
                            file_name="result.png",
                            mime="image/png"
                        )
                        image_found = True
                        break
                
                if not image_found:
                    st.warning("이미지를 생성하지 못했습니다.")

            except Exception as e:
                # 'try'와 'except'는 반드시 세로 줄이 딱 맞아야 합니다!
                if "429" in str(e):
                    st.error("🚀 API 호출 한도가 초과되었습니다. 잠시 후 다시 시도해 주세요.")
                else:
                    st.error(f"⚠️ 오류가 발생했습니다: {e}")
