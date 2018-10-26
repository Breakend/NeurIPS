import os
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index_template.html')
sitemap_xml = "https://nips.cc/Conferences/2018/Schedule"

sitemap_response = requests.get(sitemap_xml)
soup = BeautifulSoup(sitemap_response.content)
posters = soup.findAll("div", class_="maincard narrower Poster")
final_posters = []

def get_description(event_id):
    url = "https://nips.cc/Conferences/2018/Schedule?showEvent={}".format(event_id)
    print("checking {}".format(url))
    description_response = requests.get(url)
    soup_description = BeautifulSoup(description_response.content)
    description = soup_description.findAll("div", class_="abstractContainer")
    return description[0].text


for poster in posters:
    title = poster.find('div', class_="maincardBody").text
    author = poster.find('div', class_="maincardFooter").text
    date_place = poster.find('div', class_="maincardHeader").text
    event_number = poster.get('id').replace("maincard_", "")
    description = get_description(event_number)

    final_posters.append(dict(title=title, author=author, date_place=date_place, description=description))

invited_talks = soup.findAll("div", class_="maincard narrower InvitedTalk")
invited_talks.extend(soup.findAll("div", class_="maincard narrower InvitedTalkBreimanLecture"))
final_invited_talks = []
for talk in invited_talks:
    title = talk.find('div', class_="maincardBody").text
    author = talk.find('div', class_="maincardFooter").text
    date_place = talk.find('div', class_="maincardHeader").text
    event_number = poster.get('id').replace("maincard_", "")
    description = get_description(event_number)

    final_invited_talks.append(dict(title=title, author=author, date_place=date_place, description=description))

    #TODO: get description by following link
    #
    # parsed = urlparse(url)
    # # group all files from single domain in same folder
    # folder = parsed.netloc
    # # replace "/" with "__" so that files can work on-disk
    # file = parsed.path.replace("/", "__")
    #
    # print "Downloading {url} to {folder}/{file}".format(
    #     url=url, folder=folder, file=file)
    #
    # try:
    #     os.mkdir(folder)
    # except:
    #     pass
    #
    # resp = requests.get(url)
    # with open(folder + "/" + file, "wb") as output:
    #     output.write(resp.content)
#
#
#
#
output_from_parsed_template = template.render(invited_talks=final_invited_talks, posters=final_posters)

# to save the results
with open("test.html", "w") as fh:
    fh.write(output_from_parsed_template)
