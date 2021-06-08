"""Get Current Public IP Address
"""

import requests


def public_ip_address():
    """Get Current Public IP Address
    """
    return requests.get("https://ipinfo.io/ip").text.rstrip()
