import logging
from typing import Dict, Any, Optional
import requests

logging.basicConfig(level=logging.INFO)

TARGET_SERVICES = [
    {
        "service_id": "github",
        "service_name": "GitHub REST API",
        "spec_url": "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json",
        "sdk_ecosystem": "pypi",
        "sdk_package": "PyGithub"
    },
    {
        "service_id": "openai",
        "service_name": "OpenAI API",
        "spec_url": "https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml",
        "sdk_ecosystem": "pypi",
        "sdk_package": "openai"
    },
    {
        "service_id": "stripe",
        "service_name": "Stripe API",
        "spec_url": "https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json",
        "sdk_ecosystem": "pypi",
        "sdk_package": "stripe"
    },
    {
        "service_id": "resend",
        "service_name": "Resend Email API",
        "spec_url": "https://raw.githubusercontent.com/resend/resend-openapi/main/openapi.json",
        "sdk_ecosystem": "pypi",
        "sdk_package": "resend"
    },
    {
        "service_id": "posthog",
        "service_name": "PostHog API",
        "spec_url": "https://raw.githubusercontent.com/PostHog/posthog/master/posthog/api/openapi.json",
        "sdk_ecosystem": "pypi",
        "sdk_package": "posthog"
    }
]

def fetch_openapi_spec(url: str) -> Optional[Dict[str, Any]]:
    headers = {"User-Agent": "API-Drift-Preemption-Wire/1.0"}
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            if url.endswith(".yaml") or url.endswith(".yml"):
                # Basic JSON fallback if YAML parser not installed
                try:
                    import yaml
                    return yaml.safe_load(res.text)
                except ImportError:
                    pass
            return res.json()
    except Exception as e:
        logging.warning(f"Failed to fetch spec from {url}: {e}")
    return None
