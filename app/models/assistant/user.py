import datetime
from typing import Any, Dict
from enum import Enum
from app.utils import get_enum
from .slot import SlotStatus, Slot, SlotMode, SlotFillingStatus


class AccountLinkingStatus(Enum):
    ACCOUNT_LINKING_STATUS_UNSPECIFIED = "ACCOUNT_LINKING_STATUS_UNSPECIFIED"
    NOT_LINKED = "NOT_LINKED"
    LINKED = "LINKED"


class UserVerificationStatus(Enum):
    USER_VERIFICATION_STATUS_UNSPECIFIED = "USER_VERIFICATION_STATUS_UNSPECIFIED"
    GUEST = "GUEST"
    VERIFIED = "VERIFIED"


class IntentSubscription:
    def __init__(self, payload: Dict[str, Any]):
        self.intent = payload.get('intent')
        self.content = payload.get('contentTitle')


class Engagement:
    def __init__(self, payload: Dict[str, Any]):
        self.push_notification = [
            IntentSubscription(x) for x in payload.get('pushNotificationIntents', [])
        ]
        self.daily_update = [
            IntentSubscription(x) for x in payload.get('dailyUpdateIntents', [])
        ]


class SkuType(Enum):
    SKU_TYPE_UNSPECIFIED = "SKU_TYPE_UNSPECIFIED"
    IN_APP = "IN_APP"
    SUBSCRIPTION = "SUBSCRIPTION"
    APP = "APP"


class Entitlement:
    def __init__(self, payload: Dict[str, Any]):
        self.sku = payload.get('sku')
        self.type = payload.get('skuType')


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


class Permission:
    PERMISSION_UNSPECIFIED = "PERMISSION_UNSPECIFIED"
    DEVICE_PRECISE_LOCATION = "DEVICE_PRECISE_LOCATION"
    DEVICE_COARSE_LOCATION = "DEVICE_COARSE_LOCATION"
    UPDATE = "UPDATE"


class User:
    def __init__(self, payload: Dict[str, Any]):
        self.locale = payload['locale']
        self.params: Dict[str, Any] = payload.get('params', {})

        self.account_linking = get_enum(AccountLinkingStatus, payload['accountLinkingStatus'])
        self.verification = get_enum(UserVerificationStatus, payload['verificationStatus'])
        self.last_seen = datetime.datetime.fromtimestamp(payload['lastSeenTime'])

        engagement = payload.get('engagement')
        self.engagement = None
        if engagement is not None:
            self.engagement = Engagement(engagement)

        package_entitlements = payload.get('packageEntitlements', [])
        self.package_entitlements = [
            PackageEntitlements(x) for x in package_entitlements
        ]
        self.permission = [get_enum(Permission, x) for x in payload.get('permission', [])]
