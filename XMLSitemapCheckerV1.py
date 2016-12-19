import requests
import robotexclusionrulesparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tkinter import *

sitemaps = []
pages = []
Done = []
#TODO Add proper error handling
#TODO Move robots handling to it's own startup definition
#TODO Make URL count more efficient and less of a hack
#TODO Make custom file name functionality work
#TODO Export CSV file rather than to .txt file
#TODO Add more features?

def GrabSitemaps(sitemap):
    r = requests.get(sitemap)
    soup = BeautifulSoup(r.text,'html.parser')
    locs = soup.findAll('loc')
    for loc in locs:
        root.update()
        if '.xml' in str(loc.text):
            UrlLocation = loc.text
            sitemaps.append(UrlLocation)
        else:
            correctPage = loc.text
            pages.append(correctPage)

def CheckUrlStatus(StartMap):
    parsedUrl = urlparse(StartMap)
    actualUrl = '{}://{}/robots.txt'.format(parsedUrl.scheme,parsedUrl.netloc)
    RoParser = robotexclusionrulesparser.RobotExclusionRulesParser()
    RoParser.fetch(actualUrl)
    for sitepage in pages:
        root.update()
        r = requests.head(sitepage)
        status = r.status_code
        pages.remove(sitepage)
        Done.append('1')
        if RoParser.is_allowed('*',sitepage):
            robots = 'Crawlable'
        else:
            robots = 'Non-Crawlable'
        #print(sitepage,status,robots)
        root.update()
        with open('output.csv','a',encoding='utf-8') as file:
            String = '"{}","{}","{}"'.format(sitepage,status,robots)
            file.write(String)
        Pages = len(Done)
        ApplicationMessage.set('Pages completed {}'.format(Pages))
        root.update()


#tkinter setup
root = Tk()
root.iconbitmap('Adapt.ico')
root.wm_title('Sitemap Checker')

ApplicationMessage = StringVar()
ApplicationMessage.set('Waiting to start')

SiteMapURL = Label(root,text='Sitemap/Sitemap Index URL')
SiteMapURL.grid(row=0)
OutPutFileName = Label(root,text='Name for output file')
OutPutFileName.grid(row=1)

SiteMapEntry = Entry(root)
SiteMapEntry.grid(row=0,column='1')
OutPutFileName = Entry(root)
OutPutFileName.grid(row=1,column='1')

def main():
    StartMap = SiteMapEntry.get()
    GrabSitemaps(StartMap.strip())
    CheckUrlStatus(StartMap)
    while len(sitemaps) > 0:
        for sitemap in sitemaps:
            root.update()
            GrabSitemaps(sitemap)
            sitemaps.remove(sitemap)
        CheckUrlStatus(StartMap)

StartButton = Button(root,text="Start Sitemap Check",command=main)
StartButton.grid(columnspan=2)
Status = Label(root,textvariable=ApplicationMessage)
Status.grid(columnspan=2)

root.mainloop()
