import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import tldextract

def company_info_links(website:str, about_page_names):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    reqs = requests.get(website, headers=headers)
    if reqs.status_code == 200:
        soup = BeautifulSoup(reqs.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                full_url = urljoin(website, href)
                urls.append(full_url)
        return list(set(urls))
    else:
        print(f"Failed to fetch the URL. Status code: {reqs.status_code}")

        

def contains_keyword(link, about_page_names):
    """_summary_

    Args:
        link (_type_): _description_
        about_page_names (_type_): _description_

    Returns:
        _type_: _description_
    """
    for keyword in about_page_names:
        if re.search(r'\b' + re.escape(keyword) + r'\b', link, re.IGNORECASE):
            return True
    return False

def get_links(website):
    """_summary_

    Args:
        website (_type_): _description_

    Returns:
        _type_: _description_
    """
    extracted_info = tldextract.extract(website)
    about_page_names = [
                    "About",
                    "About Us",
                    "Our Story",
                    'Our mission',
                    "Who We Are",
                    "what we do"
                    "Meet the Team",
                    f"About {extracted_info.domain}",
                    "Mission & Vision",
                    "Our History",
                    "Meet the Founders",
                    "Our Mission",
                    "The Company",
                    "What We Do",
                    "Our Purpose",
                    "Our Values",
                    "Who We Are and What We Do",
                    "Our Background",
                    "About the Brand",
                    "Our Philosophy",
                    "Our Journey",
                    "Our Culture",
                    'our-partners',
                    "partners/*",
                    "Affiliates",
                    "Collaborators",
                    "Alliances",
                    "Associates",
                    "Sponsors",
                    "Contributors",
                    "Cooperators",
                    "Network",
                    "Supporters",
                    "Associations",
                    "Friends",
                    "Participating Organizations",
                    "Strategic Allies",
                    "Co-creators",
                    "Industry Partners"
                ]
    links = company_info_links(website, about_page_names)
    filtered_links = [link for link in links if contains_keyword(link,about_page_names)]
    filtered_links.append(website)

    return list(set(filtered_links)), extracted_info.domain

