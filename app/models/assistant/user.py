import datetime
from typing import Any, Dict
from enum import Enum
from app.utils.enum import get_enum
from .engagement import Engagement
from .entitlements import PackageEntitlements


class AccountLinkingStatus(Enum):
    ACCOUNT_LINKING_STATUS_UNSPECIFIED = "ACCOUNT_LINKING_STATUS_UNSPECIFIED"
    NOT_LINKED = "NOT_LINKED"
    LINKED = "LINKED"


class UserVerificationStatus(Enum):
    USER_VERIFICATION_STATUS_UNSPECIFIED = "USER_VERIFICATION_STATUS_UNSPECIFIED"
    GUEST = "GUEST"
    VERIFIED = "VERIFIED"


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
        self.last_seen = datetime.datetime.fromisoformat(payload['lastSeenTime'].rstrip('Z'))

        engagement = payload.get('engagement')
        self.engagement = None
        if engagement is not None:
            self.engagement = Engagement(engagement)

        package_entitlements = payload.get('packageEntitlements', [])
        self.package_entitlements = [
            PackageEntitlements(x) for x in package_entitlements
        ]
        self.permission = [get_enum(Permission, x) for x in payload.get('permission', [])]
