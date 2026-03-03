import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_hyipexplorer():
    r = requests.get('https://hyipexplorer.com/new', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'})
    soup = BeautifulSoup(r.text, 'html.parser')

    import re 
    detail_links = set()
    for a in soup.find_all('a', href=True): 
        href = a['href'] 
        if re.match(r'^/[a-z0-9_]+_\d+/$', href): 
            detail_links.add('https://www.hyipexplorer.com' + href)
    
    sites = []
    for detail_url in detail_links:
        try:
            r2 = requests.get(detail_url, headers={'User-Agent': 'Mozilla/5.0'})
            soup2 = BeautifulSoup(r2.text, 'html.parser')
            
            # Find the actual website link
            for a in soup2.find_all('a', href=True):
                href = a['href']
                if href.startswith('http') and 'hyipexplorer' not in href:
                    name = soup2.find('h1') or soup2.find('title')
                    sites.append({
                        'name': name.text.strip() if name else href,
                        'url': href,
                        'source': detail_url
                    })
                    break
        except Exception as e:
            print(f"Failed {detail_url}: {e}")
    
    return sites

    '''
    sites = []
    for row in soup.select('table tr'):
        link = row.select_one('a[href*="http"]')
        if link:
            sites.append({
                'name': link.text.strip(),
                'url': link['href'],
                'status': 'paying'
            })
    return sites
'''

def run():
    all_sites = []
    scrapers = [scrape_hyipexplorer]
    
    for scraper in scrapers:
        try:
            sites = scraper()
            all_sites.extend(sites)
            print(f"{scraper.__name__}: found {len(sites)} sites")
        except Exception as e:
            print(f"{scraper.__name__} failed: {e}")
    
    print(f"\n{len(all_sites)} NEW sites found:")
    for s in all_sites:
        print(f"  {s['name']} - {s['url']}")
    
    return all_sites

if __name__ == '__main__':
    run()