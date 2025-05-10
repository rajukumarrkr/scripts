import requests

# Function to get ISP details for a single IP address
def get_isp_details(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        isp_info = response.json()

        if isp_info["status"] == "fail":
            return {"IP": ip, "ISP": "Could not retrieve ISP details"}
        
        isp_details = {
            "IP": isp_info["query"],
            "ISP": isp_info["isp"],
            "Organization": isp_info["org"],
            "Location": f"{isp_info['city']}, {isp_info['regionName']}, {isp_info['country']}",
            "AS": isp_info["as"]
        }
        return isp_details
    except requests.RequestException as e:
        return {"IP": ip, "Error": f"Request failed: {e}"}

# Function to process multiple IP addresses from a file
def get_isp_details_from_file(file_path):
    isp_results = []
    try:
        with open(file_path, 'r') as file:
            ip_list = file.readlines()
        
        # Clean the IPs from extra spaces and newline characters
        ip_list = [ip.strip() for ip in ip_list]

        for ip in ip_list:
            isp_results.append(get_isp_details(ip))
        return isp_results
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"Error: {e}"

# Function to get ISP details for a single IP
def get_isp_details_for_single_ip(ip):
    return get_isp_details(ip)

# Main function
def main():
    # Ask the user if they want to search using a file or single IP
    choice = input("Do you want to input a file of IPs or a single IP? (file/single): ").strip().lower()

    if choice == 'file':
        file_path = input("Enter the path of the file containing IP addresses: ").strip()
        isp_info_list = get_isp_details_from_file(file_path)
        if isinstance(isp_info_list, list):
            for isp_info in isp_info_list:
                print(f"\nISP Details for IP {isp_info['IP']}:")
                for key, value in isp_info.items():
                    print(f"{key}: {value}")
        else:
            print(isp_info_list)  # In case of an error with the file
    elif choice == 'single':
        ip = input("Enter the IP address to check: ").strip()
        isp_info = get_isp_details_for_single_ip(ip)
        print(f"\nISP Details for IP {isp_info['IP']}:")
        for key, value in isp_info.items():
            print(f"{key}: {value}")
    else:
        print("Invalid choice! Please enter 'file' or 'single'.")

if __name__ == "__main__":
    main()
