import streamlit as st
from google import genai
from PIL import Image
import io

# 1. API 클라이언트 설정
# st.secrets["GEMINI_API_KEY"]를 사용하여 문자열 값을 정확히 가져옵니다.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Secrets 설정에서 'GEMINI_API_KEY'를 찾을 수 없습니다. Streamlit Cloud 설정을 확인해 주세요.")
    st.stop()

# 2. 대시보드 화면 구성
st.set_page_config(page_title="사내 이미지 생성기", page_icon="🍌", layout="centered")

# 디자인 업무 효율을 위한 커스텀 스타일 적용 (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍌 우리 회사 전용 나노바나나 생성기")
st.info("편집 디자이너를 위한 고퀄리티 이미지 생성 도구입니다.")

# 3. 사이드바 - 스타일 가이드 및 옵션
with st.sidebar:
    st.header("🎨 디자인 옵션")
    style = st.radio(
        "적용할 스타일 가이드를 선택하세요:",
        (
            "3D Pixar Animation (Soft lighting, high detail)", 
            "Modern Corporate Web (Glassmorphism, Clean, Minimal)",
            "Engineering Blueprint (Technical drawing, Blueprint style)",
            "Isometric 3D Infrastructure (C4D style, Clay render)"
        )
    )
    
    st.divider()
    st.caption("Model: Gemini 3.1 Flash Image (Nano Banana 2)")

# 4. 메인 입력창
prompt = st.text_area("무엇을 그릴까요?", placeholder="예: 미래형 친환경 교량 설계도, 커피 마시는 강아지 등", height=150)

# 5. 실행 로직
if st.button("이미지 생성하기"):
    if not prompt:
        st.warning("그릴 내용을 입력해 주세요!")
    else:
        with st.spinner("나노바나나 엔진이 고해상도 이미지를 렌더링 중입니다..."):
            try:
                # 프롬프트 엔지니어링: 선택한 스타일에 따라 구체적인 지시어 추가
                final_prompt = f"Style: {style}. Subject: {prompt}. Ensure high resolution, professional quality, and clear composition."
                
                # 모델 호출 (Gemini 3.1 Flash Image)
                response = client.models.generate_content(
                    model="gemini-3.1-flash-image-preview",
                    contents=[final_prompt]
                )
                
                # 결과물 출력
                image_found = False
                # candidates[0]의 content.parts에서 inline_data(이미지)를 찾음
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        image_data = part.inline_data.data
                        image = Image.open(io.BytesIO(image_data))
                        
                        st.divider()
                        st.image(image, caption=f"생성된 결과: {style}", use_container_width=True)
                        
                        # 다운로드 버튼 추가
                        buf = io.BytesIO()
                        image.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        st.download_button(
                            label="이미지 다운로드 (PNG)",
                            data=byte_im,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
                        st.success("성공적으로 이미지를 생성했습니다!")
                        image_found = True
                
                if not image_found:
                    st.error("이미지 데이터를 받지 못했습니다. 다시 시도해 주세요.")
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
                st.info("팁: API 키가 유효한지, 혹은 할당량이 초과되지 않았는지 확인해 보세요.")
