import json
import re
import urllib.request
import ssl
from pytube import YouTube
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from downloader_design import Ui_MainWindow

# bu olmazsa ssl certification error veriyor
ssl._create_default_https_context = ssl._create_unverified_context

class Design(QtWidgets.QMainWindow):
    def __init__(self):
        super(Design, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.download)
    
    def download(self):
        api_key = "AIzaSyB0ZrnQKyzvPK6qlOKnB4wohQq8tCrFSHk"
        video_url = self.ui.lineEdit.text()
        helper = Helper()
        video_id = helper.get_id_from_url(video_url)
        api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}" 
        stats = YoutubeStats(api_url)
        title = stats.get_video_title()
        title = helper.title_to_underscore_title(title)
        stats.download_video(video_url, title)

class Helper:
    def __init__(self):
        pass
    
    def title_to_underscore_title(self, title):
        title = re.sub('[\W_]+', "_", title)
        return title.lower()

    def get_id_from_url(self, url):
        # return url.rsplit("/", 1)[1]
        return url.rsplit("=", 1)[1]
    
class YoutubeStats:
    def __init__(self, url):
        self.json_url = urllib.request.urlopen(url)
        self.data = json.loads(self.json_url.read())
    
    def printdata(self):
        print(self.data)
    
    def get_video_title(self):
        return self.data["items"][0]["snippet"]["title"]

    def get_video_description(self):
        return self.data["items"][0]["snippet"]["description"]
    
    def download_video(self, youtube_url, title):
        YouTube(youtube_url).streams.get_highest_resolution().download(filename=title)
        '''
        while YouTube(youtube_url).streams.get_highest_resolution().download(filename=title):
           if YouTube(youtube_url).streams.get_highest_resolution().download(filename=title):
               QtWidgets.QMessageBox.close()
               break
        '''
        
    
        



def app():
    downloadApp = QtWidgets.QApplication(sys.argv)
    window = Design()
    window.show()
    sys.exit(downloadApp.exec_())

app()





'''
video_link = "https://www.youtube.com/watch?v=ntnqT4cEGRk&t"

helper = Helper()
video_id = helper.get_id_from_url(video_link)
url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}" 

yt_stats = YoutubeStats(url)
title = yt_stats.get_video_title()
title = helper.title_to_underscore_title(title)
yt_stats.download_video(video_link, title)
'''

#pyuic5 .ui -o homedesign.py 
#hangi videoya gideceğini video_id ile veriyosun api_key zaten malum
# youtube = discovery.build('youtube', 'v3', developerKey=api_key)


'''
json_url = urllib.request.urlopen(url) # yukarıdaki url e gidip sayfayı getirmesi için
data = json.loads(json_url.read()) # sayfayı json verisi olarak alıyoruz ve dictionary'e çeviriyoruz ?
print(data)
'''

