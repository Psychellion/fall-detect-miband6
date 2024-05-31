import requests

# Define the URL of the Gadgetbridge API endpoint
api_url = "http://your-gadgetbridge-api-url.com/"

def send_request(endpoint, params=None):
    """
    Send a request to the Gadgetbridge API endpoint.
    
    Args:
        endpoint (str): The API endpoint to send the request to.
        params (dict, optional): Parameters to include in the request.
    
    Returns:
        dict: Response from the API.
    """
    # Construct the full URL
    url = api_url + endpoint
    
    # Send the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Request failed with status code", response.status_code)
        return None

# Example usage
if __name__ == "__main__":
    # Example endpoint and parameters
    endpoint = "your-endpoint"
    params = {
        "param1": "value1",
        "param2": "value2"
    }
    
    # Send the request
    response = send_request(endpoint, params)
    
    # Print the response
    if response:
        print("Response:", response)
