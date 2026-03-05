import re

FLAGS = re.IGNORECASE | re.MULTILINE

PATTERNS = {
    "cryptolang": re.compile(
        r'(crypto|btc|eth|usdt|usdc|bnb|trx|xrp|doge|sol|defi|nft|mining|stake|staking|yield|profit|income|invest|loan|capital|fund|coin)', 
        FLAGS
    ),
    "hyiplang": re.compile(
        r'(double|bonus|reward|daily|weekly|roi|guarantee|secure|fast|instant|passive|forex|trading|robot|ai|bot|signal|money)',
        FLAGS
    ),
    "brand_impersonation": re.compile(
        r"(binance|coinbase|kraken|bybit|okx|kucoin|metamask|trustwallet)",
        FLAGS
    ),

    "numbers_in_domain": re.compile(r"[0-9]{2,}", FLAGS),

    "multi_hyphen": re.compile(r"[a-z]{2,}(-[a-z]{3,}){2,}", FLAGS),

    "year_pattern": re.compile(r"(2024|2025|2026)", FLAGS)

}

def scan_domain(domain: str) -> dict:
    results = {} 
    for name, pattern in PATTERNS.items(): 
        if name in [ 
            "crypto_keywords", "hyip_keywords", "brand_impersonation",
            "numbers_in_domain", "multi_hyphen", "year_pattern"
        ]:
            matches = pattern.findall(domain) 
            if matches:
                results[name] = matches 
    return results if results else None

def scan_domain_file(filename):
    count = 0
    with open(filename, "r") as f:
        for line in f:
            domain = line.strip()

            # skip empty lines
            if not domain:
                continue

            hits = scan_domain(domain)

            # only show suspicious ones
            if hits:
                print(f"[!] {domain}")
                print(hits)
                print("-" * 40)
                with open("suspicious_domains.txt", "a") as out:
                    out.write(f"{domain}\n")
                count += 1

    print(f"Total suspicious domains found: {count}")

if __name__ == "__main__":
    test_domains = [
        "bestcrypto2024.com",
        "fast-forex-trading.net",
        "binance-secure-wallet.io",
        "invest-in-defi-earnings.com",
        "nft-mining-bot.org",
        "pASSIve-income-2025.co",
        "secure-staking-platform.com",
        "guaranteed-roi-2026.net",
        "double-your-btc-now.com",
        "ai-trading-signal.io",
        "72e51e27fdd44d30.com",
        "gooelg.com"
    ]

    scan_domain_file("domain-names.txt")

'''
    for d in test_domains:
        d = d.lower()
        d = re.sub(r"<[^>]+>", " ", d)  # strip HTML

    for domain in test_domains:
        results = scan_domain(domain)
        if results:
            print(results)
'''