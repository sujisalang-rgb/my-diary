import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="AI 외국어 일기장", page_icon="📝")

with st.sidebar:
    st.title("⚙️ 설정")
    api_key = st.text_input("Google API Key를 입력하세요", type="password")
    lang = st.radio("학습 언어", ("영어 (English)", "중국어 (中文)"))

st.title("📔 나만의 AI 외국어 일기장")

user_content = st.text_area(
    "오늘의 일기를 작성해 보세요.",
    placeholder="예: 오늘 친구랑 밥을 먹었는데 delicious 했어.",
    height=250
)

if st.button("AI 선생님께 교정받기 ✨"):
    if not api_key:
        st.error("API 키를 입력해 주세요!")
    elif not user_content.strip():
        st.warning("내용을 입력해 주세요.")
    else:
        try:
            # API 설정
            genai.configure(api_key=api_key)
            
            # [핵심] 사용 가능한 모델 중 'generateContent'를 지원하는 첫 번째 모델 자동 선택
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not available_models:
                st.error("사용 가능한 Gemini 모델을 찾을 수 없습니다. API 키 설정을 확인해주세요.")
            else:
                # 가장 안정적인 flash 모델 우선 선택, 없으면 첫 번째 모델 사용
                selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
                model = genai.GenerativeModel(selected_model)
                
                with st.spinner(f'AI 선생님({selected_model})이 분석 중입니다...'):
                    prompt = f"""
                    당신은 {lang}와 한국어 교육 전문가입니다. 아래 일기를 교정해주세요.
                    1. [교정된 문장]: 한국어 부분은 {lang}로 번역하고, 전체를 자연스러운 표현으로 수정.
                    2. [오늘의 포인트]: 중요한 문법/단어 규칙 설명.
                    내용: {user_content}
                    """
                    response = model.generate_content(prompt)
                    
                    st.divider()
                    st.subheader("✅ AI 선생님의 피드백")
                    st.write(response.text)
                    st.caption(f"사용한 모델: {selected_model}")
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.info("💡 만약 이 오류가 계속된다면, Google AI Studio에서 새 API 키를 생성하는 것을 권장합니다.")
