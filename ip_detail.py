import tkinter as tk
from tkinter import filedialog, messagebox
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
        
        ip_list = [ip.strip() for ip in ip_list]

        for ip in ip_list:
            isp_results.append(get_isp_details(ip))
        return isp_results
    except FileNotFoundError:
        return "Error: The file was not found."
    except Exception as e:
        return f"Error: {e}"

# Function to display ISP details in the result box
def display_results(results):
    result_text.delete(1.0, tk.END)
    if isinstance(results, list):
        for result in results:
            for key, value in result.items():
                result_text.insert(tk.END, f"{key}: {value}\n")
            result_text.insert(tk.END, "\n" + "-"*30 + "\n")
    else:
        result_text.insert(tk.END, results)

# Function to handle single IP search
def search_single_ip():
    ip = ip_entry.get()
    if ip:
        isp_info = get_isp_details(ip)
        display_results([isp_info])
    else:
        messagebox.showerror("Input Error", "Please enter an IP address.")

# Function to handle file input
def search_from_file():
    file_path = filedialog.askopenfilename(title="Select IP file", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if file_path:
        results = get_isp_details_from_file(file_path)
        display_results(results)
    else:
        messagebox.showerror("File Error", "No file selected.")

# Creating the main application window
root = tk.Tk()
root.title("ISP Details Finder")
root.geometry("600x400")

# Single IP search
ip_label = tk.Label(root, text="Enter IP Address:")
ip_label.pack(pady=5)
ip_entry = tk.Entry(root, width=50)
ip_entry.pack(pady=5)
ip_button = tk.Button(root, text="Search Single IP", command=search_single_ip)
ip_button.pack(pady=10)

# File input search
file_button = tk.Button(root, text="Search from File", command=search_from_file)
file_button.pack(pady=10)

# Result display box
result_text = tk.Text(root, height=15, width=70)
result_text.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
