from bs4 import BeautifulSoup
import requests

# https://stackoverflow.com/questions/42237672/python-toomanyredirects-exceeded-30-redirects -> 여기서 찾은 정보임
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

def scrape_wework(term):
  URL = f"https://weworkremotely.com/remote-jobs/search?term={term}"
  wework_res = requests.get(URL)

  soup = BeautifulSoup(wework_res.text, "html.parser")
  whole_jobs = soup.find("body", {"class":"home"}).find("section", {"id":"category-2"})
  programming_lists= whole_jobs.find("ul").find_all("li")
  wework_jobs = []
  for programming_list in programming_lists:
    try:
      wework_link = programming_list.find("a")["href"]
      wework_title = programming_list.find("a").find("span", {"class":"title"}).string
      wework_company = programming_list.find("a").find("span", {"class":"company"}).string
    except:
      continue
    job = {"title" : wework_title, "company": wework_company, "link": wework_link, "URL": URL}
    wework_jobs.append(job)
  return wework_jobs
    

def scrape_SO(term):
  SO_res = requests.get(f"https://stackoverflow.com/jobs?q={term}&r=true")
  soup = BeautifulSoup(SO_res.text, "html.parser")

# 페이지 구하기
  page_links = soup.find("div", {"class":"s-pagination"}).find_all("a")[:-1] 
  page = []
  # 원래 2페이지인데 12페이지까지 나옴... 참고!!
  for page_link in page_links:
    page_link = page_link.find("span").string
    page.append(page_link)
  # 마지막 페이지 구함
  last_page = page[-1]

  for page in range(int(last_page)):
    SO_result = requests.get(f"https://stackoverflow.com/jobs?q={term}&r=true&pg={page}")
    result_soup = BeautifulSoup(SO_result.text, "html.parser")


# 각 페이지 당 직업 구하기
    job_lists = result_soup.find("div", {"class":"listResults"}).find_all("div", {"class":"grid--cell fl1"})
    URL = "https://stackoverflow.com/" 
    SO_jobs = []
    for job_list in job_lists:
      try:
        title = job_list.find("h2",{"class":"fs-body3"}).find("a").string
      except:
        continue
      company = job_list.find("h3", {"class":"fs-body1"}).find("span").string
      # link가 뒷부분만 있으니까 조심하자! 나중에 수정해야 할 수도 잇음
      link = job_list.find("h2",{"class":"fs-body3"}).find("a")["href"]
      job = {"title": title, "company": company, "URL": URL, "link": link}
      SO_jobs.append(job)
   

  return SO_jobs


def scrape_remote(term):
  URL = f"https://remoteok.io"
  remote_res = requests.get(f"{URL}/remote-dev+{term}-jobs", headers=headers)
  
  soup = BeautifulSoup(remote_res.text, "html.parser")
  jobs = soup.find("div", {"class":"container"}).find("table", {"id":"jobsboard"}).find_all("tr", {"class":"job"})
  remote_jobs =[]
  for job in jobs:
    title = job.find("td", {"class":"company position company_and_position"}).find("h2").string
    company = job.find("td", {"class":"company position company_and_position"}).find("h3").string
    company_link = job.find("td", {"class":"company position company_and_position"}).find("a",{"class":"preventLink"})["href"]
    job_information = {"title": title, "company": company, "link": company_link, "URL": URL}
    remote_jobs.append(job_information)
  return remote_jobs
    


  

