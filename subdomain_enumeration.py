import requests
 
def check_subdomain(subdomain, domain):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Found: {url}")
    except requests.ConnectionError:
        pass
 
def enumerate_subdomains(domain, wordlist_file):
    with open(wordlist_file, 'r') as file:
        subdomains = file.readlines()
 
    for subdomain in subdomains:
        subdomain = subdomain.strip()
        check_subdomain(subdomain, domain)
 
if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ")  # User input for domain
    wordlist = "subdomains.txt"  # Replace with your wordlist file
 
    enumerate_subdomains(target_domain, wordlist)
