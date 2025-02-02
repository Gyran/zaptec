"""Zaptec integration constants."""
from __future__ import annotations

NAME = "zaptec-dev"
VERSION = "0.0.6b231001"
ISSUEURL = "https://github.com/sveinse/zaptec/issues"

DOMAIN = "zaptec"
MANUFACTURER = "Zaptec"

STARTUP = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""

CHARGE_MODE_MAP = {
    "Unknown": ["Unknown", "mdi:help-rhombus-outline"],
    "Disconnected": ["Disconnected", "mdi:power-plug-off"],
    "Connected_Requesting": ["Waiting", "mdi:timer-sand"],
    "Connected_Charging": ["Charging", "mdi:lightning-bolt"],
    "Connected_Finished": ["Charge done", "mdi:battery-charging-100"],
}

TOKEN_URL = "https://api.zaptec.com/oauth/token"
API_URL = "https://api.zaptec.com/api/"
CONST_URL = "https://api.zaptec.com/api/constants"

API_RETRIES = 5

DEFAULT_SCAN_INTERVAL = 60

API_TIMEOUT = 60

REQUEST_REFRESH_DELAY = 0.3

CONF_MANUAL_SELECT = "manual_select"
CONF_CHARGERS = "chargers"


class Missing:
    """Singleton class representing a missing value."""


MISSING = Missing()

TRUTHY = ["true", "1", "on", "yes", 1, True]
FALSY = ["false", "0", "off", "no", 0, False]
