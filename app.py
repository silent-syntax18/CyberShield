import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import plotly.graph_objects as go

from ai.ai_engine import ask_cybershield
from modules.url_scanner import analyze_url
from modules.ip_domain_intelligence import analyze_target
from modules.phone_number_intelligence import analyze_phone_number
from modules.pdf_qa import extract_pdf_text, search_pdf_text


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CyberShield 2026",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #07111f;
    color: #e8f1ff;
}

[data-testid="stSidebar"] {
    background: #0b1728;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    color: #8fa8c7;
    font-size: 17px;
}

.card {
    background: #0d1b2e;
    border: 1px solid #1d3553;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛡️ CyberShield 2026")
st.sidebar.caption("AI-Powered Cybersecurity Platform")

page = st.sidebar.radio(
    "Security Modules",
    [
        "🏠 Dashboard",
        "🤖 AI Assistant",
        "🔗 URL Scanner",
        "📄 PDF Q&A",
        "📧 Phishing Analyzer",
        "🔐 Password Security",
        "🌐 IP & Domain Intelligence",
        "🦠 Threat Intelligence",
        "📱 Phone Number Intelligence",
        "🛡️ Vulnerability Center",
        "🚨 Incident Response",
        "📚 Cyber Academy",
        "📊 Security Reports"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("CyberShield AI • RAG • Threat Analysis")


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🛡️ CyberShield 2026</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-powered cybersecurity monitoring and threat analysis platform</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Security Score", "87%")

    with col2:
        st.metric("Threats Detected", "24")

    with col3:
        st.metric("URLs Scanned", "156")

    with col4:
        st.metric("System Status", "Protected")

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.markdown("### 📊 Risk Distribution")

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Low", "Medium", "High"],
                    values=[65, 25, 10],
                    hole=0.55
                )
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.markdown("### 📈 Threat Activity")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                y=[4, 7, 5, 10, 8, 13, 9],
                mode="lines+markers",
                name="Threats"
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="card">
        <h3>🔐 CyberShield Protection Engine</h3>
        <p>
        Monitor suspicious URLs, analyze phishing attempts,
        investigate domains and IP addresses, and use AI-powered
        cybersecurity guidance.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "🤖 AI Assistant":

    st.title("🤖 CyberShield AI Assistant")

    st.write(
        "Ask cybersecurity questions and get AI-powered answers "
        "using the CyberShield knowledge base."
    )

    language = st.selectbox(
        "Response Language",
        ["English", "Roman Urdu"]
    )

    question = st.text_area(
        "Enter your cybersecurity question",
        placeholder="Example: How can I identify a phishing email?"
    )

    if st.button("🚀 Ask CyberShield AI", use_container_width=True):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("CyberShield AI is analyzing..."):

                try:

                    answer = ask_cybershield(
                        question,
                        language=language
                    )

                    st.markdown("### 🧠 AI Response")

                    st.markdown(
                        f'<div class="card">{answer}</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(f"AI Error: {e}")


# ============================================================
# URL SCANNER
# ============================================================

elif page == "🔗 URL Scanner":

    st.title("🔗 CyberShield URL Scanner")

    st.write(
        "Perform a safe, non-invasive security analysis of a URL."
    )

    url = st.text_input(
        "Enter URL",
        placeholder="https://example.com"
    )

    if st.button("🔍 Scan URL", use_container_width=True):

        if not url.strip():

            st.warning("Please enter a URL.")

        else:

            with st.spinner("Analyzing URL..."):

                try:

                    result = analyze_url(url)

                    st.markdown("### 🔎 Scan Results")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Risk Score",
                            f"{result['risk_score']}/100"
                        )

                    with col2:
                        st.metric(
                            "Risk Level",
                            result["risk_level"]
                        )

                    with col3:
                        st.metric(
                            "HTTPS",
                            "Enabled" if result["https"]
                            else "Not Enabled"
                        )

                    st.markdown("---")

                    st.write(
                        "**Domain:**",
                        result["domain"]
                    )

                    st.write(
                        "**Resolved IP:**",
                        result["ip_address"]
                    )

                    st.write(
                        "**Valid URL:**",
                        "Yes" if result["valid_url"] else "No"
                    )

                    st.markdown("### ⚠️ Security Indicators")

                    if result["indicators"]:

                        for indicator in result["indicators"]:

                            st.warning(
                                "⚠️ " + indicator
                            )

                    else:

                        st.success(
                            "✅ No suspicious indicators were "
                            "detected by the current URL rules."
                        )

                    st.info(
                        "A URL alone cannot determine a person's "
                        "exact identity, physical location, or exact device."
                    )

                except Exception as e:

                    st.error(
                        f"Scanner Error: {e}"
                    )


# ============================================================
# PHISHING ANALYZER
# ============================================================

elif page == "📧 Phishing Analyzer":

    st.title("📧 Phishing Email Analyzer")

    st.write(
        "Paste an email or message to analyze possible phishing indicators."
    )

    email_text = st.text_area(
        "Email / Message",
        height=250,
        placeholder="Paste suspicious email text here..."
    )

    if st.button(
        "🕵️ Analyze Message",
        use_container_width=True
    ):

        if not email_text.strip():

            st.warning(
                "Please paste an email or message."
            )

        else:

            with st.spinner(
                "Analyzing phishing indicators..."
            ):

                try:

                    prompt = f"""
Analyze the following email/message for phishing indicators.

Identify:
- suspicious language
- urgency or pressure
- fake login requests
- suspicious links
- credential requests
- social engineering indicators
- recommended safe actions

Email/message:

{email_text}
"""

                    answer = ask_cybershield(
                        prompt
                    )

                    st.markdown(
                        "### 🧠 CyberShield Analysis"
                    )

                    st.markdown(
                        f'<div class="card">{answer}</div>',
                        unsafe_allow_html=True
                    )

                except Exception as e:

                    st.error(
                        f"Analyzer Error: {e}"
                    )


# ============================================================
# PASSWORD SECURITY
# ============================================================

elif page == "🔐 Password Security":

    st.title("🔐 Password Security Checker")

    password = st.text_input(
        "Enter a password to check",
        type="password"
    )

    if st.button(
        "🔎 Check Password",
        use_container_width=True
    ):

        if not password:

            st.warning(
                "Please enter a password."
            )

        else:

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

            st.metric(
                "Password Strength Score",
                f"{score}/100"
            )

            if score >= 80:

                st.success(
                    "🟢 Strong password"
                )

            elif score >= 50:

                st.warning(
                    "🟡 Moderate password"
                )

            else:

                st.error(
                    "🔴 Weak password"
                )

            st.info(
                "Use unique passwords for important accounts "
                "and enable multi-factor authentication."
            )


# ============================================================
# IP & DOMAIN INTELLIGENCE
# ============================================================

elif page == "🌐 IP & Domain Intelligence":

    st.title("🌐 IP & Domain Intelligence")

    st.write(
        "Investigate publicly available information about "
        "an IP address or domain."
    )

    target = st.text_input(
        "Enter IP address or domain",
        placeholder="example.com or 8.8.8.8"
    )

    if st.button(
        "🔎 Investigate",
        use_container_width=True
    ):

        if not target.strip():

            st.warning(
                "Please enter an IP address or domain."
            )

        else:

            with st.spinner(
                "Collecting public intelligence..."
            ):

                try:

                    result = analyze_target(target)

                    # ----------------------------------------
                    # BASIC INFORMATION
                    # ----------------------------------------

                    st.markdown("### 🎯 Target Information")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Target Type",
                            result["type"]
                        )

                    with col2:
                        st.metric(
                            "IP Address",
                            result["ip_address"]
                            or "Unavailable"
                        )

                    with col3:

                        if result["ssl"].get("https"):
                            ssl_status = "Enabled"
                        else:
                            ssl_status = "Unavailable"

                        st.metric(
                            "HTTPS / SSL",
                            ssl_status
                        )

                    st.markdown("---")

                    # ----------------------------------------
                    # DOMAIN
                    # ----------------------------------------

                    if result["domain"]:

                        st.markdown("### 🌐 Domain")

                        st.write(
                            result["domain"]
                        )

                    # ----------------------------------------
                    # DNS INFORMATION
                    # ----------------------------------------

                    st.markdown("### 🔎 DNS Information")

                    dns = result.get("dns", {})

                    if dns:

                        st.write(
                            "**Hostname:**",
                            dns.get(
                                "hostname",
                                "Unavailable"
                            )
                        )

                        aliases = dns.get(
                            "aliases",
                            []
                        )

                        addresses = dns.get(
                            "ip_address",
                            []
                        )

                        st.write(
                            "**Aliases:**",
                            ", ".join(aliases)
                            if aliases
                            else "None"
                        )

                        st.write(
                            "**Resolved Addresses:**",
                            ", ".join(addresses)
                            if addresses
                            else "Unavailable"
                        )

                    else:

                        st.info(
                            "DNS information is unavailable."
                        )

                    # ----------------------------------------
                    # SSL INFORMATION
                    # ----------------------------------------

                    st.markdown("### 🔐 HTTPS / SSL Information")

                    ssl_info = result.get(
                        "ssl",
                        {}
                    )

                    if ssl_info.get("https"):

                        st.success(
                            "✅ HTTPS connection is available."
                        )

                        st.write(
                            "**Certificate Issuer:**",
                            ssl_info.get(
                                "issuer",
                                "Unavailable"
                            )
                        )

                        st.write(
                            "**Certificate Subject:**",
                            ssl_info.get(
                                "subject",
                                "Unavailable"
                            )
                        )

                    else:

                        st.warning(
                            "⚠️ HTTPS/SSL information could not "
                            "be retrieved."
                        )
                    # ----------------------------------------
                    # NETWORK INTELLIGENCE
                    # ----------------------------------------

                    st.markdown("### 🌐 Network Intelligence")

                    intelligence = result.get(
                        "intelligence",
                        {}
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write(
                            "**ISP:**",
                            intelligence.get(
                                "isp",
                                "Unavailable"
                            )
                        )

                        st.write(
                            "**ASN:**",
                            intelligence.get(
                                "asn",
                                "Unavailable"
                            )
                        )

                    with col2:
                        st.write(
                            "**Organization / Hosting:**",
                            intelligence.get(
                                "organization",
                                "Unavailable"
                            )
                        )

                        st.write(
                            "**Country:**",
                            intelligence.get(
                                "country",
                                "Unavailable"
                            )
                        )

                    with col3:
                        st.write(
                            "**Region:**",
                            intelligence.get(
                                "region",
                                "Unavailable"
                            )
                        )

                        st.write(
                            "**City (Approx.):**",
                            intelligence.get(
                                "city",
                                "Unavailable"
                            )
                        )

                    st.markdown("#### 📍 Approximate Location")

                    lat = intelligence.get(
                        "latitude",
                        "Unavailable"
                    )

                    lon = intelligence.get(
                        "longitude",
                        "Unavailable"
                    )

                    st.write(
                        f"**Coordinates:** {lat}, {lon}"
                    )

                    st.write(
                        "**Timezone:**",
                        intelligence.get(
                            "timezone",
                            "Unavailable"
                        )
                    )

                    st.caption(
                        "Location shown here is approximate IP/network "
                        "geolocation and may represent the ISP, hosting "
                        "provider, CDN, or network endpoint rather than "
                        "the user's physical location."
                    )

                    # ----------------------------------------
                    # NOTES
                    # ----------------------------------------

                    st.markdown("### 📝 Intelligence Notes")

                    notes = result.get(
                        "notes",
                        []
                    )

                    if notes:

                        for note in notes:

                            st.info(
                                "ℹ️ " + note
                            )

                    # ----------------------------------------
                    # PRIVACY LIMITATION
                    # ----------------------------------------

                    st.markdown("---")

                    st.info(
                        "🔒 Privacy limitation: IP and domain "
                        "intelligence provides network-level and "
                        "publicly available information. It does "
                        "not identify a person's exact home address, "
                        "exact physical location, or exact identity."
                    )

                except Exception as e:

                    st.error(
                        f"Intelligence Error: {e}"
                    )

# ============================================================
# THREAT INTELLIGENCE
# ============================================================

elif page == "🦠 Threat Intelligence":

    st.title("🦠 Threat Intelligence")

    st.write(
        "Analyze publicly available security indicators "
        "and identify common threat patterns."
    )

    # --------------------------------------------------------
    # THREAT INDICATOR INPUT
    # --------------------------------------------------------

    st.markdown("### 🔎 Threat Indicator Scanner")

    indicator = st.text_input(
        "Enter IP address, domain or URL",
        placeholder="example.com or 8.8.8.8"
    )

    if st.button(
        "🚨 Analyze Threat",
        use_container_width=True
    ):

        if not indicator.strip():

            st.warning(
                "Please enter an IP address, domain or URL."
            )

        else:

            target = indicator.strip().lower()

            # ------------------------------------------------
            # BASIC THREAT ANALYSIS
            # ------------------------------------------------

            risk_score = 0
            indicators = []

            # Suspicious keywords
            suspicious_words = [
                "login",
                "verify",
                "account",
                "password",
                "secure",
                "update",
                "confirm",
                "bank",
                "wallet",
                "free"
            ]

            for word in suspicious_words:

                if word in target:

                    risk_score += 10

                    indicators.append(
                        f"Suspicious keyword detected: {word}"
                    )

            # HTTP instead of HTTPS
            if target.startswith("http://"):

                risk_score += 20

                indicators.append(
                    "Connection uses HTTP instead of HTTPS."
                )

            # IP address indicator
            try:

                import ipaddress

                ipaddress.ip_address(target)

                indicators.append(
                    "Input is a direct IP address."
                )

            except ValueError:

                pass

            # Long suspicious-looking URL
            if len(target) > 80:

                risk_score += 10

                indicators.append(
                    "Unusually long URL or indicator."
                )

            # Final score limit
            risk_score = min(
                risk_score,
                100
            )

            # ------------------------------------------------
            # RISK LEVEL
            # ------------------------------------------------

            if risk_score >= 60:

                risk_level = "High"
                risk_icon = "🔴"

            elif risk_score >= 30:

                risk_level = "Medium"
                risk_icon = "🟠"

            else:

                risk_level = "Low"
                risk_icon = "🟢"

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            st.markdown("---")

            st.markdown("### 🛡️ Threat Analysis Result")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Threat Score",
                    f"{risk_score}/100"
                )

            with col2:

                st.metric(
                    "Risk Level",
                    f"{risk_icon} {risk_level}"
                )

            with col3:

                st.metric(
                    "Indicators",
                    len(indicators)
                )

            # ------------------------------------------------
            # VISUAL RISK BAR
            # ------------------------------------------------

            st.markdown("### 📊 Risk Level")

            st.progress(
                risk_score / 100
            )

            if risk_level == "High":

                st.error(
                    "🔴 High-risk indicators detected. "
                    "Further investigation is recommended."
                )

            elif risk_level == "Medium":

                st.warning(
                    "🟠 Medium-risk indicators detected. "
                    "Review the identified patterns carefully."
                )

            else:

                st.success(
                    "🟢 No major suspicious patterns detected "
                    "by this basic analysis."
                )

            # ------------------------------------------------
            # DETECTED INDICATORS
            # ------------------------------------------------

            st.markdown("### 🚨 Detected Indicators")

            if indicators:

                for item in indicators:

                    st.write(
                        "⚠️",
                        item
                    )

            else:

                st.info(
                    "No suspicious indicators were detected."
                )

            # ------------------------------------------------
            # THREAT CATEGORIES
            # ------------------------------------------------

            st.markdown("### 🧩 Threat Categories")

            category_data = {

                "Category": [
                    "Phishing",
                    "Malware",
                    "Ransomware",
                    "Credential Theft",
                    "Suspicious URLs"
                ],

                "Threat Activity": [
                    42,
                    31,
                    12,
                    25,
                    56
                ]
            }

            st.dataframe(
                category_data,
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # PRIVACY LIMITATION
            # ------------------------------------------------

            st.markdown("---")

            st.info(
                "🔒 Privacy limitation: This module performs "
                "basic indicator analysis using publicly available "
                "patterns. It does not identify a person's exact "
                "identity, device or physical location."
            )
# ============================================================
# PHONE NUMBER INTELLIGENCE
# ============================================================

elif page == "📱 Phone Number Intelligence":

    st.title("📱 Phone Number Intelligence")

    st.write(
        "Analyze basic phone-number information such as "
        "country code, region, number type and risk indicators."
    )

    st.info(
        "🔒 Privacy Note: CyberShield does not identify a "
        "private person's exact live location, home address "
        "or personal identity from a phone number."
    )

    # --------------------------------------------------------
    # PHONE NUMBER INPUT
    # --------------------------------------------------------

    phone_number = st.text_input(
        "Enter phone number",
        placeholder="+923001234567"
    )

    if st.button(
        "📱 Analyze Phone Number",
        use_container_width=True
    ):

        if not phone_number.strip():

            st.warning(
                "Please enter a phone number."
            )

        else:

            try:

                result = analyze_phone_number(
                    phone_number
                )

                st.markdown("---")

                st.markdown(
                    "### 📊 Phone Number Analysis"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Format",
                        "Valid"
                        if result["valid_format"]
                        else "Invalid"
                    )

                with col2:

                    st.metric(
                        "Country Code",
                        result["country_code"]
                    )

                with col3:

                    st.metric(
                        "Country",
                        result["country"]
                    )

                with col4:

                    st.metric(
                        "Number Type",
                        result["number_type"]
                    )

                # ------------------------------------------------
                # REGIONAL INFORMATION
                # ------------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### 🌍 Regional Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Country",
                        result["country"]
                    )

                with col2:

                    st.metric(
                        "Region",
                        result["region"]
                    )

                # ------------------------------------------------
                # RISK ASSESSMENT
                # ------------------------------------------------

                st.markdown("---")

                st.markdown(
                    "### ⚠️ Risk Assessment"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Risk Score",
                        f"{result['risk_score']}/100"
                    )

                with col2:

                    if result["risk_level"] == "Low":

                        st.success(
                            "🟢 Risk Level: Low"
                        )

                    elif result["risk_level"] == "Medium":

                        st.warning(
                            "🟡 Risk Level: Medium"
                        )

                    else:

                        st.error(
                            "🔴 Risk Level: High"
                        )

                # ------------------------------------------------
                # INDICATORS
                # ------------------------------------------------

                st.markdown(
                    "### 🔎 Indicators"
                )

                if result["indicators"]:

                    for indicator in result["indicators"]:

                        st.write(
                            "⚠️",
                            indicator
                        )

                else:

                    st.success(
                        "No basic risk indicators detected."
                    )

            except Exception as e:

                st.error(
                    f"Phone Analysis Error: {e}"
                )
# ============================================================
# VULNERABILITY CENTER
# ============================================================

elif page == "🛡️ Vulnerability Center":

    st.title("🛡️ Vulnerability Center")

    st.write(
        "Perform a basic security assessment of software, "
        "services and configuration indicators."
    )

    # --------------------------------------------------------
    # VULNERABILITY INPUT
    # --------------------------------------------------------

    st.markdown("### 🔎 Security Assessment")

    target = st.text_input(
        "Enter software, service or security configuration",
        placeholder="Example: outdated software, FTP, HTTP, weak password"
    )

    if st.button(
        "🛡️ Run Vulnerability Scan",
        use_container_width=True
    ):

        if not target.strip():

            st.warning(
                "Please enter something to assess."
            )

        else:

            value = target.strip().lower()

            findings = []
            risk_score = 0

            # ------------------------------------------------
            # BASIC SECURITY CHECKS
            # ------------------------------------------------

            if "ftp" in value:

                risk_score += 30

                findings.append(
                    (
                        "🔴 High",
                        "FTP detected",
                        "FTP may transmit credentials without "
                        "encryption. Consider using SFTP or FTPS."
                    )
                )

            if "http" in value and "https" not in value:

                risk_score += 25

                findings.append(
                    (
                        "🟠 Medium",
                        "HTTP detected",
                        "Unencrypted HTTP traffic can expose "
                        "sensitive information."
                    )
                )

            if "weak password" in value:

                risk_score += 35

                findings.append(
                    (
                        "🔴 High",
                        "Weak password configuration",
                        "Use long, unique passwords and enable "
                        "multi-factor authentication."
                    )
                )

            if "outdated" in value:

                risk_score += 30

                findings.append(
                    (
                        "🔴 High",
                        "Outdated software",
                        "Software should be updated regularly to "
                        "receive security fixes."
                    )
                )

            if "telnet" in value:

                risk_score += 35

                findings.append(
                    (
                        "🔴 High",
                        "Telnet detected",
                        "Telnet is an insecure remote-access "
                        "protocol. Consider SSH instead."
                    )
                )

            # ------------------------------------------------
            # FINAL SCORE
            # ------------------------------------------------

            risk_score = min(
                risk_score,
                100
            )

            if risk_score >= 60:

                risk_level = "High"
                icon = "🔴"

            elif risk_score >= 30:

                risk_level = "Medium"
                icon = "🟠"

            else:

                risk_level = "Low"
                icon = "🟢"

            # ------------------------------------------------
            # RESULTS
            # ------------------------------------------------

            st.markdown("---")

            st.markdown(
                "### 📊 Vulnerability Assessment"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Risk Score",
                    f"{risk_score}/100"
                )

            with col2:

                st.metric(
                    "Risk Level",
                    f"{icon} {risk_level}"
                )

            with col3:

                st.metric(
                    "Findings",
                    len(findings)
                )

            st.markdown("### 📈 Risk Level")

            st.progress(
                risk_score / 100
            )

            # ------------------------------------------------
            # FINDINGS
            # ------------------------------------------------

            st.markdown(
                "### ⚠️ Security Findings"
            )

            if findings:

                for severity, title, description in findings:

                    st.markdown(
                        f"**{severity} — {title}**"
                    )

                    st.write(
                        description
                    )

                    st.markdown("---")

            else:

                st.success(
                    "🟢 No known risky pattern was detected "
                    "by this basic assessment."
                )

            # ------------------------------------------------
            # RECOMMENDATIONS
            # ------------------------------------------------

            st.markdown(
                "### 💡 Security Recommendations"
            )

            recommendations = [
                "Keep operating systems and software updated.",
                "Use HTTPS and encrypted protocols.",
                "Use strong and unique passwords.",
                "Enable multi-factor authentication.",
                "Disable unnecessary services and ports.",
                "Monitor systems for unusual activity."
            ]

            for recommendation in recommendations:

                st.write(
                    "✅",
                    recommendation
                )

            # ------------------------------------------------
            # PRIVACY / LIMITATION
            # ------------------------------------------------

            st.markdown("---")

            st.info(
                "🔒 Limitation: This is a basic pattern-based "
                "vulnerability assessment. It does not perform "
                "exploit testing or claim to identify every CVE."
            )
# ============================================================
# INCIDENT RESPONSE
# ============================================================

elif page == "🚨 Incident Response":

    st.title("🚨 Incident Response Center")

    st.write(
        "Analyze a security incident and generate a defensive "
        "response plan using CyberShield AI."
    )

    # --------------------------------------------------------
    # INCIDENT DETAILS
    # --------------------------------------------------------

    st.markdown("### 📝 Incident Details")

    incident = st.text_area(
        "Describe the security incident",
        height=180,
        placeholder=(
            "Example: A suspicious attachment was opened "
            "on a workstation."
        )
    )

    # --------------------------------------------------------
    # INCIDENT SEVERITY
    # --------------------------------------------------------

    severity = st.selectbox(
        "Select incident severity",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

    # --------------------------------------------------------
    # INCIDENT TYPE
    # --------------------------------------------------------

    incident_type = st.selectbox(
        "Incident type",
        [
            "Phishing",
            "Malware",
            "Ransomware",
            "Account Compromise",
            "Data Exposure",
            "Suspicious Activity",
            "Other"
        ]
    )

    # --------------------------------------------------------
    # INCIDENT OVERVIEW
    # --------------------------------------------------------

    if incident.strip():

        st.markdown("---")

        st.markdown(
            "### 📊 Incident Overview"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Severity",
                severity
            )

        with col2:

            st.metric(
                "Incident Type",
                incident_type
            )

        with col3:

            st.metric(
                "Response Status",
                "Ready"
            )

    # --------------------------------------------------------
    # RESPONSE PLAN
    # --------------------------------------------------------

    if st.button(
        "🚨 Generate Response Plan",
        use_container_width=True
    ):

        if not incident.strip():

            st.warning(
                "Please describe the incident."
            )

        else:

            with st.spinner(
                "CyberShield AI is preparing response guidance..."
            ):

                try:

                    prompt = f"""
Create a defensive cybersecurity incident response plan.

Incident Type:
{incident_type}

Severity:
{severity}

Incident Description:
{incident}

Include these sections:

1. Immediate Containment
2. Evidence Preservation
3. Investigation
4. Recovery
5. Prevention

Keep the guidance defensive, practical and safe.
"""

                    answer = ask_cybershield(
                        prompt
                    )

                    # ------------------------------------------------
                    # RESPONSE STATUS
                    # ------------------------------------------------

                    st.markdown("---")

                    st.markdown(
                        "### 🛡️ Response Status"
                    )

                    st.success(
                        "✅ AI response plan generated successfully."
                    )

                    st.progress(
                        100
                    )

                    # ------------------------------------------------
                    # RESPONSE PLAN
                    # ------------------------------------------------

                    st.markdown(
                        "### 📋 CyberShield Response Plan"
                    )

                    st.markdown(
                        f'<div class="card">{answer}</div>',
                        unsafe_allow_html=True
                    )

                    # ------------------------------------------------
                    # RESPONSE CHECKLIST
                    # ------------------------------------------------

                    st.markdown(
                        "### ✅ Response Checklist"
                    )

                    checklist = [
                        "Contain the affected system.",
                        "Preserve relevant evidence.",
                        "Investigate the incident.",
                        "Remove the threat.",
                        "Recover affected systems.",
                        "Apply preventive security measures."
                    ]

                    for item in checklist:

                        st.write(
                            "☐",
                            item
                        )

                    # ------------------------------------------------
                    # SAFETY NOTE
                    # ------------------------------------------------

                    st.info(
                        "🔒 CyberShield provides defensive guidance. "
                        "Verify recommendations before applying them "
                        "to production systems."
                    )

                except Exception as e:

                    st.error(
                        f"Response Error: {e}"
                    )
                    


# ============================================================
# PDF Q&A
# ============================================================

elif page == "📄 PDF Q&A":

    st.title("📄 PDF Q&A")

    st.write(
        "Upload a PDF and ask questions about its content."
    )

    st.info(
        "🔒 Privacy Note: CyberShield processes the uploaded "
        "PDF for analysis. Do not upload confidential or "
        "private documents."
    )

    uploaded_pdf = st.file_uploader(
        "📤 Upload a PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        try:

            pdf_text = extract_pdf_text(
                uploaded_pdf
            )

            if not pdf_text.strip():

                st.warning(
                    "⚠️ No readable text was found in this PDF."
                )

            else:

                st.success(
                    "✅ PDF uploaded and text extracted successfully!"
                )

                word_count = len(
                    pdf_text.split()
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "📄 File",
                        uploaded_pdf.name
                    )

                with col2:

                    st.metric(
                        "📝 Words",
                        word_count
                    )

                st.markdown("---")

                question = st.text_input(
                    "❓ Ask a question about this PDF",
                    placeholder="Example: What is phishing?"
                )

                if st.button(
                    "🤖 Ask from PDF",
                    use_container_width=True
                ):

                    if not question.strip():

                        st.warning(
                            "Please enter a question."
                        )

                    else:

                        relevant_text = search_pdf_text(
                            pdf_text,
                            question
                        )

                        if not relevant_text:

                            st.warning(
                                "No relevant information was found "
                                "in the uploaded PDF."
                            )

                        else:

                            context = "\n\n".join(
                                relevant_text
                            )

                            prompt = f"""
You are CyberShield PDF Assistant.

Answer the user's question using ONLY the
information provided in the PDF context below.

If the answer is not available in the PDF,
clearly say that the information was not
found in the uploaded document.

PDF Context:
{context}

User Question:
{question}

Give a clear and concise answer.
"""

                            with st.spinner(
                                "🤖 Analyzing PDF..."
                            ):

                                answer = ask_cybershield(
                                    prompt
                                )

                            st.markdown("---")

                            st.markdown(
                                "### 🤖 PDF Answer"
                            )

                            st.write(answer)

        except Exception as e:

            st.error(
                f"PDF Analysis Error: {e}"
            )

# ============================================================
# CYBER ACADEMY
# ============================================================

elif page == "📚 Cyber Academy":

    st.title("📚 Cyber Academy")

    st.write(
        "Learn essential cybersecurity concepts through "
        "simple lessons and quick knowledge checks."
    )

    # --------------------------------------------------------
    # TOPIC SELECTION
    # --------------------------------------------------------

    topic = st.selectbox(
        "Choose a cybersecurity topic",
        [
            "Phishing",
            "Password Security",
            "Malware",
            "Ransomware",
            "Social Engineering",
            "Network Security"
        ]
    )

    # --------------------------------------------------------
    # LESSONS
    # --------------------------------------------------------

    lessons = {

        "Phishing": {
            "title": "🎣 Phishing",
            "content": (
                "Phishing is a cyber attack where attackers try "
                "to trick users into revealing sensitive information "
                "through fake emails, messages or websites."
            ),
            "tips": [
                "Check the sender carefully.",
                "Do not click suspicious links.",
                "Never share passwords through email.",
                "Check website addresses before entering information."
            ],
            "question": "What is the main goal of phishing?",
            "options": [
                "Improve internet speed",
                "Trick users into revealing information",
                "Update computer drivers",
                "Create backups"
            ],
            "answer": "Trick users into revealing information"
        },

        "Password Security": {
            "title": "🔐 Password Security",
            "content": (
                "Strong passwords help protect accounts from "
                "unauthorized access. Passwords should be unique "
                "and difficult to guess."
            ),
            "tips": [
                "Use long and unique passwords.",
                "Avoid using personal information.",
                "Use a password manager when possible.",
                "Enable multi-factor authentication."
            ],
            "question": "Which is a good password security practice?",
            "options": [
                "Reuse the same password everywhere",
                "Share your password with friends",
                "Use unique passwords and MFA",
                "Use your name as a password"
            ],
            "answer": "Use unique passwords and MFA"
        },

        "Malware": {
            "title": "🦠 Malware",
            "content": (
                "Malware is malicious software designed to damage "
                "systems, steal information or perform unauthorized actions."
            ),
            "tips": [
                "Keep software updated.",
                "Use trusted security software.",
                "Avoid unknown downloads.",
                "Do not open suspicious attachments."
            ],
            "question": "What does malware mean?",
            "options": [
                "Malicious software",
                "Internet hardware",
                "A backup system",
                "A programming language"
            ],
            "answer": "Malicious software"
        },

        "Ransomware": {
            "title": "🔒 Ransomware",
            "content": (
                "Ransomware is malware that can encrypt or block "
                "access to data and demand payment from victims."
            ),
            "tips": [
                "Keep offline or protected backups.",
                "Keep operating systems updated.",
                "Avoid suspicious attachments and links.",
                "Use endpoint security controls."
            ],
            "question": "What can ransomware do?",
            "options": [
                "Improve computer performance",
                "Encrypt or block access to data",
                "Increase Wi-Fi speed",
                "Create stronger passwords"
            ],
            "answer": "Encrypt or block access to data"
        },

        "Social Engineering": {
            "title": "🎭 Social Engineering",
            "content": (
                "Social engineering involves manipulating people "
                "into performing actions or revealing information."
            ),
            "tips": [
                "Verify unexpected requests.",
                "Do not trust pressure tactics.",
                "Confirm sensitive requests through another channel.",
                "Protect personal information."
            ],
            "question": "What does social engineering target?",
            "options": [
                "Only computer hardware",
                "Human behavior",
                "Internet cables",
                "Computer processors"
            ],
            "answer": "Human behavior"
        },

        "Network Security": {
            "title": "🌐 Network Security",
            "content": (
                "Network security protects systems and data "
                "from unauthorized access and malicious activity."
            ),
            "tips": [
                "Use secure Wi-Fi.",
                "Keep network devices updated.",
                "Use firewalls where appropriate.",
                "Monitor unusual network activity."
            ],
            "question": "What is a firewall commonly used for?",
            "options": [
                "Filtering network traffic",
                "Increasing screen brightness",
                "Editing photos",
                "Creating passwords"
            ],
            "answer": "Filtering network traffic"
        }
    }

    lesson = lessons[topic]

    # --------------------------------------------------------
    # LESSON DISPLAY
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        f"### {lesson['title']}"
    )

    st.info(
        lesson["content"]
    )

    st.markdown(
        "### 🛡️ Security Tips"
    )

    for tip in lesson["tips"]:
        st.write(
            "✅",
            tip
        )

    # --------------------------------------------------------
    # KNOWLEDGE CHECK
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🧠 Quick Knowledge Check"
    )

    answer = st.radio(
        lesson["question"],
        lesson["options"]
    )

    if st.button(
        "✅ Check Answer",
        use_container_width=True
    ):

        if answer == lesson["answer"]:

            st.success(
                "🎉 Correct! Great cybersecurity knowledge."
            )

        else:

            st.error(
                "❌ Not quite. Review the lesson and try again."
            )

    # --------------------------------------------------------
    # SAFETY NOTE
    # --------------------------------------------------------

    st.markdown("---")

    st.info(
        "📚 Cyber Academy provides educational cybersecurity "
        "information for awareness and defensive learning."
    )
# ============================================================
# SECURITY REPORTS
# ============================================================

elif page == "📊 Security Reports":

    st.title("📊 Security Reports")

    st.write(
        "Generate a security assessment report based on "
        "CyberShield analysis results."
    )

    # --------------------------------------------------------
    # REPORT DETAILS
    # --------------------------------------------------------

    st.markdown("### 📝 Report Details")

    report_title = st.text_input(
        "Report Title",
        value="CyberShield Security Assessment"
    )

    analyst = st.text_input(
        "Analyst / User",
        placeholder="Enter your name"
    )

    target = st.text_input(
        "Target",
        placeholder="Example: example.com"
    )

    # --------------------------------------------------------
    # SECURITY STATUS
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 🛡️ Security Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        status = st.selectbox(
            "Overall Status",
            [
                "🟢 Secure",
                "🟡 Needs Attention",
                "🔴 High Risk"
            ]
        )

    with col2:
        score = st.number_input(
            "Security Score",
            min_value=0,
            max_value=100,
            value=80
        )

    with col3:
        findings = st.number_input(
            "Findings",
            min_value=0,
            max_value=100,
            value=0
        )

    # --------------------------------------------------------
    # REPORT SUMMARY
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📋 Report Summary")

    summary = st.text_area(
        "Security assessment summary",
        height=150,
        placeholder=(
            "Describe the security assessment, "
            "detected issues and recommendations."
        )
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    st.markdown("### 💡 Recommendations")

    recommendations = st.text_area(
        "Security recommendations",
        height=150,
        placeholder=(
            "Example:\n"
            "- Enable multi-factor authentication.\n"
            "- Use strong unique passwords.\n"
            "- Keep software updated."
        )
    )

    # --------------------------------------------------------
    # GENERATE REPORT
    # --------------------------------------------------------

    if st.button(
        "📊 Generate Security Report",
        use_container_width=True
    ):

        if not target.strip():

            st.warning(
                "Please enter a target."
            )

        else:

            st.success(
                "✅ Security report generated successfully."
            )

            st.markdown("---")

            st.markdown(
                f"## 🛡️ {report_title}"
            )

            st.markdown(
                f"**Target:** {target}"
            )

            if analyst.strip():

                st.markdown(
                    f"**Analyst:** {analyst}"
                )

            st.markdown("### 📊 Assessment")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Security Score",
                    f"{score}/100"
                )

            with col2:

                st.metric(
                    "Status",
                    status
                )

            with col3:

                st.metric(
                    "Findings",
                    findings
                )

            st.markdown("### 📝 Summary")

            if summary.strip():

                st.write(summary)

            else:

                st.write(
                    "No additional summary provided."
                )

            st.markdown("### 💡 Recommendations")

            if recommendations.strip():

                st.write(recommendations)

            else:

                st.write(
                    "No additional recommendations provided."
                )

            st.markdown("---")

            st.info(
                "🔒 CyberShield reports are intended for "
                "defensive security assessment and awareness. "
                "Verify findings before making security decisions."
            )
