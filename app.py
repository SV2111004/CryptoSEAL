import streamlit as st
from key_manager import generate_keys
from crypto_module import sign_file
from client import send_file

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="CryptoSEAL | Digital Signature System", page_icon="🛡️", layout="wide")

# --------------------------------------------------
# THEME CSS (Cybersecurity Dark Mint)
# --------------------------------------------------
css = """
<style>
body, .stApp {
    background: linear-gradient(180deg, #071019 0%, #0b1220 100%);
}
div.block-container {
    background: rgba(10, 14, 18, 0.78) !important;
    padding: 1.6rem;
    border-radius: 10px;
    border: 1px solid rgba(34, 197, 94, 0.08);
}

/* Headers */
h1, h2, h3, h4 {
    color: #a7f3d0 !important;
}

/* Buttons */
.stButton > button {
    background: transparent;
    color: #a7f3d0;
    border: 1px solid rgba(167,243,208,0.25);
    border-radius: 8px;
    padding: 8px 12px;
    font-weight: 600;
    transition: 0.12s;
}
.stButton > button:hover {
    background: rgba(167,243,208,0.07);
    box-shadow: 0 0 6px rgba(167,243,208,0.07);
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size:15px;
    padding:8px 14px;
    color:#9fe7cb !important;
    font-weight:600;
    border-bottom: 2px solid transparent;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 2px solid rgba(159,231,203,0.18);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(6,10,14,0.9);
    border-right: 1px solid rgba(159,231,203,0.04);
}

/* Code Blocks */
.stCodeBlock pre {
    background: rgba(0,0,0,0.45) !important;
}

/* Shield animations */
.success-shield {
    animation: pulse 1.5s ease-in-out infinite;
    filter: drop-shadow(0 0 12px rgba(0,255,120,0.45));
}
@keyframes pulse {
    0% { transform: scale(1); opacity:1; }
    50% { transform: scale(1.08); opacity:0.85; }
    100% { transform: scale(1); opacity:1; }
}

.fail-shield {
    animation: crack 1s ease-in-out;
    filter: drop-shadow(0 0 10px rgba(255,0,80,0.45));
}
@keyframes crack {
    0% { transform: scale(1); filter: brightness(1); }
    30% { transform: scale(1.1) rotate(-3deg); }
    60% { transform: scale(0.9) rotate(3deg); filter: brightness(3); }
    100% { transform: scale(1); }
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --------------------------------------------------
# STATE INIT
# --------------------------------------------------
if "step" not in st.session_state:
    st.session_state.update({
        "step": 1,
        "private_key": None,
        "public_key": None,
        "signature": None,
        "file": None,
        "new_data": None,
        "tampered": False,
        "response": ""
    })

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div style='display:flex;align-items:center;gap:12px'>
        <span style="font-size:42px;">🛡️</span>
        <div>
            <h2 style='margin:0;color:#a7f3d0;'>CryptoSEAL: Digital Signature Verification System</h2>
            <div style='color:#bfeedc'>RSA • SHA-256 • Authenticity • Integrity • Security</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# --------------------------------------------------
# SIDEBAR PROGRESS
# --------------------------------------------------
with st.sidebar:
    st.subheader("Workflow Progress")
    steps = ["Generate Keys", "Sign File", "Start Server", "Send File", "Verify"]
    for i, step in enumerate(steps, 1):
        icon = "🟢" if st.session_state.step > i else "🔷" if st.session_state.step == i else "⚫"
        st.write(f"{icon} {i}) {step}")
    st.info("Complete each step in order.")

# --------------------------------------------------
# HELPER: TAB LOCK
# --------------------------------------------------
def lock(step_req):
    if st.session_state.step < step_req:
        st.warning("⛓️ Complete previous step first.")
        st.stop()

# --------------------------------------------------
# TABS
# --------------------------------------------------
tabs = st.tabs(["1️⃣ Generate Keys", "2️⃣ Sign File", "3️⃣ Start Server", "4️⃣ Send File", "5️⃣ Verify"])

# TAB 1
with tabs[0]:
    lock(1)
    st.header("🔑 Generate RSA Key Pair")

    if st.button("Generate RSA Keys"):
        priv, pub = generate_keys()
        st.session_state.private_key = priv
        st.session_state.public_key = pub
        st.session_state.step = 2
        st.success("✅ Keys generated & stored securely (keys/ folder)")

# TAB 2
with tabs[1]:
    lock(2)
    st.header("✍️ Sign File")

    file = st.file_uploader("Upload file to Sign", type=["txt"])
    if file:
        data = file.read()
        sig = sign_file(data, st.session_state.private_key)

        st.session_state.file = data
        st.session_state.signature = sig
        st.session_state.step = 3

        st.success("✅ File Signed Successfully")

# TAB 3
with tabs[2]:
    lock(3)
    st.header("📡 Start Receiver Server")
    st.code("python server.py", language="bash")
    st.info("Start server in terminal, then continue")
    st.session_state.step = 4

# TAB 4
with tabs[3]:
    lock(4)
    st.header("📤 Send File to Receiver")

    f2 = st.file_uploader("Re-upload same signed file", type=["txt"], key="send")
    if f2:
        new = f2.read()
        st.session_state.new_data = new
        st.session_state.tampered = (new != st.session_state.file)

        with st.spinner("Sending..."):
            st.session_state.response = send_file(new, st.session_state.signature)

        st.session_state.step = 5
        st.success("📨 File sent to server")

# TAB 5
with tabs[4]:
    lock(5)
    st.header("🧾 Verification Result")

    tampered = st.session_state.tampered
    response = st.session_state.response

    # ✅ Shield Animation
    if tampered or ("Invalid" in response):
        st.markdown("<p class='fail-shield' style='font-size:90px; text-align:center;'>🛡️❌</p>", unsafe_allow_html=True)
        st.error("File Tampered ❌")
    else:
        st.markdown("<p class='success-shield' style='font-size:90px; text-align:center;'>🛡️✅</p>", unsafe_allow_html=True)
        st.success("File Authentic ✅")

    st.write(response)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <br><hr style="border:1px solid rgba(159,231,203,0.15);">
    <div style="text-align:center; color:#9fe7cb; font-size:14px; opacity:0.85;">
        © 2025 <b>CryptoSEAL</b> | Built using Python & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
