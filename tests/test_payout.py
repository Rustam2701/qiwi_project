import pytest
import uuid
from playwright.sync_api import playwright, APIRequestContext
from tests.api.qiwi_api import QiwiPayoutAPI


@pytest.fixture(scope="session")
def api_context():
    with playwright() as p:
        context = p.request.new_context()
        yield context
        context.dispose()


@pytest.fixture
def qiwi_client(api_context: APIRequestContext):
    return QiwiPayoutAPI(api_context)


def test_service_availability(qiwi_client: QiwiPayoutAPI):
    response = qiwi_client.get_all_payments()

    assert response.ok, f"Сервис недоступен. Код ответа: {response.status}"

    data = response.json()
    assert isinstance(data, list), "Критическая ошибка: Формат ответа изменился! Ожидался список []."


def test_get_balance(qiwi_client: QiwiPayoutAPI):
    response = qiwi_client.get_balance()

    assert response.ok, f"Не удалось получить баланс. Код ответа: {response.status}"

    data = response.json()
    balance_value = float(data["available"]["value"])

    assert balance_value > 0, f"Ошибка: Баланс равен {balance_value}, а должен быть строго больше 0!"


def test_payment_lifecycle(qiwi_client: QiwiPayoutAPI):
    unique_payment_id = str(uuid.uuid4())
    target_account = "79123456789"

    create_response = qiwi_client.create_payment(
        payment_id=unique_payment_id,
        account=target_account,
        amount="1.00"
    )
    assert create_response.ok, f"Ошибка создания платежа. Код: {create_response.status}"

    create_data = create_response.json()
    assert create_data["status"]["value"] in ["READY", "ACCEPTED"], \
        f"Неверный статус после создания: {create_data['status']['value']}"

    execute_response = qiwi_client.execute_payment(unique_payment_id)
    assert execute_response.ok, f"Ошибка исполнения платежа. Код: {execute_response.status}"

    execute_data = execute_response.json()
    assert execute_data["status"]["value"] in ["SUCCESS", "PROCESSING"], \
        f"Платеж отклонен или завис. Текущий статус: {execute_data['status']['value']}"
