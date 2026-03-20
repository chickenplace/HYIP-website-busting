import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import re
from tqdm import tqdm

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = 8
MAX_WORKERS = 20

SCAM_PATTERNS = {
    "guaranteed profit": 3,
    "daily return": 3,
    "double your money": 4,
    "risk free": 3,
    "investment plan": 2,
    "minimum deposit": 2,
    "referral bonus": 2,
    "withdraw": 1,
    "passive income": 2,
    "roi": 2,
    "crypto": 1,
    "trading bot": 2,
    "hyip": 3,
    "wallet connect": 1,
    "guaranteed": 3,
    "yield": 2,
    "high yield": 3,
    "investment": 2,
    "plan": 2,
    "profit": 3,
    "income": 2,
    "mining": 2,
    "earn": 2,
    "minimum deposit": 2,
    "weekly return": 2,
    "future": 1

}

REGEX_PATTERNS = [
    (r"\d+% (daily|per day|weekly)", 3),
    (r"earn \$?\d+ per day", 3),
    (r"minimum deposit", 2),
]

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ").lower()

def scan_domain(domain):
    url = "http://" + domain
    result = {"domain": domain, "score": 0, "matches": ""}

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        text = extract_text(r.text)

        matches = []
        score = 0

        for kw, weight in SCAM_PATTERNS.items():
            if kw in text:
                matches.append(kw)
                score += weight

        for pattern, weight in REGEX_PATTERNS:
            if re.search(pattern, text):
                matches.append(pattern)
                score += weight

        result["score"] = score
        result["matches"] = "; ".join(matches)

    except Exception as e:
        result["score"] = -1
        result["matches"] = "ERROR"

    return result

# Load domains
with open("suspicious_domains.txt") as f:
    domains = [d.strip() for d in f if d.strip()]

results = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(scan_domain, d) for d in domains]

    for future in tqdm(as_completed(futures), total=len(futures)):
        results.append(future.result())

# Save CSV
with open("scan_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["domain", "score", "matches"])
    writer.writeheader()
    writer.writerows(results)

print("Scan complete.")