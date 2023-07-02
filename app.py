import requests
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

headers = {
    'authority': 'job-search-api.svc.dhigroupinc.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.dice.com',
    'referer': 'https://www.dice.com/',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'x-api-key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8',
}

params = {
    'countryCode2': 'US',
    'radius': '9999',
    'radiusUnit': 'mi',
    'page': '1',
    'pageSize': '100',
    'facets': 'employmentType|postedDate|workFromHomeAvailability|employerType|easyApply|isRemote',
    'filters.employmentType': 'CONTRACTS|THIRD_PARTY',
    'filters.postedDate': 'ONE',
    'fields': 'id|jobId|summary|title|postedDate|modifiedDate|jobLocation.displayName|detailsPageUrl|salary|clientBrandId|companyPageUrl|\
        companyLogoUrl|positionId|companyName|employmentType|isHighlighted|score|easyApply|employerType|workFromHomeAvailability|isRemote|debug',
    'culture': 'en',
    'recommendations': 'true',
    'interactionId': '0',
    'fj': 'true',
    'includeRemote': 'true',
    'eid': 'a6zd7NUgR0Wy8Tzf36TS2Q_|Tb30SliOSoWcjf4RBdhGSg_0',
}
jobs = set()
response = requests.get('https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search', params=params, headers=headers)
i = 0
if response.status_code == 200:
    page_limit = 2
    for page in range(2, page_limit+2):
        response = json.loads(response.text)
        page_limit = response["meta"]["pageCount"]
        print("\n\n *** Currently on Page # {} *** \n\n" .format(response["meta"]["currentPage"]))
        
        for job in response["data"]:
            job_page = job["detailsPageUrl"]
            job_title = job["title"]
            company_name = job["companyName"]
            job_type = job["employmentType"]

            detail_page = requests.get(job_page, headers=headers)
            tree = html.fromstring(detail_page.content) 
            job_description =  '\n'.join(tree.xpath('//div[@id="jobDescription"]//text()'))

            print(i, job_page)
            i+=1
            
        params["page"] = page
        response = requests.get('https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search', params=params, headers=headers)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)