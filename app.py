import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="AI 외국어 일기장", page_icon="🤖")

# 사이드바: 설정 및 API 키 입력
with st.sidebar:
    st.title("⚙️ 설정")
    # API 키를 직접 코드에 넣지 않고 화면에서 입력받아 보안을 지킵니다.
    api_key_input = st.text_input("OpenAI API Key를 입력하세요", type="password")
    lang = st.radio("공부할 언어 선택", ("영어 (English)", "중국어 (中文)"))
    st.info("API 키는 세션이 종료되면 저장되지 않으니 안심하세요.")

st.title("📔 나만의 AI 외국어 일기장")
st.write(f"현재 선택된 언어: **{lang}**")

# 일기 입력창
user_content = st.text_area("오늘의 일기를 작성해 보세요. (한글을 섞어 쓰셔도 AI가 교정해줍니다!)", height=250)

if st.button("AI 선생님께 교정받기 ✨"):
    if not api_key_input:
        st.error("왼쪽 사이드바에 API 키를 먼저 입력해 주세요!")
    elif not user_content.strip():
        st.warning("내용을 입력해 주세요.")
    else:
        try:
            client = OpenAI(api_key=api_key_input)
            
            with st.spinner('AI 선생님이 일기를 읽고 분석 중입니다...'):
                # AI에게 전달할 상세 지침(Prompt)
                system_msg = f"당신은 {lang} 교육 전문가입니다. 사용자가 쓴 일기를 보고 교정해주세요."
                user_msg = f"""
                다음 일기 내용을 확인하고 아래 형식으로 답해주세요:
                1. [교정된 문장]: 한국어는 {lang}로 바꾸고, 문법적으로 더 자연스러운 문장으로 전체를 다시 써주세요.
                2. [문법 포인트]: 오늘 일기에서 틀린 부분이나 꼭 알아야 할 {lang} 문법을 1-2개만 쉽게 설명해주세요.
                
                내용: {user_content}
                """

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", # 또는 gpt-4o
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ]
                )

                # 결과 출력
                st.divider()
                st.subheader("✅ AI 선생님의 피드백")
                st.write(response.choices[0].message.content)
                
                # 저장 기능 가이드
                st.download_button(
                    label="일기장 파일로 내보내기",
                    data=f"날짜: {st.write}\n언어: {lang}\n내용: {user_content}\n\n교정내용:\n{response.choices[0].message.content}",
                    file_name=f"diary_{lang}.txt"
                )

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

st.divider()
st.caption("제공: 나만의 AI 일기장 프로젝트")
