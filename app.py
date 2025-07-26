import streamlit as st
from datetime import datetime
from multiple_agent import get_response, agent_team

# CSS for chat bubbles and timestamps
chat_css = """
<style>
.chat-bubble-user {
    background-color: #313d27;
    color: white;
    padding: 0.8rem;
    border-radius: 10px;
    margin-bottom: 0.1rem;
    align-self: flex-end;
    max-width: 80%;
    word-wrap: break-word;
}

.chat-bubble-assistant {
    background-color: #1f1111;
    color: white;
    padding: 0.8rem;
    border-radius: 10px;
    margin-bottom: 0.1rem;
    align-self: flex-start;
    border: 1px solid #eee;
    max-width: 80%;
    word-wrap: break-word;
}


.chat-message {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.8rem;
}

.timestamp {
    font-size: 0.7rem;
    color: #999;
    margin-left: 0.5rem;
}
</style>
"""
st.markdown(chat_css, unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar showing agents info
st.sidebar.title("🧠 Agents Available")
for agent in agent_team.members:
    with st.sidebar.expander(f"🤖 {agent.name}"):
        st.markdown(f"- **Role:** {agent.role}")
        st.markdown(f"- **Tools:** {', '.join(t.__class__.__name__ for t in agent.tools)}")

st.title("💬 Multi-Agent Chat")

# Display chat messages with timestamps
with st.container():
    for pair in st.session_state.chat_history:
        user_html = f'''
        <div class="chat-message">
            <div class="chat-bubble-user">{pair["user"]}</div>
            <div class="timestamp" style="text-align: right;">{pair["user_time"]}</div>
        </div>
        '''
        agent_html = f'''
        <div class="chat-message">
            <div class="chat-bubble-assistant">{pair["agent"]}</div>
            <div class="timestamp" style="text-align: left;">{pair["agent_time"]}</div>
        </div>
        '''
        st.markdown(user_html, unsafe_allow_html=True)
        st.markdown(agent_html, unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", placeholder="e.g. Give me an outlook on the AI chip market")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    with st.spinner("Agents are thinking..."):
        agent_reply = get_response(user_input)
    
    # Current timestamp
    now = datetime.now().strftime("%I:%M %p")

    # Append chat with timestamps
    st.session_state.chat_history.append({
        "user": user_input,
        "agent": agent_reply,
        "user_time": now,
        "agent_time": now
    })

    st.rerun()
