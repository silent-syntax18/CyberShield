import re
import ssl
import socket
from urllib.parse import urlparse


def analyze_url(url):
    """
    Perform a safe, non-invasive URL security analysis.
    """

    result = {
        "url": url,
        "valid_url": False,
        "https": False,
        "domain": "",
        "ip_address": "Unavailable",
        "risk_level": "Low",
        "risk_score": 0,
        "indicators": []
    }

    # --------------------------------------------------------
    # Basic URL validation
    # --------------------------------------------------------

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:
        result["risk_level"] = "High"
        result["risk_score"] = 80
        result["indicators"].append("Invalid or incomplete URL.")
        return result

    result["valid_url"] = True

    domain = parsed.hostname

    if not domain:
        result["risk_level"] = "High"
        result["risk_score"] = 80
        result["indicators"].append("Domain could not be identified.")
        return result

    result["domain"] = domain

    # --------------------------------------------------------
    # HTTPS check
    # --------------------------------------------------------

    if parsed.scheme == "https":
        result["https"] = True
    else:
        result["risk_score"] += 15
        result["indicators"].append(
            "Website is using HTTP instead of HTTPS."
        )

    # --------------------------------------------------------
    # Suspicious URL patterns
    # --------------------------------------------------------

    suspicious_words = [
        "login",
        "verify",
        "account",
        "password",
        "confirm",
        "security",
        "update",
        "wallet",
        "payment",
        "free",
        "urgent"
    ]

    url_lower = url.lower()

    found_words = [
        word for word in suspicious_words
        if word in url_lower
    ]

    if len(found_words) >= 3:
        result["risk_score"] += 20

        result["indicators"].append(
            "URL contains multiple security-sensitive keywords: "
            + ", ".join(found_words)
        )

    # --------------------------------------------------------
    # IP address used instead of domain
    # --------------------------------------------------------

    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    if re.match(ip_pattern, domain):

        result["risk_score"] += 25

        result["indicators"].append(
            "URL uses an IP address instead of a normal domain."
        )

    # --------------------------------------------------------
    # @ symbol
    # --------------------------------------------------------

    if "@" in url:

        result["risk_score"] += 25

        result["indicators"].append(
            "URL contains '@', which can be used to disguise the destination."
        )

    # --------------------------------------------------------
    # Excessively long URL
    # --------------------------------------------------------

    if len(url) > 150:

        result["risk_score"] += 10

        result["indicators"].append(
            "URL is unusually long."
        )

    # --------------------------------------------------------
    # Too many subdomains
    # --------------------------------------------------------

    subdomain_count = len(domain.split("."))

    if subdomain_count >= 5:

        result["risk_score"] += 15

        result["indicators"].append(
            "Domain contains an unusually large number of subdomains."
        )

    # --------------------------------------------------------
    # Domain resolution
    # --------------------------------------------------------

    try:

        ip_address = socket.gethostbyname(domain)

        result["ip_address"] = ip_address

    except Exception:

        result["indicators"].append(
            "Domain could not be resolved to an IP address."
        )

        result["risk_score"] += 10

    # --------------------------------------------------------
    # Risk classification
    # --------------------------------------------------------

    if result["risk_score"] >= 60:

        result["risk_level"] = "High"

    elif result["risk_score"] >= 30:

        result["risk_level"] = "Medium"

    else:

        result["risk_level"] = "Low"

    return result