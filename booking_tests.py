import pytest
from datetime import datetime
from typing import Generator

from playwright.sync_api import Playwright, APIRequestContext, expect

def isValidDate(date):
    res = True
    try:
        res = bool(datetime.strptime(date, "%Y-%m-%Y"))
        
    except ValueError:
        res = False

    return res
    

@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    
    request_context = playwright.request.new_context(
        base_url="https://automationintesting.online"
    )
    yield request_context
    request_context.dispose()

#Get bookign summary with a specific ID
def test_get_booking_summary(api_request_context: APIRequestContext)-> None:

    response = api_request_context.get("/booking/summary?roomid=1")

    assert response.status == 200

    body = response.json()
    assert len(body['bookings']) >= 1
    #print(body['bookings'][0]['bookingDates']['checkin'])
    assert isValidDate(body['bookings'][0]['bookingDates']['checkin']) 
    assert isValidDate(body['bookings'][0]['bookingDates']['checkout']) 

    print(body)
