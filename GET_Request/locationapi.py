import requests


def get_location_info(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        ip = data.get("ip", "N/A")
        city = data.get("city", "N/A")
        region = data.get("region", "N/A")
        country = data.get("country", "N/A")
        location = f"IP: {ip}, City: {city}, Region: {region}, Country: {country}"
        return location
    else:
        return "Unable to retrieve location information."


# Replace with the IP address you want to look up
ip_address = "116.75.251.6"
location_info = get_location_info(ip_address)
print(location_info)
