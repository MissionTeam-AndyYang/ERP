"""Bounded FM-02 C2 validation and service-layer contract."""

from .service import (
    CUSTOMER_SCOPE_SENTINEL,
    C2Service,
    build_app,
    normalize_customer_qualification,
    resolve_item_specific_conversion,
    validate_approval_evidence,
    validate_conversion_rule,
)

__all__ = [
    "CUSTOMER_SCOPE_SENTINEL",
    "C2Service",
    "build_app",
    "normalize_customer_qualification",
    "resolve_item_specific_conversion",
    "validate_approval_evidence",
    "validate_conversion_rule",
]
