import requests
from bs4 import BeautifulSoup
import json, re, os

import asyncio, aiohttp
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

def check_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)

def load_cookies(cookies_json):
    raw_cookies = json.load(open(cookies_json))
    cookies = {}
    for cookie in raw_cookies:
        name = cookie['name']
        value = cookie['value']
        cookies.update({name:value})
    return cookies

def get_contact(url):
    html = render(url)
    contact = getContactInfo(html)
    return contact

def render(url):
    if "showroom" not in url:
        url = "/".join(url.split("/")[:-1]) + "/contact-info.html"
    cookies = load_cookies("./data/cookies.json")
    req = requests.get(url, headers=headers, cookies=cookies)
    return req.text

def getPage(html):
    page = BeautifulSoup(html,"html.parser")
    return page

def getContactInfo(html):

    def method_1(page):
        contact_block = page.find("div",{"class":re.compile("contact-block")})
        company_name = page.find("div",{"class":"title-txt"}).text.strip()
        details = getContactDetails(contact_block)
        contact_supplier = contact_block.find("div",{"class":"contact-customer"})
        info_details = contact_supplier.find("div",{"class":"info-detail"})
        contact_name = info_details.find("div",{"class":"info-name"}).text.strip()
        info_details = info_details.find_all("div",{"class":"info-item"})            
        contact_info = {
            "company_name": company_name,
            "company_url": url,
            "contact_name": contact_name,
            "telephone": getFromDict(details,'telephone'),
            "mobile_phone": getFromDict(details,'mobile_phone'),
        }
        return contact_info

    def method_2(page):
        company_name = page.find("div",{"class":"com-name-txt"}).text.strip()
        content = page.find("div",{"class":"com-info-wp"})
        content = content.find("div",{"class":"info-content"})
        info = content.find("div",{"class":"person"})
        positions = info.find_all("div",{"class":"manager"})
        contact_info = {
            "contact_name": info.find("div",{"class":"name"}).text.strip(),
            "company_name": company_name,
            "company_url": url,
        }
        content = content.find("div",{"class":"info-cont-wp"})
        items = content.find_all("div",{"class":"item"})
        for item in items:
            label = item.find("div",{"class":"label"}).text.strip()
            label = label.strip(":").lower().replace(" ","_")
            info = item.find("div",{"class":"info"}).text.strip()
            info = info.split("\n")[0]
            if label in ["address","zip_code"]:
                label = "company_" + label
            contact_info.update({label:info})
        return contact_info

    def validate(dict):
        data = {}
        attrs = [
            "company_name",
            "company_url",
            "contact_name",
            "telephone",
            "mobile_phone",
        ]
        for attr in attrs:
            try: value = dict[attr]
            except: value = None
            if value == "": value = None
            data.update({attr:value})
        return data

    # read the text file into bs4 object
    page = getPage(html)
    url = page.find("link",{"rel":"canonical"})['href']
    if "showroom" not in url:        
        try: contact_info = method_1(page)
        except: contact_info = method_2(page)
    else:
        contact_info = method_2(page)
    return validate(contact_info)

def getContactDetails(page):
    content = page.find("div",{"class":"contact-info"})
    content = content.find_all("div",{"class":"info-item"})
    details = {}
    for c in content:
        label = c.find("div",{"class":"info-label"}).text.strip()
        label = label.strip(":").replace(" ","_").lower()
        field = c.find("div",{"class":"info-fields"}).text.strip()
        details.update({label:field})
    return details

def getFromDict(dict, key):
    try: return dict[key]
    except: return None

async def render_from(session,url):
    loop = asyncio.get_event_loop()
    async with session.get(url) as r:
        result = await loop.run_in_executor(None, getContactInfo, await r.text())
        return result

async def render(session,urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(render_from(session,url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

cookies = load_cookies("./data/cookies.json")
async def render_all(urls):
    async with aiohttp.ClientSession(headers=headers,cookies=cookies) as session:
        results = await render(session,urls)
        return results