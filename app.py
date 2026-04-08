import streamlit as st
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="나만의 외국어 일기장", page_icon="📔")

st.title("📔 AI 외국어 일기장")
st.info("오늘 하루를 영어 혹은 중국어로 기록해보세요!")

# 사이드바 설정
with st.sidebar:
    lang = st.radio("언어 선택", ("English", "Chinese"))
    st.write("---")
    st.caption("일기를 쓰고 '저장'을 누르면 아래 기록에 쌓입니다.")

# 일기 입력창
content = st.text_area(f"{lang}로 일기를 작성하세요.", height=200)

if st.button("일기 저장하기"):
    if content.strip():
        # 실제 배포 환경에서는 데이터베이스가 필요하지만, 
        # 우선은 화면에 즉시 보여주는 방식으로 구현합니다.
        st.success(f"✅ {lang} 일기가 저장되었습니다!")
        st.session_state['last_entry'] = content
        
        # 수정용 복사 텍스트 제공
        st.subheader("📝 교정 요청용 텍스트")
        st.code(content)
        st.write("위 코드를 복사해서 Gemini에게 보여주세요!")
    else:
        st.error("내용을 입력해주세요.")

# 저장된 기록 보기 (간이 구현)
if 'last_entry' in st.session_state:
    with st.expander("최근 작성한 내용 확인"):
        st.write(st.session_state['last_entry'])
