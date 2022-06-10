from typing import Any, Dict


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