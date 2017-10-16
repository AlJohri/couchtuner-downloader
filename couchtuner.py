import os
import sys
import traceback
import requests
import lxml.html
import youtube_dl

# 'preview' page
# https://www.couchtuner.onl/2017/10/madam-secretary-season-4-episode-2-off-the-record/"

# 'video' page
# http://video247.xyz/madam-secretary-s4e2-off-the-record/

blacklist = ['vidup.me', 'thevideo.me']
# whitelist = ['vshare.eu', 'openload.co']

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python couchtuner.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    response = requests.get(url)
    if "Watch It Here :" in response.text:
        doc = lxml.html.fromstring(response.content)
        url = doc.cssselect("a[rel='bookmark']")[0].get('href')
        response = requests.get(url)

    # parse video page
    doc = lxml.html.fromstring(response.content)
    folder = doc.cssselect('h2.postSingle')[0].text.strip().replace(' ', '_')
    os.makedirs(folder, exist_ok=True)
    iframes = doc.cssselect('.postTabs_divs iframe')
    iframe_urls = [iframe.get('src') for iframe in iframes
                    if not any(domain in iframe.get('src') for domain in blacklist)]
    with youtube_dl.YoutubeDL({'outtmpl': folder + '/%(title)s-%(id)s.%(ext)s'}) as ydl:
        for url in iframe_urls:
            print(f'attempting to download {url} to {folder}')
            try:
                ydl.download([url])
            except Exception as e:
                continue
            else:
                break
