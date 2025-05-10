import requests

# Function to get public IP
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        ip_info = response.json()
        return ip_info['ip']
    except requests.RequestException as e:
        return f"Error: {e}"

# Function to get ISP details using the public IP
def get_isp_details(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        isp_info = response.json()
        
        if isp_info["status"] == "fail":
            return "Could not retrieve ISP details."
        
        isp_details = {
            "IP": isp_info["query"],
            "ISP": isp_info["isp"],
            "Organization": isp_info["org"],
            "Location": f"{isp_info['city']}, {isp_info['regionName']}, {isp_info['country']}",
            "AS": isp_info["as"]
        }
        
        return isp_details
    except requests.RequestException as e:
        return f"Error: {e}"

# Main function
def main():
    public_ip = get_public_ip()
    print(f"Your Public IP is: {public_ip}")
    
    isp_details = get_isp_details(public_ip)
    
    if isinstance(isp_details, dict):
        print("\nISP Details:")
        for key, value in isp_details.items():
            print(f"{key}: {value}")
    else:
        print(isp_details)

if __name__ == "__main__":
    main()
