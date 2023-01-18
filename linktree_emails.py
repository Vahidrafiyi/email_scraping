from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import random
import time
import pandas
import pickle

excel_data = pandas.read_excel('linktree_users.xlsx', sheet_name='Sheet1')
urls = excel_data['urls'].to_list()[:1000]

not_found_email_urls = []
#Column name
names = []
mails = []
gumroad_urls = []
platform_urls = []
mails_count = 0
urls_count = 0
ua = UserAgent()
data = {
  'username': names,
  'gumroad': gumroad_urls,
  'platform': platform_urls,
  'mail': mails,
  'urls_without_email': not_found_email_urls
}


def save_state_data():
  with open('data.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_state_data():
  with open('data.pickle', 'rb') as handle:
    return pickle.load(handle)


def save_state_platform():
  with open('platform.pickle', 'wb') as handle:
    pickle.dump(platform_urls, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_state_platform():
  with open('platform.pickle', 'rb') as handle:
    return pickle.load(handle)


def save_state_mails_count():
  with open('mails_count.pickle', 'wb') as handle:
    pickle.dump(mails_count, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_state_mails_count():
  with open('mails_count.pickle', 'rb') as handle:
    return pickle.load(handle)


def save_state_urls_count():
  with open('urls_count.pickle', 'wb') as handle:
    pickle.dump(urls_count, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_state_urls_count():
  with open('urls_count.pickle', 'rb') as handle:
    return pickle.load(handle)


def save_state_urls():
  with open('urls.pickle', 'wb') as handle:
    pickle.dump(urls, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_state_urls():
  with open('urls.pickle', 'rb') as handle:
    return pickle.load(handle)


try:
  urls = load_state_urls()
  data = load_state_data()
  mails_count = load_state_mails_count()
  urls_count = load_state_urls_count()
  platform_urls = load_state_platform()
except:
  pass

for url in urls:
  urls_count += 1
  print('url: ' + str(urls_count))
  print(url)
  time.sleep(random.uniform(5, 15))  # Add a random delay between requests
  headers = {'User-Agent': ua.random}  # Use a randomized User-Agent
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  links = soup.find_all(href=True)
  email_found = False
  email_link = ''
  for link in links:
    if 'mail.com' in link['href']:
      email_found = True
      email_link = link['href']
  if email_found:
    name = url.split('/')[::-1][0]
    data['mail'].append(email_link)
    data['username'].append(name)
    data['gumroad'].append(f'https://gumroad.com/{name}')
    data['platform'].append(url)
    mails_count += 1
    print('email: ' + str(mails_count))
    urls.remove(link)
  else:
    index = urls.index(url)
    data['urls_without_email'].append(urls.pop(index))
  save_state_data()
  save_state_urls()
  save_state_mails_count()
  save_state_urls_count()
  save_state_platform()

#   if mail:
#     mails_count += 1
#     print(mails_count)
#     mails.append(mail.group(0))
#     name = url.split('/')[::-1][0]
#     names.append(name)
#     gumroad_urls.append(f'https://gumroad.com/{name}')
#   else:
#     urls.remove(url)

data_ex = pandas.DataFrame.from_dict(data, orient='index')
data = data_ex.transpose()
writer = pandas.ExcelWriter("linktree_mails.xlsx")
data.to_excel(writer)
writer.save()
