import allure
from pydantic import ValidationError
from core.models.booking import BookingResponse
import requests
import pytest
import random
from datetime import datetime, timedelta


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
        checkin_date = datetime.now() + timedelta(days=random.randint(1, 30))
        checkout_date = checkin_date + timedelta(days=random.randint(1, 30))

        booking_data = {
            "firstname": "Anton",
            "lastname": "Pavlovich",
            "totalprice": 166,
            "depositpaid": True,
            "bookingdates": booking_dates,
            "additionalneeds": "Dinner"
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
@allure.story('Positive: String totalprice converted to None')
def test_create_booking_string_totalprice_converted_to_none(api_client):

    booking_data = {
        "firstname": "Anton",
        "lastname": "Pavlovich",
        "totalprice": "invalid",
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-06",
            "checkout": "2025-06-16"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking method with string totalprice"):
        response = api_client.create_booking(booking_data)

        assert response["booking"]["totalprice"] is None, "totalprice should be None"


@allure.feature('Test creating booking')
@allure.story('Negative: Invalid bookingdates format')
def test_create_booking_invalid_bookingdates_format(api_client):

    booking_data = {
        "firstname": "Anton",
        "lastname": "Pavlovich",
        "totalprice": 166,
        "depositpaid": True,
        "bookingdates": "Invalid date format",
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking method with invalid bookingdates format"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: Missing checkin date in bookingdates')
def test_create_booking_missing_checkin_date(api_client):

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
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: Missing bookingdates field')
def test_create_booking_missing_bookingdates(api_client):

    booking_data = {
        "firstname": "Anton",
        "lastname": "Pavlovich",
        "totalprice": 166,
        "depositpaid": True,
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking method with missing bookingdates field"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: Empty request data')
def test_create_booking_empty_data_returns_error(api_client):

    booking_data = {}

    with allure.step("Calling create_booking method with empty data"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: Invalid firstname type (integer)')
def test_create_booking_invalid_firstname_type(api_client):
    booking_data = {
        "firstname": 123,
        "lastname": "Pavlovich",
        "totalprice": 166,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-06",
            "checkout": "2025-06-16"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking with invalid firstname type"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: Invalid firstname type (integer)')
def test_create_booking_invalid_firstname_type(api_client):
    booking_data = {
        "firstname": 123,
        "lastname": "Pavlovich",
        "totalprice": 166,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-06",
            "checkout": "2025-06-16"
        },
        "additionalneeds": "Dinner"
    }

    with allure.step("Calling create_booking with invalid firstname type"):
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            api_client.create_booking(booking_data)














