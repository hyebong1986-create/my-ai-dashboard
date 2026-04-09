import streamlit as st
from google import genai
from PIL import Image
import io

# 1. 금고 안에서 'GEMINI_API_KEY'라는 이름의 열쇠를 정확히 꺼내옵니다.
# (이 부분이 수정되었습니다!)
api_key = st.secrets
client = genai.Client(api_key=api_key)

# 2. 대시보드 화면 꾸미기
st.set_page_config(page_title="사내 이미지 생성기", page_icon="🍌")
st.title("🍌 우리 회사 전용 나노바나나 생성기")
st.write("원하는 스타일을 선택하고 글자를 입력하세요!")

# 3. 스타일 가이드 선택 버튼 만들기
style = st.radio("적용할 스타일 가이드를 선택하세요:", 
    ["[스타일 A] 3D 픽사 애니메이션 느낌", 
     " 세련된 기업용 웹사이트 배너 느낌"]
)

# 4. 그릴 내용 입력받기
prompt = st.text_area("무엇을 그릴까요?", "커피를 마시는 귀여운 강아지")

# 5. 생성 버튼을 눌렀을 때의 동작
if st.button("이미지 생성하기"):
    if not prompt:
        st.warning("그릴 내용을 입력해 주세요!")
    else:
        with st.spinner("나노바나나 엔진이 그림을 그리는 중입니다..."):
            try:
                # 선택한 스타일과 입력한 글자를 합쳐서 엔진에 전달
                final_prompt = f"다음 스타일 규칙을 무조건 엄격하게 지켜서 그려주세요: {style}. 그릴 내용: {prompt}"
                
                # 나노바나나 2 모델 호출
                response = client.models.generate_content(
                    model="gemini-3.1-flash-image-preview",
                    contents=[final_prompt]
                )
                
                # 완성된 그림을 화면에 보여주기
                for part in response.candidates.content.parts:
                    if part.inline_data:
                        image = Image.open(io.BytesIO(part.inline_data.data))
                        st.image(image, caption="생성된 이미지", use_container_width=True)
                        st.success("이미지 생성 완료!")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
