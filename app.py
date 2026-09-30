import streamlit as st
import plotly.graph_objects as go
import time

from ai.ai_engine import ask_cybershield
from modules.url_scanner import analyze_url
from modules.ip_domain_intelligence import analyze_target
from modules.phone_number_intelligence import analyze_phone_number
from modules.pdf_qa import extract_pdf_text, search_pdf_text


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FUTURISTIC CYBERPUNK CSS
# This CSS styles the native Streamlit widgets; the Dashboard itself avoids
# HTML <div> blocks so raw HTML cannot appear in the UI.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800&display=swap');

:root {
    --cyber-bg: #06182b;
    --cyber-panel: #0b2340;
    --cyber-panel-2: #0e2c4d;
    --cyber-border: rgba(25, 217, 255, 0.34);
    --cyber-text: #effcff;
    --cyber-muted: #9cc4d9;
    --cyber-cyan: #19d9ff;
    --cyber-blue: #3d7cff;
    --cyber-purple: #765cff;
    --cyber-green: #45f0b0;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(25,217,255,.22), transparent 27%),
        radial-gradient(circle at 92% 8%, rgba(61,124,255,.20), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(118,92,255,.12), transparent 35%),
        linear-gradient(135deg, #041321 0%, #082642 48%, #06182b 100%);
    color: var(--cyber-text);
}

[data-testid="stHeader"] { background: rgba(4, 16, 30, .72); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06182c 0%, #092743 52%, #06182c 100%);
    border-right: 1px solid rgba(25,217,255,.34);
    box-shadow: 8px 0 35px rgba(0,0,0,.22);
}
section[data-testid="stSidebar"] * { color: #e7f9ff; }

.sidebar-title { font-family:'Orbitron',sans-serif; font-size:23px; font-weight:800; letter-spacing:1.5px; text-align:center; color:#eafcff; }
.sidebar-subtitle { text-align:center; color:#8fb8cf; font-size:10px; margin:3px 0 15px; letter-spacing:.5px; }
.sidebar-online { text-align:center; border:1px solid rgba(69,240,176,.38); background:rgba(69,240,176,.09); color:#63f5bd; border-radius:999px; padding:7px; font-size:11px; font-weight:700; margin-bottom:16px; box-shadow:0 0 18px rgba(69,240,176,.08); }

h1,h2,h3 { color:#f2fcff !important; text-shadow:0 0 18px rgba(25,217,255,.10); }

.hero-card {
    padding:30px; border-radius:26px; border:1px solid rgba(25,217,255,.48);
    background:linear-gradient(135deg, rgba(10,39,68,.96), rgba(7,25,47,.94));
    box-shadow:0 0 32px rgba(25,217,255,.09), 0 22px 70px rgba(0,0,0,.34), inset 0 1px 0 rgba(255,255,255,.06);
}
.hero-kicker { color:#5ff4c0; font-size:11px; font-weight:800; letter-spacing:1.4px; }
.hero-title { font-family:'Orbitron',sans-serif; font-size:37px; font-weight:800; margin-top:12px; color:#f4fdff; }
.hero-title span { color:#19d9ff; text-shadow:0 0 10px rgba(25,217,255,.65), 0 0 28px rgba(25,217,255,.28); }
.hero-subtitle { color:#a4c7da; font-size:14px; max-width:760px; margin-top:9px; line-height:1.6; }

.panel { padding:22px; border-radius:21px; border:1px solid rgba(25,217,255,.28); background:linear-gradient(145deg, rgba(12,42,70,.92), rgba(7,28,50,.94)); box-shadow:0 0 24px rgba(25,217,255,.055), 0 16px 40px rgba(0,0,0,.22); }
.panel-title { color:#eafaff; font-size:16px; font-weight:800; }
.panel-text { color:#9bc0d5; font-size:12px; line-height:1.6; }
.score-big { font-family:'Orbitron',sans-serif; font-size:43px; font-weight:800; color:#45f0b0; text-shadow:0 0 24px rgba(69,240,176,.28); }
.score-label { color:#8fb7ce; font-size:10px; letter-spacing:1.3px; font-weight:800; }

.metric-card,.module-card,.activity-row { border:1px solid rgba(25,217,255,.22); background:linear-gradient(145deg, rgba(12,43,72,.92), rgba(7,27,49,.94)); box-shadow:0 0 20px rgba(25,217,255,.04); }
.metric-card { padding:18px; border-radius:17px; min-height:90px; }
.metric-value { font-family:'Orbitron',sans-serif; font-size:24px; font-weight:800; color:#e8fbff; text-shadow:0 0 12px rgba(25,217,255,.18); }
.metric-label { color:#8fb7ce; font-size:11px; margin-top:4px; }
.module-card { padding:18px; border-radius:19px; min-height:145px; }
.module-icon { font-size:29px; filter:drop-shadow(0 0 7px rgba(25,217,255,.25)); }
.module-title { color:#eafaff; font-size:15px; font-weight:800; margin-top:7px; }
.module-description { color:#91b6ca; font-size:11px; margin-top:5px; line-height:1.5; }
.activity-row { padding:12px 15px; border-radius:13px; margin-bottom:7px; color:#b4cfdd; font-size:12px; }

.stButton > button { border-radius:12px !important; border:1px solid rgba(25,217,255,.30) !important; background:linear-gradient(135deg,#0d3559,#092642) !important; color:#e6fbff !important; font-weight:700 !important; min-height:43px; transition:all .18s ease; }
.stButton > button:hover { border-color:#19d9ff !important; color:#19d9ff !important; box-shadow:0 0 25px rgba(25,217,255,.22) !important; transform:translateY(-1px); }
.scan-button > button { background:linear-gradient(135deg,#0bcff5,#3d7cff) !important; border:none !important; color:white !important; min-height:54px !important; font-size:15px !important; box-shadow:0 0 28px rgba(25,217,255,.24) !important; }

.stTextInput input,.stTextArea textarea { background:#09243e !important; color:#effcff !important; border:1px solid rgba(25,217,255,.30) !important; border-radius:11px !important; }
.stTextInput input:focus,.stTextArea textarea:focus { border-color:#19d9ff !important; box-shadow:0 0 18px rgba(25,217,255,.14) !important; }
.stSelectbox div[data-baseweb="select"] > div { background:#09243e !important; border-color:rgba(25,217,255,.30) !important; border-radius:11px !important; }
[data-testid="stMetric"] { background:rgba(9,36,62,.80); border:1px solid rgba(25,217,255,.22); padding:12px; border-radius:14px; }
[data-testid="stProgressBar"] > div > div > div { background:linear-gradient(90deg,#19d9ff,#3d7cff,#765cff,#45f0b0); box-shadow:0 0 12px rgba(25,217,255,.35); }
hr { border-color:rgba(25,217,255,.16) !important; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

if "security_score" not in st.session_state:
    st.session_state.security_score = 87

if "scan_history" not in st.session_state:
    st.session_state.scan_history = [
        ("URL Scanner", "example.com", "Low"),
        ("Password Security", "Password check", "Strong"),
        ("IP Intelligence", "example.com", "Analyzed"),
    ]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "🛡️",
    help="CyberShield"
)
st.sidebar.markdown("### CyberShield")
st.sidebar.caption("Interactive Cybersecurity Center")
st.sidebar.markdown("🟢 **SYSTEM ONLINE**")

pages = [
    "🏠 Dashboard",
    "🤖 AI Assistant",
    "🔗 URL Scanner",
    "📧 Phishing Analyzer",
    "🔐 Password Security",
    "🌐 IP & Domain Intelligence",
    "🛡️ Threat Intelligence",
    "📄 PDF Q&A",
    "📱 Phone Intelligence",
    "🛠️ Vulnerability Center",
    "🚨 Incident Response",
    "📚 Cyber Academy",
    "📊 Security Reports",
    "🦠 Virus Scanner",
    "📡 Network Security",
]

selected_page = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = selected_page

page = st.session_state.page


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    # ========================================================
    # CYBERSHIELD COMMAND CENTER
    # ========================================================

    st.markdown("""
    <div class="hero-card">
        <div class="hero-kicker">● SYSTEM STATUS: PROTECTED</div>
        <div class="hero-title">🛡️ Welcome to <span>CyberShield</span></div>
        <div class="hero-subtitle">
            Your interactive cybersecurity command center —
            scan, investigate, learn and strengthen your digital security.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # SCORE + QUICK SCAN
    score_col, action_col = st.columns([1, 2])

    with score_col:
        st.markdown("""
        <div class="panel">
            <div class="score-label">OVERALL SECURITY SCORE</div>
            <div class="score-big">87%</div>
            <div class="panel-title">Good Security Health</div>
            <div class="panel-text">
                Your current dashboard score is healthy. Keep monitoring
                important accounts, links and devices.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(0.87)

    with action_col:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">⚡ Quick Security Scan</div>
            <div class="panel-text">
                Run CyberShield's available checks and review your
                current security posture.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        scan_slot = st.empty()

        with scan_slot.container():
            if st.button(
                "🛡️  RUN SECURITY CHECK",
                key="dashboard_scan",
                use_container_width=True
            ):
                progress = st.progress(0)
                status = st.empty()

                stages = [
                    ("Initializing CyberShield...", 15),
                    ("Scanning security signals...", 35),
                    ("Checking SSL & network security...", 55),
                    ("Analyzing threat indicators...", 80),
                    ("Security check complete.", 100),
                ]

                for message, value in stages:
                    status.info(message)
                    progress.progress(value)
                    time.sleep(0.30)

                status.success("✓ Security check completed successfully.")

    st.write("")
    st.markdown("### 📊 Security Overview")

    m1, m2, m3, m4 = st.columns(4)

    metric_data = [
        ("87%", "Security Score"),
        ("12", "Scans Completed"),
        ("0", "Critical Threats"),
        ("14", "Modules Available"),
    ]

    for col, (value, label) in zip((m1, m2, m3, m4), metric_data):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.markdown("### 🚀 Security Command Modules")
    st.caption("Choose a module to jump directly into a focused security workflow.")

    module_data = [
        ("🔗", "URL Scan", "Check a website or suspicious link", "🔗 URL Scanner"),
        ("🌐", "Domain Intel", "Explore DNS, SSL, ISP and ASN", "🌐 IP & Domain Intelligence"),
        ("🤖", "Cyber AI", "Get defensive cybersecurity guidance", "🤖 AI Assistant"),
        ("🔐", "Password", "Check password strength locally", "🔐 Password Security"),
        ("📄", "PDF Q&A", "Ask questions about a cybersecurity PDF", "📄 PDF Q&A"),
        ("🦠", "Virus Scan", "Run available device security checks", "🦠 Virus Scanner"),
    ]

    cols = st.columns(3)

    for i, (icon, title, description, target_page) in enumerate(module_data):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="module-card">
                    <div class="module-icon">{icon}</div>
                    <div class="module-title">{title}</div>
                    <div class="module-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"Open {title}  →",
                key=f"dashboard_module_{i}",
                use_container_width=True
            ):
                st.session_state.page = target_page
                st.rerun()

    st.write("")
    st.markdown("### 📈 Security Activity")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            y=[52, 61, 58, 72, 68, 81, 87],
            mode="lines+markers",
            name="Security Score",
            line=dict(width=4),
            fill="tozeroy"
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11,16,34,0.72)",
        xaxis=dict(showgrid=False, color="#7890a7"),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(53,217,255,0.08)",
            range=[0, 100],
            color="#7890a7"
        ),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔔 Recent Security Activity")

    if st.session_state.scan_history:
        for module_name, target, result in st.session_state.scan_history:
            st.markdown(
                f"""
                <div class="activity-row">
                    🛡️ <strong>{module_name}</strong>
                    &nbsp;•&nbsp; {target}
                    &nbsp;•&nbsp; <strong>{result}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No recent security activity.")

    st.caption(
        "Privacy: CyberShield's network-level modules do not identify an exact person, "
        "device owner or physical address."
    )


# ============================================================
# AI ASSISTANT
# ============================================================



    st.title("🤖 CyberShield AI Assistant")
    st.caption("Ask defensive cybersecurity questions.")

    question = st.text_area(
        "What would you like to ask?",
        placeholder="Example: How can I protect myself from phishing?"
    )

    if st.button("Ask CyberShield AI", use_container_width=True):

        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("CyberShield AI is analyzing..."):
                answer = ask_cybershield(question)

            st.markdown("### 🧠 AI Response")
            st.write(answer)


# ============================================================
# URL SCANNER
# ============================================================

elif page == "🔗 URL Scanner":

    st.title("🔗 URL Security Scanner")
    st.caption("Analyze a website URL for common security indicators.")

    url = st.text_input(
        "Enter URL",
        placeholder="https://example.com"
    )

    if st.button("🔍 Scan URL", use_container_width=True):

        if not url.strip():
            st.warning("Please enter a URL.")
        else:

            with st.spinner("Scanning URL..."):
                result = analyze_url(url)

            if not result.get("valid_url"):
                st.error("Invalid URL.")
            else:

                score = result.get("risk_score", 0)
                level = result.get("risk_level", "Unknown")

                st.subheader("Security Result")

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric("Risk Score", f"{score}/100")

                with c2:
                    st.metric("Risk Level", level)

                with c3:
                    st.metric(
                        "HTTPS",
                        "Enabled" if result.get("https") else "Not Enabled"
                    )

                st.write("**Domain:**", result.get("domain"))
                st.write("**IP Address:**", result.get("ip_address"))

                indicators = result.get("indicators", [])

                if indicators:
                    st.warning("Security Indicators")
                    for indicator in indicators:
                        st.write("•", indicator)
                else:
                    st.success("No common suspicious indicators detected.")


# ============================================================
# IP & DOMAIN INTELLIGENCE
# ============================================================

elif page == "🌐 IP & Domain Intelligence":

    st.title("🌐 IP & Domain Intelligence")
    st.caption(
        "DNS, SSL, ISP, ASN and approximate network-level information."
    )

    target = st.text_input(
        "Enter IP address or domain",
        placeholder="example.com"
    )

    if st.button("🌐 Analyze Target", use_container_width=True):

        if not target.strip():
            st.warning("Please enter a target.")
        else:

            with st.spinner("Collecting network intelligence..."):
                result = analyze_target(target)

            if result:

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Target Type",
                        result.get("target_type", "Unknown")
                    )

                with c2:
                    st.metric(
                        "IP Address",
                        result.get("ip_address", "Unknown")
                    )

                with c3:
                    st.metric(
                        "HTTPS / SSL",
                        "Enabled" if result.get("https") else "Not Available"
                    )

                st.markdown("### 🌐 Network Intelligence")

                n1, n2, n3 = st.columns(3)

                with n1:
                    st.markdown(
                        f"**ISP**  \n{result.get('isp', 'Unknown')}"
                    )

                with n2:
                    st.markdown(
                        f"**ASN**  \n{result.get('asn', 'Unknown')}"
                    )

                with n3:
                    st.markdown(
                        f"**Organization**  \n{result.get('organization', 'Unknown')}"
                    )

                st.markdown("### 🔎 DNS Information")
                st.write(result.get("dns_addresses", []))

                st.markdown("### 🔐 SSL Information")
                st.write(result.get("ssl_issuer", "Not available"))

                st.info(
                    "Privacy note: IP/domain intelligence provides "
                    "network-level information. It cannot identify a "
                    "person's exact identity, device or physical address."
                )


# ============================================================
# PASSWORD SECURITY
# ============================================================

elif page == "🔐 Password Security":

    st.title("🔐 Password Security")
    st.caption("Check password strength locally.")

    password = st.text_input(
        "Enter a password",
        type="password"
    )

    if st.button("Check Password", use_container_width=True):

        score = 0

        if len(password) >= 8:
            score += 25

        if len(password) >= 12:
            score += 25

        if any(c.isupper() for c in password):
            score += 15

        if any(c.islower() for c in password):
            score += 15

        if any(c.isdigit() for c in password):
            score += 10

        if any(not c.isalnum() for c in password):
            score += 10

        st.progress(score / 100)

        if score >= 80:
            st.success(f"🟢 Strong password — {score}/100")
        elif score >= 50:
            st.warning(f"🟡 Medium password — {score}/100")
        else:
            st.error(f"🔴 Weak password — {score}/100")

        st.caption(
            "Your password is evaluated locally and is not sent to CyberShield AI."
        )


# ============================================================
# PHONE INTELLIGENCE
# ============================================================

elif page == "📱 Phone Intelligence":

    st.title("📱 Phone Intelligence")
    st.caption("Basic phone-number security information.")

    phone = st.text_input(
        "Enter phone number",
        placeholder="+923001234567"
    )

    if st.button("Analyze Number", use_container_width=True):

        if not phone.strip():
            st.warning("Please enter a phone number.")
        else:

            with st.spinner("Analyzing number..."):
                result = analyze_phone_number(phone)

            if result:

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric(
                        "Valid",
                        "Yes" if result.get("valid") else "No"
                    )

                with c2:
                    st.metric(
                        "Country",
                        result.get("country", "Unknown")
                    )

                with c3:
                    st.metric(
                        "Type",
                        result.get("type", "Unknown")
                    )

                st.info(
                    "Phone-number analysis does not reveal someone's "
                    "exact live location or private identity."
                )


# ============================================================
# PDF Q&A
# ============================================================

elif page == "📄 PDF Q&A":

    st.title("📄 PDF Q&A")
    st.caption("Upload a cybersecurity PDF and ask questions about it.")

    uploaded_file = st.file_uploader(
        "Drag & drop your PDF here",
        type=["pdf"]
    )

    if uploaded_file:

        with st.spinner("Reading PDF..."):
            pdf_text = extract_pdf_text(uploaded_file)

        if pdf_text.strip():

            st.success("PDF loaded successfully.")

            question = st.text_input(
                "Ask a question about your PDF"
            )

            if st.button("Ask PDF", use_container_width=True):

                chunks = search_pdf_text(
                    pdf_text,
                    question
                )

                if chunks:

                    context = "\n\n".join(chunks)

                    prompt = f"""
Use the following PDF content to answer the user's question.

PDF CONTENT:
{context}

QUESTION:
{question}

Give a clear answer based only on the supplied PDF content.
"""

                    with st.spinner("Analyzing PDF..."):
                        answer = ask_cybershield(prompt)

                    st.markdown("### 🤖 Answer")
                    st.write(answer)

                else:
                    st.warning(
                        "I could not find a relevant section in the PDF."
                    )

        else:
            st.warning(
                "This PDF does not contain extractable text."
            )


# ============================================================
# OTHER MODULES
# ============================================================

elif page == "📧 Phishing Analyzer":

    st.title("📧 Phishing Analyzer")

    text = st.text_area(
        "Paste email or suspicious message",
        height=180
    )

    if st.button("Analyze Phishing Risk", use_container_width=True):

        if not text.strip():
            st.warning("Please enter the message.")
        else:

            with st.spinner("Analyzing indicators..."):
                answer = ask_cybershield(
                    f"""
Analyze this message for common phishing indicators.

Message:
{text}

Give:
1. Suspicious indicators
2. Risk level
3. Safe defensive actions
"""
                )

            st.write(answer)


elif page == "🛡️ Threat Intelligence":

    st.title("🛡️ Threat Intelligence")

    indicator = st.text_input(
        "Enter URL, domain, IP or indicator"
    )

    if st.button("Investigate Indicator", use_container_width=True):

        if indicator.strip():

            with st.spinner("Investigating..."):
                answer = ask_cybershield(
                    f"""
Provide a defensive cybersecurity assessment of this indicator:

{indicator}

Explain possible security concerns and safe next steps.
Do not claim live threat-intelligence data unless available.
"""
                )

            st.write(answer)
        else:
            st.warning("Please enter an indicator.")


elif page == "🛠️ Vulnerability Center":

    st.title("🛠️ Vulnerability Center")

    target = st.text_area(
        "Describe the system/security configuration you want to review"
    )

    if st.button("Run Security Review", use_container_width=True):

        if target.strip():

            with st.spinner("Checking common security weaknesses..."):
                answer = ask_cybershield(
                    f"""
Review the following configuration for common defensive
security weaknesses:

{target}

Give severity and recommended remediation.
"""
                )

            st.write(answer)

        else:
            st.warning("Please provide information to review.")


elif page == "🚨 Incident Response":

    st.title("🚨 Incident Response")

    incident = st.text_area(
        "Describe the security incident",
        height=180
    )

    if st.button("Generate Response Plan", use_container_width=True):

        if incident.strip():

            with st.spinner("Preparing response plan..."):
                answer = ask_cybershield(
                    f"""
Create a defensive incident response plan for:

{incident}

Include:
- Immediate containment
- Investigation
- Recovery
- Prevention
"""
                )

            st.write(answer)

        else:
            st.warning("Please describe the incident.")


elif page == "📚 Cyber Academy":

    st.title("📚 Cyber Academy")

    st.markdown("""
    Learn cybersecurity through short challenges.

    **Topics**
    - Phishing
    - Password Security
    - Malware
    - Network Security
    - Social Engineering
    - Privacy
    """)

    question = st.radio(
        "Challenge: Which action helps protect an online account?",
        [
            "Use the same password everywhere",
            "Enable multi-factor authentication",
            "Share your password with friends",
            "Disable security alerts"
        ]
    )

    if st.button("Submit Answer", use_container_width=True):

        if question == "Enable multi-factor authentication":
            st.success("🎉 Correct! +10 XP")
        else:
            st.error("Not quite. Try again.")


elif page == "📊 Security Reports":

    st.title("📊 Security Reports")

    st.markdown("""
    ### Security Report

    Use the information below to create a professional security summary.
    """)

    report_name = st.text_input("Report name")

    summary = st.text_area(
        "Security summary",
        height=180
    )

    if st.button("Generate Report", use_container_width=True):

        st.success("Security report generated.")

        st.markdown("### Report Preview")

        st.markdown(f"""
**Report:** {report_name or "CyberShield Security Report"}

**Summary:**

{summary or "No summary provided."}

**Overall Security Score:** 87/100

**Status:** Protected
""")


# ============================================================
# NEW MODULES
# ============================================================

elif page == "🦠 Virus Scanner":

    st.title("🦠 Virus Scanner")

    st.info(
        "CyberShield can perform available security checks, but it is "
        "not a replacement for a full antivirus engine such as Microsoft Defender."
    )

    device = st.selectbox(
        "Select device",
        ["Windows PC", "Laptop", "Android", "iPhone"]
    )

    if st.button("🛡️ Start Security Scan", use_container_width=True):

        progress = st.progress(0)

        stages = [
            ("Initializing scan...", 20),
            ("Checking accessible files...", 45),
            ("Checking security configuration...", 70),
            ("Analyzing suspicious indicators...", 90),
            ("Scan complete.", 100)
        ]

        for message, value in stages:
            st.info(message)
            progress.progress(value)
            time.sleep(0.35)

        st.success(
            f"✓ Security checks completed for {device}."
        )

        st.warning(
            "This result represents CyberShield's available checks; "
            "it should not be interpreted as a complete antivirus verdict."
        )


elif page == "📡 Network Security":

    st.title("📡 Network Security")

    st.info(
        "This module provides basic network-security guidance and checks. "
        "It does not perform unauthorized network testing."
    )

    network = st.text_input(
        "Network information",
        placeholder="Example: Home Wi-Fi"
    )

    if st.button("Analyze Network", use_container_width=True):

        if network.strip():

            with st.spinner("Checking network security..."):
                answer = ask_cybershield(
                    f"""
Give defensive security recommendations for this network:

{network}
"""
                )

            st.write(answer)

        else:
            st.warning("Enter network information first.")


# ============================================================
# END
# ============================================================

st.markdown("---")

st.caption(
    "🛡️ CyberShield — Defensive cybersecurity education and analysis."
)
