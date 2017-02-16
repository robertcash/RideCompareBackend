import requests
import sys
from helpers import response

LYFT_KEY = 'gAAAAABYokyuGHWk_AwoIHEWyUzD3yOALEEc42SOHcOJxJMXLwEDBAZjKerONfOJ6-tUwCrlTF2cCouY-4C3u3BL_SVCh1IR4SeNOoOkFYIIvmF0_eTtIxkQBrKtRnhMQMG474Lk_OBVHYjfWovOYxiRzU9CjfIqVzB8DawVeyReKv40AzwtVl8='
LYFT_URL = 'https://api.lyft.com/v1/cost'
UBER_KEY = 'FT-zL9tcvqiSWPqonMx2wLBfs_guAd3gC1H4szCi'
UBER_URL = 'https://api.uber.com/v1.2/estimates/price'

'''

    Compare Route Functions

'''

def compare(request):
    # Grab locational data from POST request
    start_lat = request['start_lat']
    start_lng = request['start_lng']
    end_lat = request['end_lat']
    end_lng = request['end_lng']

    # Create params for API requests to Lyft and Uber
    lyft_params = {
        'start_lat':start_lat,
        'start_lng':start_lng,
        'end_lat':end_lat,
        'end_lng':end_lng
    }
    lyft_headers = {
        'Authorization':'bearer ' + LYFT_KEY
    }
    uber_params = {
        'start_latitude':start_lat,
        'start_longitude':start_lng,
        'end_latitude':end_lat,
        'end_longitude':end_longitude
    }
    uber_headers = {
        'Authorization':'Token ' + UBER_KEY
    }

    # Do API Requests to Lyft and Uber
    lyft_request = requests.get(LYFT_URL, params=lyft_params, headers=lyft_headers)
    uber_request = requests.get(UBER_URL, params=uber_params, headers=uber_headers)

    # Check if both requests were succesful
    if lyft_request.status_code != 200 or uber_request.status_code != 200:
        return response({'success':False})

    # Get estimates from both requests
    lyft_cost_estimates = lyft_request.json()['cost_estimates']
    uber_cost_estimates = uber_request.json()['prices']

    # Check to see what is cheaper and send it back to the user
    lyft_low = sys.maxint
    uber_low = sys.maxint

    for estimate in lyft_cost_estimates:
        cost = (estimate['estimated_cost_cents_min']/100)
        lyft_low = min(lyft_low, int(cost))

    for estimate in uber_cost_estimates:
        cost = estimate['low_estimate']
        uber_low = min(uber_low, cost)

    if lyft_low > uber_low:
        # Uber is cheaper
        return response({'success':True, 'winner':'uber'})

    return response({'success':True, 'winner':'lyft'})
