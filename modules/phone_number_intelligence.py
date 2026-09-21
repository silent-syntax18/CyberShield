import re


COUNTRY_DATA = {
    "+92": {
        "country": "Pakistan",
        "region": "Pakistan",
        "type": "Mobile"
    },
    "+91": {
        "country": "India",
        "region": "India",
        "type": "Phone"
    },
    "+44": {
        "country": "United Kingdom",
        "region": "United Kingdom",
        "type": "Phone"
    },
    "+971": {
        "country": "United Arab Emirates",
        "region": "UAE",
        "type": "Phone"
    },
    "+1": {
        "country": "United States / Canada",
        "region": "North America",
        "type": "Phone"
    },
    "+61": {
        "country": "Australia",
        "region": "Australia",
        "type": "Phone"
    },
    "+49": {
        "country": "Germany",
        "region": "Germany",
        "type": "Phone"
    },
    "+33": {
        "country": "France",
        "region": "France",
        "type": "Phone"
    }
}


def analyze_phone_number(phone_number):

    phone = phone_number.strip()

    cleaned = re.sub(
        r"[\s\-\(\)]",
        "",
        phone
    )

    result = {
        "phone_number": phone,
        "valid_format": False,
        "country_code": "Unknown",
        "country": "Unknown",
        "region": "Unknown",
        "number_type": "Unknown",
        "risk_level": "Low",
        "risk_score": 0,
        "indicators": []
    }

    # --------------------------------------------------------
    # FORMAT VALIDATION
    # --------------------------------------------------------

    if not re.match(
        r"^\+\d{8,15}$",
        cleaned
    ):

        result["risk_level"] = "Medium"
        result["risk_score"] = 40

        result["indicators"].append(
            "Invalid or incomplete international phone number format."
        )

        return result

    result["valid_format"] = True

    # --------------------------------------------------------
    # COUNTRY DETECTION
    # --------------------------------------------------------

    matched_code = None

    for code in sorted(
        COUNTRY_DATA.keys(),
        key=len,
        reverse=True
    ):

        if cleaned.startswith(code):

            matched_code = code
            break

    if matched_code:

        data = COUNTRY_DATA[matched_code]

        result["country_code"] = matched_code
        result["country"] = data["country"]
        result["region"] = data["region"]
        result["number_type"] = data["type"]

    else:

        result["country_code"] = "Unknown"
        result["country"] = "Unknown"
        result["region"] = "Unknown"
        result["number_type"] = "Phone"

        result["indicators"].append(
            "Country code is not available in the local database."
        )

    # --------------------------------------------------------
    # BASIC RISK CHECKS
    # --------------------------------------------------------

    digits = re.sub(
        r"\D",
        "",
        cleaned
    )

    if len(digits) < 10:

        result["risk_score"] += 20

        result["indicators"].append(
            "Number appears unusually short."
        )

    # Repeated digits
    if len(set(digits)) <= 2:

        result["risk_score"] += 20

        result["indicators"].append(
            "Number contains an unusual repeated-digit pattern."
        )

    # Normalize score
    result["risk_score"] = min(
        result["risk_score"],
        100
    )

    # Risk level
    if result["risk_score"] >= 60:

        result["risk_level"] = "High"

    elif result["risk_score"] >= 30:

        result["risk_level"] = "Medium"

    else:

        result["risk_level"] = "Low"

    return result