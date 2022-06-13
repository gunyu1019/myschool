from enum import Enum
from typing import Any, Dict
from app.utils.enum import get_enum


class SkuType(Enum):
    SKU_TYPE_UNSPECIFIED = "SKU_TYPE_UNSPECIFIED"
    IN_APP = "IN_APP"
    SUBSCRIPTION = "SUBSCRIPTION"
    APP = "APP"


class Entitlement:
    def __init__(self, payload: Dict[str, Any]):
        self.sku = payload.get('sku')
        self.type = get_enum(SkuType, payload.get('skuType'))


class SignedData:
    def __init__(self, payload: Dict[str, Any]):
        self.data = payload.get('inAppPurchaseData')
        self.signature = payload.get('inAppDataSignature')


class PackageEntitlements:
    def __init__(self, payload: Dict[str, Any]):
        self.name = payload.get('packageName')
        self.entitlements = [
            Entitlement(x) for x in payload.get('entitlements', [])
        ]

        details = payload.get('inAppDetails')
        self.details = None
        if details is not None:
            self.details = SignedData(details)
