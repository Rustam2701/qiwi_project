from playwright.sync_api import APIRequestContext
from config import Config


class QiwiPayoutAPI:
    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        self.headers = {
            "Authorization": f"Bearer {Config.TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.base_path = f"{Config.BASE_URL}/v1/agents/{Config.AGENT_ID}/points/{Config.POINT_ID}"

    def get_all_payments(self):
        return self.request.get(f"{self.base_path}/payments", headers=self.headers)

    def get_balance(self):
        return self.request.get(f"{self.base_path}/balance", headers=self.headers)

    def create_payment(self, payment_id: str, account: str, amount: str = "1.00"):
        payload = {
            "recipientDetails": {
                "providerCode": "qiwi-wallet",
                "fields": {"account": account}
            },
            "amount": {"value": amount, "currency": "RUB"}
        }
        return self.request.put(f"{self.base_path}/payments/{payment_id}", headers=self.headers, data=payload)

    def execute_payment(self, payment_id: str):
        payload = {"action": "EXECUTE"}
        return self.request.post(f"{self.base_path}/payments/{payment_id}/status", headers=self.headers, data=payload)
