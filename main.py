import streamlit as st
from openai import OpenAI

st.set_page_config(page_title='도움', page_icon='🤐', layout="centered")

code = """
<style>
@media (max-width: 50.5rem) {
  .st-emotion-cache-gh2jqd {
    max-width: calc(-0rem + 100vw);
  }
}
header {visibility: hidden;}
</style>"""
st.html(code)

if 'logged' not in st.session_state:
    st.session_state.logged = False
if st.session_state.logged == False:
    if st.text_input(type='password', label='비밀번호를 입력하세요.') == 'TheFiveGuys': st.session_state.logged = True; st.rerun()

if st.session_state.logged == True:
    client = OpenAI(
    api_key='sk-ERbEZ6g35cYPM7DcMylctYXpg92zF60UaaVGMZWfPU1x7dpX',
    base_url='https://api.chatanywhere.cn'
    )

    st.header('토론 의견 생성 AI', divider='rainbow')
    '##'

    with st.form('아래 양식을 모두 작성하여주세요.'):
        global topic, opinion, rebuttal
        topic = st.text_input('토론 주제', placeholder='ex. 크리스천이 술을 마셔도 되나요?')
        opinion = st.text_input('당신의 찬반 내용', placeholder='ex. 술을 마시면 안된다고 생각합니다.')
        rebuttal = st.checkbox('반박 의견 생성')

        if st.form_submit_button('의견 생성'):
            if topic != '' and opinion != '':
                message_placeholder = st.empty()
                full_response = ""
                placeholder = st.empty()
                
                if rebuttal is False:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You will be provided with debate topic and its user's opinion. Create at least 5 opinions for user. Remember that you are a Christian."},
                            {"role": "user", "content": "topic: 크리스천이 술을 마셔도 되나요? \n opinion: 술을 마시면 안된다고 생각합니다."},
                            {"role": "assistant", "content": "- 술에 취한다면, 침참하고 냉정한 마음을 가질 수 없다. \n - 알코올은 파괴의 사명을 가지고 있다. \n - 알코올은 진정제다. \n - 알코올은 내 판단력을 왜곡시킨다. \n - 알코올은 나를 더 낫게 하는 것이 아니라 더 나쁘게 한다. \n - 내가 자제해서 적당하게, 알맞게 하는 것을, 나의 자녀들은 넘어서서 극단적으로 한다. \n - 알코올은 나를 주께로 더 가까이 데려가지 못한다. 내가 술을 마실 때 더 멀어진다. \n - 나는 모든 모양의 악을 피하기를 원한다. \n - 알코올은 자기 절제의 열매를 실천하는 것이 더 어렵게 만든다. \n - 알코올은 중독적이다."},
                            {"role": "user", "content": f"topic: {topic} \n opinion: {opinion}"}

                        ],
                        temperature=0.7,
                        #max_tokens=64,
                        top_p=1,
                        stream= True
                    )
                  
                if rebuttal is True:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You will be provided with debate topic, its user's opinion, and rebuttal opinions(which is opponent's opinion) Create at least 5 opinions for user first, and rebuttal opinions. Remember that you are a Christian."},
                            {"role": "user", "content": "topic: 크리스천이 술을 마셔도 되나요? \n opinion: 술을 마시면 안된다고 생각합니다."},
                            {"role": "assistant", "content": "- 술에 취한다면, 침참하고 냉정한 마음을 가질 수 없다. \n - 알코올은 파괴의 사명을 가지고 있다. \n - 알코올은 진정제다. \n - 알코올은 내 판단력을 왜곡시킨다. \n - 알코올은 나를 더 낫게 하는 것이 아니라 더 나쁘게 한다. \n --- \n - 술은 사람의 스트레스를 없애줄 수 있다. \n - 술은 우리를 같이 술을 마시는 사람과 친하게 만들 수 있다. \n - 술은 절제만 하면 되지 취하기 까지 마시면 안된다. \n 술은 우리의 나쁜 기억들을 없애줄 수 있다. \n - 술은 행동과 사고에 능동적 변화를 줄 수 있다."},
                            {"role": "user", "content": f"topic: {topic} \n opinion: {opinion}"}

                        ],
                        temperature=0.7,
                        #max_tokens=64,
                        top_p=1,
                        stream= True
                    )
                st.info(response)

                streamed_text = " "
                for chunk in response:
                    chunk_content = chunk.choices[0].delta.content
                    if chunk_content is not None:
                        streamed_text = streamed_text + chunk_content
                        placeholder.info(streamed_text)
            else:
                st.error('모든 양식을 작성하여 주십시오.')
