import requests
import time

API_KEY = "019cb1f1-d7ae-7078-9ebb-ea867ca5d428"

HEADERS = {
    "API-Key": API_KEY,
    "Content-Type": "application/json"
}

SCAN_URL = "https://urlscan.io/api/v1/scan/"
SEARCH_URL = "https://urlscan.io/api/v1/search/"

def submit_scan(target_url):
    payload = {
        "url": target_url,
        "visibility": "public"
    }
    r = requests.post(SCAN_URL, headers=HEADERS, json=payload)
    r.raise_for_status()
    data = r.json()
    return data["uuid"]

def wait_for_result(uuid):
    result_url = f"https://urlscan.io/api/v1/result/{uuid}/"
    print("[+] Waiting for scan result...")
    while True:
        r = requests.get(result_url)
        if r.status_code == 200:
            return r.json()
        time.sleep(5)

def search_similar(domain, title):
    # Build search query
    query = f'domain:{domain}'

    params = {
        "q": query,
        "size": 100
    }

    r = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()["results"]

def main():
    target_url = input("Enter URL to scan: ").strip()

    # Submit scan
    uuid = submit_scan(target_url)
    print(f"[+] Scan submitted: {uuid}")

    # Wait for result
    result = wait_for_result(uuid)

    domain = result["page"]["domain"]
    title = result["page"].get("title", "")

    print(f"[+] Domain: {domain}")
    print(f"[+] Title: {title}")

    # Search similar URLs
    results = search_similar(domain, title)

    print(f"[+] Found {len(results)} similar URLs\n")

    rows = []

    for r in results:
        page = r.get("page", {})
        url = page.get("url")
        scan_id = r.get("_id")

        if url:
            print(url)
            rows.append([url, scan_id])

    

if __name__ == "__main__":
    main()