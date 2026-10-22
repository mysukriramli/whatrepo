from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Directive(str, Enum):
    GENERATE_COMPATIBILITY_SHIM = "GENERATE_COMPATIBILITY_SHIM"
    PIN_SDK = "PIN_SDK"
    REGENERATE_CLIENT = "REGENERATE_CLIENT"
    ADD_CONTRACT_TEST = "ADD_CONTRACT_TEST"
    SAFE_TO_UPGRADE = "SAFE_TO_UPGRADE"

class ReasonCode(str, Enum):
    ENDPOINT_REMOVED = "ENDPOINT_REMOVED"
    NEW_REQUIRED_PARAMETER = "NEW_REQUIRED_PARAMETER"
    HTTP_METHOD_REMOVED = "HTTP_METHOD_REMOVED"
    RESPONSE_SCHEMA_MUTATION = "RESPONSE_SCHEMA_MUTATION"
    SDK_LAG_BEHIND_SPEC = "SDK_LAG_BEHIND_SPEC"
    SPEC_EXPANDED_COMPATIBLE = "SPEC_EXPANDED_COMPATIBLE"
    BASELINE_INITIALIZED = "BASELINE_INITIALIZED"

class BreakingChange(BaseModel):
    change_type: str
    path: str
    method: Optional[str] = None
    detail: str
    severity: float = Field(ge=0.0, le=10.0)

class ServiceDriftRecord(BaseModel):
    service_id: str
    service_name: str
    spec_url: str
    spec_hash_sha256: str
    total_endpoints: int
    breaking_changes: List[BreakingChange]
    sdk_ecosystem: str
    sdk_package: str
    sdk_latest_version: str
    sdk_release_age_days: float
    drift_score: float = Field(ge=0.0, le=100.0)
    directive: Directive
    confidence: float = Field(ge=0.0, le=1.0)
    reason_codes: List[ReasonCode]
