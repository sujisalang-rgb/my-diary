import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="AI 외국어 일기장", page_icon="🤖")

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ 설정")
    api_key_input = st.text_input("Google API Key를 입력하세요", type="password")
    lang = st.radio("공부할 언어 선택", ("영어 (English)", "중국어 (中文)"))
    st.info("API 키는 세션 종료 후 저장되지 않습니다.")

st.title("📔 나만의 AI 외국어 일기장")

user_content = st.text_area(
    "오늘의 일기를 작성해 보세요.",
    placeholder="예: 오늘 친구랑 밥을 먹었는데 delicious 했어.",
    height=250
)

if st.button("AI 선생님께 교정받기 ✨"):
    if not api_key_input:
        st.error("Google API 키를 입력해 주세요!")
    elif not user_content.strip():
        st.warning("내용을 입력해 주세요.")
    else:
        try:
            # Gemini 설정
            genai.configure(api_key=api_key_input)
            
            # 404 에러 방지를 위해 가장 범용적인 모델명 사용
            # 만약 gemini-1.5-flash가 안되면 gemini-2.0-flash로 자동 시도하도록 설정 가능
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('AI 선생님이 일기를 분석 중입니다...'):
                prompt = f"""
                당신은 {lang}와 한국어 교육 전문가입니다. 
                사용자가 쓴 다음 일기를 교정해주세요:
                
                1. [교정된 문장]: 한국어 부분은 {lang}로 번역하고, 전체를 자연스러운 원어민 표현으로 수정.
                2. [오늘의 포인트]: 틀린 부분이나 중요한 문법/단어 규칙을 1~2개 설명.
                
                내용: {user_content}
                """
                
                response = model.generate_content(prompt)
                
                st.divider()
                st.subheader("✅ AI 선생님의 피드백")
                st.write(response.text)
                
        except Exception as e:
            # 404 에러가 날 경우 다른 모델명으로 재시도하라는 안내
            st.error(f"오류가 발생했습니다: {e}")
            st.info("💡 만약 404 에러가 계속된다면, 코드의 'gemini-1.5-flash' 부분을 'gemini-2.0-flash'로 바꿔보세요.")

st.divider()
st.caption("나만의 외국어 일기장 - Gemini AI")
