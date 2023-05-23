import pytest
from datetime import datetime
from typing import Generator

from playwright.sync_api import Playwright, APIRequestContext, expect

cookie = "A"

def isValidDate(date):
    res = True
    try:
        res = bool(datetime.strptime(date, "%Y-%m-%d"))
        
    except ValueError:
        res = False

    return res
    

@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    
    data = {
        "username": "admin",
        "password": "password",
    }
   
    
    request_context = playwright.request.new_context(
        base_url="https://automationintesting.online",  
    )
    response = request_context.post("auth/login", data = data)
    assert response.status == 200
    global cookie
    cookie = response.headers['set-cookie']
    cookie = cookie.split(";")[0].split("=")[1]
    yield request_context
    request_context.dispose()

#Get bookign summary with a specific ID
def test_get_booking_summary(api_request_context: APIRequestContext)-> None:

    response = api_request_context.get("/booking/summary?roomid=1")

    assert response.status == 200

    body = response.json()

    assert len(body['bookings']) >= 1
    assert isValidDate(body['bookings'][0]['bookingDates']['checkin']) 
    assert isValidDate(body['bookings'][0]['bookingDates']['checkout']) 

def test_get_all_bookings_details(api_request_context: APIRequestContext) -> None:

    
    headers = {
        "cookie": "token="+cookie
    }
    response = api_request_context.get("/booking/", headers=headers)

    assert response.status == 200

    body = response.json()
    
    assert len(body['bookings']) >= 1
    assert body['bookings'][0]['bookingid'] == 1
    assert body['bookings'][0]['roomid'] == 1
    assert body['bookings'][0]['firstname'] == "James"
    assert body['bookings'][0]['lastname'] == "Dean"
    assert body['bookings'][0]['depositpaid']    
    assert isValidDate(body['bookings'][0]['bookingdates']['checkin']) 
    assert isValidDate(body['bookings'][0]['bookingdates']['checkout']) 


def test_get_booking_by_id_with_details(api_request_context: APIRequestContext) -> None:

    
    headers = {
        "cookie": "token="+cookie
    }
    response = api_request_context.get("/booking/1", headers=headers)

    assert response.status == 200

    body = response.json()
    
    
    assert body['bookingid'] == 1
    assert body['roomid'] == 1
    assert body['firstname'] == "James"
    assert body['lastname'] == "Dean"
    assert body['depositpaid']    
    assert isValidDate(body['bookingdates']['checkin']) 
    assert isValidDate(body['bookingdates']['checkout']) 
