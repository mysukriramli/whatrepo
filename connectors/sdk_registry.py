import logging
from datetime import datetime, timezone
from typing import Tuple
import requests

logging.basicConfig(level=logging.INFO)

def get_sdk_metadata(ecosystem: str, package_name: str) -> Tuple[str, float]:
    """
    Fetches the latest package version and the elapsed days since that version was released.
    Returns: (latest_version, release_age_days)
    """
    headers = {"User-Agent": "API-Drift-Preemption-Wire/1.0"}
    now = datetime.now(timezone.utc)

    if ecosystem.lower() == "pypi":
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                latest_ver = data.get("info", {}).get("version", "0.0.0")
                releases = data.get("releases", {}).get(latest_ver, [])
                if releases:
                    upload_time_str = releases[0].get("upload_time_iso_8601")
                    if upload_time_str:
                        dt = datetime.fromisoformat(upload_time_str.replace("Z", "+00:00"))
                        age_days = max(0.0, (now - dt).total_seconds() / 86400.0)
                        return latest_ver, round(age_days, 1)
                return latest_ver, 1.0
        except Exception as e:
            logging.warning(f"PyPI check failed for {package_name}: {e}")

    elif ecosystem.lower() == "npm":
        url = f"https://registry.npmjs.org/{package_name}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                latest_ver = data.get("dist-tags", {}).get("latest", "0.0.0")
                time_entry = data.get("time", {}).get(latest_ver)
                if time_entry:
                    dt = datetime.fromisoformat(time_entry.replace("Z", "+00:00"))
                    age_days = max(0.0, (now - dt).total_seconds() / 86400.0)
                    return latest_ver, round(age_days, 1)
                return latest_ver, 1.0
        except Exception as e:
            logging.warning(f"npm check failed for {package_name}: {e}")

    return "0.0.0", 30.0
