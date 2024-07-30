import requests
import time
import concurrent.futures
 
found_subdomains = []
https_subdomains = []
 
def check_https(subdomain):
    try:
        response = requests.get(f"https://{subdomain}", timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False
 
def add_subdomain(subdomain, supports_https):
    found_subdomains.append((subdomain, supports_https))
    if supports_https:
        https_subdomains.append(subdomain)
 
def print_summary():
    print("Subdomain Scan Summary")
    print(f"Total subdomains found: {len(found_subdomains)}")
    print(f"Subdomains supporting HTTPS: {len(https_subdomains)}\n")
    print("List of found subdomains:")
    for sub, supports_https in found_subdomains:
        https_status = "supports HTTPS" if supports_https else "does not support HTTPS"
        print(f"{sub} {https_status}")

def enumerate_subdomains(domain, subdomain_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subdomain = {executor.submit(check_https, f"{sub.strip()}.{domain}"): sub.strip() for sub in subdomain_list}
        for future in concurrent.futures.as_completed(future_to_subdomain):
            sub = future_to_subdomain[future]
            subdomain = f"{sub}.{domain}"
            try:
                supports_https = future.result()
            except Exception as exc:
                supports_https = False
                print(f"{subdomain} generated an exception: {exc}")
            add_subdomain(subdomain, supports_https)
 
    print_summary()
 
# Main function to get user input and read subdomains from a file
def main():
    domain = input("Enter the domain name: ")
    subdomain_file = input("Enter the path to the subdomains file: ")
 
    try:
        with open(subdomain_file, 'r') as file:
            subdomain_list = file.readlines()
        enumerate_subdomains(domain, subdomain_list)
    except FileNotFoundError:
        print(f"Error: The file '{subdomain_file}' was not found.")
 
# Run the main function
if __name__ == "__main__":
    main()
