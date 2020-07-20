import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


# This script uploads news from RSS feeds to staffbase channel
# The RSS feed url needs to be defined is the variable rssFeedUrl
# the staffbase channel to which we need to post is defined in variable staffbase_channel
# The api authorisation token( with minimum editorial access) needs to be inserted in authorisation header before running

AuthorizationHeader = "Basic insert_api_token_here"


def rssToItems(url):
    response = requests.get(url)
    retLst = []
    soup = BeautifulSoup(response.text)
    for item in soup.findAll("item"):
        title = item.find("title").getText()
        # guid from rss feed is mapped to external id.If guid is not present in rss feed, this needs to be generated uniqely for each post
        guid = item.find("guid").getText()
        content = item.find("description").getText()
        image = item.find("media:thumbnail")["url"]
        itemDate = item.find("pubdate").getText()
        dt = datetime.strptime(itemDate, "%a, %d %b %Y %H:%M:%S +%f")
        pubDate = datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
        retLst.append({
            "externalID": guid,
            "contents": {
                "en_US": {
                    "content": content,
                    "image": image,
                    "teaser": "This teaser should be text only.",
                    "title": title
                }}, "published": pubDate})
    return retLst


def post(url, item):
    headers = {
        "Content-Type": "application/json",
        "Authorization": AuthorizationHeader
    }

    print("post url : %s " % (url))
    # converting dict to json
    staffbase_post_request = requests.post(
        url, data=json.dumps(item), headers=headers)
    print(staffbase_post_request.status_code)


if __name__ == "__main__":
    rssFeedUrl = "https://www.cnet.com/rss/how-to/"
    items = rssToItems(rssFeedUrl)
    staffbase_api = "https://backend.staffbase.com/api/channels/"
    staffbase_channel = "5f15455ad960e93b74c754a8"
    staffbase_url = staffbase_api+staffbase_channel+"/posts"
    print(staffbase_url)
    for item in items:
        post(staffbase_url, item)
