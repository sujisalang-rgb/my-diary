import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="나만의 AI 일기장", page_icon="📝")

# 2. 사이드바 - 설정
with st.sidebar:
    st.title("⚙️ 설정")
    api_key = st.text_input("Google API Key를 입력하세요", type="password")
    lang = st.radio("학습 언어", ("영어 (English)", "중국어 (中文)"))
    st.info("API 키는 세션 종료 후 저장되지 않습니다.")

st.title("📔 나만의 AI 외국어 일기장")
st.write(f"현재 선택된 언어: **{lang}**")

# 3. 입력창
user_content = st.text_area(
    "오늘의 일기를 작성해 보세요. 한국어를 섞어 써도 괜찮아요!",
    placeholder="예: 오늘 아침에 exercise를 했어. 기분이 very good했다.",
    height=250
)

# 4. 분석 버튼
if st.button("AI 선생님께 교정받기 ✨"):
    if not api_key:
        st.error("API 키를 입력해 주세요!")
    elif not user_content.strip():
        st.warning("내용을 입력해 주세요.")
    else:
        try:
            # API 설정
            genai.configure(api_key=api_key)
            
            # 모델 지정 (가장 호환성이 높은 최신 명칭)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            with st.spinner('AI 선생님이 일기를 분석 중입니다...'):
                prompt = f"""
                당신은 {lang}와 한국어 교육 전문가입니다. 
                사용자가 쓴 다음 일기를 교정해주세요:
                
                1. [교정된 문장]: 한국어 부분은 {lang}로 번역하고, 전체를 자연스러운 원어민 표현으로 수정.
                2. [오늘의 포인트]: 틀린 부분이나 중요한 문법/단어 규칙을 1~2개 설명.
                
                내용: 
                {user_content}
                """
                
                # 결과 생성
                response = model.generate_content(prompt)
                
                # 결과 출력
                st.divider()
                st.subheader("✅ AI 선생님의 피드백")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.info("💡 모델명을 찾을 수 없다면 구글 AI 스튜디오에서 'Gemini API'가 활성화되었는지 확인해 보세요.")

st.divider()
st.caption("나만의 외국어 일기장 - Gemini AI")
