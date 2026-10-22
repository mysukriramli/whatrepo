import hashlib
import json
from typing import Dict, Any, List, Tuple
from core.taxonomy import BreakingChange

class OpenAPIDiffEngine:
    @staticmethod
    def compute_spec_hash(spec: Dict[str, Any]) -> str:
        canonical_str = json.dumps(spec, sort_keys=True)
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    @staticmethod
    def extract_endpoints(spec: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        paths = spec.get("paths", {})
        endpoints = {}
        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method.lower() in ["get", "post", "put", "patch", "delete", "options", "head"]:
                    key = f"{method.upper()} {path}"
                    endpoints[key] = {
                        "path": path,
                        "method": method.upper(),
                        "parameters": operation.get("parameters", []) if isinstance(operation, dict) else [],
                        "request_body": operation.get("requestBody", {}) if isinstance(operation, dict) else {},
                        "responses": operation.get("responses", {}) if isinstance(operation, dict) else {}
                    }
        return endpoints

    def diff_specs(
        self,
        old_spec: Dict[str, Any],
        new_spec: Dict[str, Any]
    ) -> Tuple[List[BreakingChange], float]:
        breaking_changes: List[BreakingChange] = []
        severity_accum = 0.0

        old_endpoints = self.extract_endpoints(old_spec)
        new_endpoints = self.extract_endpoints(new_spec)

        # 1. Detect removed endpoints or HTTP methods
        for key, old_ep in old_endpoints.items():
            if key not in new_endpoints:
                change = BreakingChange(
                    change_type="ENDPOINT_OR_METHOD_REMOVED",
                    path=old_ep["path"],
                    method=old_ep["method"],
                    detail=f"Operation {key} was removed from the active OpenAPI specification.",
                    severity=9.0
                )
                breaking_changes.append(change)
                severity_accum += 9.0

        # 2. Detect newly introduced required parameters on existing operations
        for key, new_ep in new_endpoints.items():
            if key in old_endpoints:
                old_ep = old_endpoints[key]
                old_params = {p.get("name"): p for p in old_ep.get("parameters", []) if isinstance(p, dict)}
                new_params = {p.get("name"): p for p in new_ep.get("parameters", []) if isinstance(p, dict)}

                for param_name, param_obj in new_params.items():
                    is_required = param_obj.get("required", False)
                    if is_required and param_name not in old_params:
                        change = BreakingChange(
                            change_type="NEW_REQUIRED_PARAMETER",
                            path=new_ep["path"],
                            method=new_ep["method"],
                            detail=f"New required parameter '{param_name}' was added to existing endpoint.",
                            severity=7.5
                        )
                        breaking_changes.append(change)
                        severity_accum += 7.5

        raw_score = min(100.0, severity_accum)
        return breaking_changes, round(raw_score, 2)
