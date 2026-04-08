import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="AI 외국어 일기장", page_icon="🤖")

# 사이드바 설정
with st.sidebar:
    st.title("⚙️ 설정")
    # 구글 API 키 입력 (AIzaSy...)
    api_key_input = st.text_input("Google API Key를 입력하세요", type="password")
    lang = st.radio("공부할 언어 선택", ("영어 (English)", "중국어 (中文)"))
    st.info("API 키는 보안을 위해 이 세션에서만 임시로 사용됩니다.")

st.title("📔 나만의 AI 외국어 일기장 (Gemini)")
st.write(f"현재 설정된 언어: **{lang}**")

# 일기 작성 구역
user_content = st.text_area(
    "오늘의 일기를 작성해 보세요. 한국어를 섞어 써도 자연스럽게 바꿔줍니다!",
    placeholder="예: 오늘 친구랑 밥을 먹었는데 delicious 했어. 내일 또 가고 싶어.",
    height=250
)

if st.button("AI 선생님께 교정받기 ✨"):
    if not api_key_input:
        st.error("Google API 키를 먼저 입력해 주세요! (AIzaSy...로 시작하는 키)")
    elif not user_content.strip():
        st.warning("내용을 입력해 주세요.")
    else:
        try:
            # Gemini 설정
            genai.configure(api_key=api_key_input)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('AI 선생님이 일기를 분석하고 있습니다...'):
                # AI에게 줄 미션 (프롬프트)
                prompt = f"""
                당신은 {lang}와 한국어에 능통한 언어 교육 전문가입니다. 
                다음 일기를 교정해주세요:
                
                1. [교정된 전체 문장]: 한국어 부분은 {lang}로 번역하고, 전체적으로 자연스러운 원어민 표현으로 다시 써주세요.
                2. [단어 및 문법 설명]: 교정 과정에서 바뀐 중요한 단어나 {lang} 문법 규칙을 초보자가 알기 쉽게 1~2개만 설명해주세요.
                
                일기 내용: 
                {user_content}
                """
                
                response = model.generate_content(prompt)
                
                # 결과 출력
                st.divider()
                st.subheader("✅ AI 선생님의 피드백")
                st.write(response.text)
                
                # 다운로드 기능
                st.download_button(
                    label="일기 내용 저장하기 (txt)",
                    data=f"--- {lang} 일기 ---\n\n[원본]\n{user_content}\n\n[AI 교정]\n{response.text}",
                    file_name=f"diary_ai.txt"
                )
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.info("API 키가 유효한지, 혹은 Gemini API 사용 설정이 되어 있는지 확인해 주세요.")

st.divider()
st.caption("나만의 외국어 일기장 프로젝트 - Gemini AI 탑재")
