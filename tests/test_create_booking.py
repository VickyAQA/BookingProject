import allure
from pydantic import ValidationError
from core.models.booking import BookingResponse
import requests
import pytest

@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
    "firstname" : "Anton",
    "lastname" : "Pavlovich",
    "totalprice" : 166,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2025-06-06",
        "checkout" : "2025-06-16"
    },
    "additionalneeds" : "Dinner"
}
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response["booking"]["firstname"] == booking_data["firstname"], "firstname is incorrect"
    assert response["booking"]["lastname"] == booking_data["lastname"], "lastname is incorrect"
    assert response["booking"]["totalprice"] == booking_data["totalprice"], "totalprice is incorrect"
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"], "depositpaid is incorrect"
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"], "checkin is incorrect"
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"], "checkout is incorrect"
    assert response["booking"]["additionalneeds"] == booking_data["additionalneeds"], "additionalneeds is incorrect"


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_with_random_data(api_client, booking_dates):
    booking_data = {
    "firstname" : "Anton",
    "lastname" : "Pavlovich",
    "totalprice" : 166,
    "depositpaid" : True,
    "bookingdates" : booking_dates,
    "additionalneeds" : "Dinner"
}
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise   ValidationError(f"Response validation failed: {e}")

    assert response["booking"]["firstname"] == booking_data["firstname"], "firstname is incorrect"
    assert response["booking"]["lastname"] == booking_data["lastname"], "lastname is incorrect"
    assert response["booking"]["totalprice"] == booking_data["totalprice"], "totalprice is incorrect"
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"], "depositpaid is incorrect"
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"], "checkin is incorrect"
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"], "checkout is incorrect"
    assert response["booking"]["additionalneeds"] == booking_data["additionalneeds"], "additionalneeds is incorrect"


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking without firstname')
def test_create_booking_without_firstname(api_client):
    booking_data = {
        "lastname": "Pavlovich",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-06",
            "checkout": "2025-06-16"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking method without firstname"):
        try:
            response = api_client.create_booking(booking_data)
            pytest.fail("Test failed: Expected an HTTPError, but the request was successful")

        except requests.exceptions.HTTPError as e:
            print(f"Got an HTTPError with status code: {e.response.status_code}")
            return

        except Exception as e:
            allure.attach(str(e), name="Unexpected Error", attachment_type=allure.attachment_type.TEXT)
            raise


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with no request body')
def test_create_booking_with_no_request_body(api_client):
    with allure.step("Calling create_booking method with no data"):
        try:
            response = api_client.create_booking(None)
            pytest.fail("Test failed: Expected an HTTPError, but the request was successful")
        except requests.exceptions.HTTPError as e:
            print(f"Got an HTTPError with status code: {e.response.status_code}")
            return
        except Exception as e:
            allure.attach(str(e), name="Unexpected Error", attachment_type=allure.attachment_type.TEXT)
            raise


@allure.feature('Test creating booking')
@allure.story('Negative: Invalid booking_dates structure (missing checkin)')
def test_create_booking_invalid_booking_dates_missing_checkin(api_client):
    booking_data = {
        "firstname": "Anton",
        "lastname": "Pavlovich",
        "totalprice": 166,
        "depositpaid": True,
        "bookingdates": {
            "checkout": "2025-06-16"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking method with missing checkin date"):
        try:
            response = api_client.create_booking(booking_data)
            pytest.fail("Test failed: Expected an HTTPError, but the request was successful")

        except requests.exceptions.HTTPError as e:
            print(f"Got an HTTPError with status code: {e.response.status_code}")
            return

        except Exception as e:
            allure.attach(str(e), name="Unexpected Error", attachment_type=allure.attachment_type.TEXT)
            raise



@allure.feature('Test creating booking')
@allure.story('Positive: depositpaid integer converted to boolean')
def test_create_booking_deposit_paid_integer_converted(api_client):

    booking_data = {
        "firstname": "Anton",
        "lastname": "Pavlovich",
        "totalprice": 166,
        "depositpaid": 1,
        "bookingdates": {
            "checkin": "2025-06-06",
            "checkout": "2025-06-16"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking method with integer depositpaid"):
        response = api_client.create_booking(booking_data)

        assert response["booking"]["depositpaid"] is True, "depositpaid should be True"








