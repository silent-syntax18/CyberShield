import socket
import ssl
import ipaddress
import json
from urllib.request import urlopen, Request
from urllib.parse import urlparse


def resolve_domain(domain):
    """Resolve domain to an IP address."""

    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def get_dns_info(domain):
    """Get basic DNS information."""

    dns_info = {
        "hostname": domain,
        "ip_address": [],
        "aliases": []
    }

    try:
        hostname, aliases, addresses = socket.gethostbyname_ex(domain)

        dns_info["hostname"] = hostname
        dns_info["aliases"] = aliases
        dns_info["ip_address"] = addresses

    except Exception:
        pass

    return dns_info


def get_ssl_info(domain):
    """Get basic HTTPS/SSL certificate information."""

    result = {
        "https": False,
        "issuer": "Unavailable",
        "subject": "Unavailable"
    }

    try:

        context = ssl.create_default_context()

        with socket.create_connection(
            (domain, 443),
            timeout=5
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=domain
            ) as secure_sock:

                certificate = secure_sock.getpeercert()

                result["https"] = True

                issuer = certificate.get("issuer", [])
                subject = certificate.get("subject", [])

                result["issuer"] = str(issuer)
                result["subject"] = str(subject)

    except Exception:
        pass

    return result


def get_ip_intelligence(ip):
    """
    Get publicly available IP intelligence.

    Includes approximate geolocation, ISP/organization
    and ASN information.
    """

    result = {
        "isp": "Unavailable",
        "organization": "Unavailable",
        "asn": "Unavailable",
        "country": "Unavailable",
        "region": "Unavailable",
        "city": "Unavailable",
        "latitude": "Unavailable",
        "longitude": "Unavailable",
        "timezone": "Unavailable"
    }

    if not ip:
        return result

    try:

        url = f"https://ipinfo.io/{ip}/json"

        request = Request(
            url,
            headers={
                "User-Agent": "CyberShield/2026"
            }
        )

        with urlopen(request, timeout=8) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        result["organization"] = data.get(
            "org",
            "Unavailable"
        )

        # IPinfo's org field commonly contains:
        # AS number + organization name
        org = data.get("org", "")

        if org.startswith("AS"):

            parts = org.split(" ", 1)

            result["asn"] = parts[0]

            if len(parts) > 1:
                result["isp"] = parts[1]

        else:

            result["isp"] = org or "Unavailable"

        result["country"] = data.get(
            "country",
            "Unavailable"
        )

        result["region"] = data.get(
            "region",
            "Unavailable"
        )

        result["city"] = data.get(
            "city",
            "Unavailable"
        )

        result["timezone"] = data.get(
            "timezone",
            "Unavailable"
        )

        # IPinfo returns coordinates as:
        # "latitude,longitude"

        location = data.get("loc")

        if location:

            coordinates = location.split(",")

            if len(coordinates) == 2:

                result["latitude"] = coordinates[0]
                result["longitude"] = coordinates[1]

    except Exception:

        pass

    return result


def analyze_target(target):
    """
    Analyze a domain or IP address using
    safe, publicly available network information.
    """

    target = target.strip()

    result = {
        "target": target,
        "type": "Unknown",
        "domain": None,
        "ip_address": None,
        "dns": {},
        "ssl": {},
        "intelligence": {},
        "notes": []
    }

    if not target:

        result["notes"].append(
            "No target was provided."
        )

        return result

    # --------------------------------------------------
    # Remove protocol if user enters a URL
    # --------------------------------------------------

    if "://" in target:

        parsed = urlparse(target)

        target = parsed.hostname or target

    # --------------------------------------------------
    # Check whether target is an IP address
    # --------------------------------------------------

    try:

        ipaddress.ip_address(target)

        result["type"] = "IP Address"
        result["ip_address"] = target

        result["intelligence"] = get_ip_intelligence(
            target
        )

        result["notes"].append(
            "Target is a valid IP address."
        )

        return result

    except ValueError:

        pass

    # --------------------------------------------------
    # Treat target as domain
    # --------------------------------------------------

    result["type"] = "Domain"
    result["domain"] = target

    ip = resolve_domain(target)

    if ip:

        result["ip_address"] = ip

        result["notes"].append(
            "Domain successfully resolved to an IP address."
        )

        result["intelligence"] = get_ip_intelligence(
            ip
        )

    else:

        result["notes"].append(
            "Domain could not be resolved."
        )

    # --------------------------------------------------
    # DNS information
    # --------------------------------------------------

    result["dns"] = get_dns_info(target)

    # --------------------------------------------------
    # SSL information
    # --------------------------------------------------

    result["ssl"] = get_ssl_info(target)

    return result