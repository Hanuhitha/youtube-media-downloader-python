import sys,os
from PyQt5.QtWidgets import QProgressBar,QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,QRadioButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pytube import YouTube 

#layout to download videos/audio
class SecondWindow(QWidget):
    def __init__(self,filesize = None):
        super().__init__()
        self.filesize = 0
        
    def init_ui(self,rbuttons=None,ids=None,yt_obj=None,file_name = None):
        self.setStyleSheet("background-color: #1e3d59;")
        print(rbuttons)
        self.yt_obj = yt_obj
        self.ids = ids
        self.file_name_original = file_name
        self.main_wd =  MainWindow()
        self.setWindowTitle('second window')
        self.label = QLabel('Please select the quality of download ')
        self.label.setStyleSheet("color:white;font-weight:strong")
        self.label2 = QLabel("")
        self.label3 = QLabel(self.file_name_original)
        self.label3.setStyleSheet("color:white;font-weight:strong")
        self.button_2 = QPushButton('download', self)
        self.button_2.clicked.connect(self.onClick)
        self.button_2.setStyleSheet("background-color : #4aa96c")
        self.cls_btn =  QPushButton('back', self)
        self.cls_btn.clicked.connect(self.mainLayout)
        self.cls_btn.setStyleSheet("background-color : #ffc107")
        self.progressBar = QProgressBar(self)

        self.button_2.setFixedHeight(40)
        self.cls_btn.setFixedHeight(40)
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.label)
        self.rdbtn = []
        for rb in rbuttons:
            print(rb)
            self.rdbtn.append(QRadioButton(rb))
        for rbs in  self.rdbtn:  
            rbs.setStyleSheet("color : white")
            self.layout1.addWidget(rbs)
        self.layout1.addWidget(self.label2)
        self.layout1.addWidget(self.label3)
        self.layout1.addWidget(self.progressBar)
        self.layout1.addWidget(self.button_2)
        self.layout1.addWidget(self.cls_btn)
        
        self.setGeometry(200, 200, 800, 400)
        self.setLayout(self.layout1)
        self.setWindowTitle('Download window')
        self.show()

    def onClick(self):
        """
        this function reads the radio buttons and based on the selected option downloads the media file to /downloads folder
        """
        flag = 0
        tag_id = None
        for i,rdbtn in enumerate(self.rdbtn):
            if rdbtn.isChecked():
                flag = 1
                print(rdbtn.text())
                tag_id = self.ids[i]
                break             
        if flag ==0:
            return
        stream = self.yt_obj.streams.get_by_itag(int(tag_id))
        self.filesize = stream.filesize
        stream.download(filename=stream.default_filename,output_path="Downloads")
        print("download succesfull")
    def mainLayout(self):
        #to go back to the main layout
        self.main_wd.show()
        self.close()

    def progress_Check(self, chunk = None, file_handler = None, bytes_remaining = None):
        #Gets the percentage of the file that has been downloaded.
        percent = (100*(self.filesize-bytes_remaining))/self.filesize
        self.progressBar.setValue(int(percent))
        QApplication.processEvents()        

class MainWindow(QWidget):
    """
    This is the main layout of the application
    """
    def __init__(self):
        super().__init__()
        self.init_ui(['audio','video'])
    def init_ui(self,rbuttons):
        """
        method to initialize the UI
        """
        self.setStyleSheet("background-color: #1e3d59;")
        self.secondWindow = SecondWindow()
        self.label = QLabel('Please paste the youtube video URL ')
        self.label.setStyleSheet("color:white;font-weight:strong")
        self.label2 = QLabel("")
        self.url_link = QLineEdit(self)
        self.url_link.setStyleSheet("background-color : white")
        self.button_1 = QPushButton('Proceed to download', self)
        self.button_1.setStyleSheet("background-color : #ffc107")
        self.button_1.setFixedHeight(40)
        self.url_link.setFixedHeight(40)
        self.label.setAlignment(Qt.AlignCenter)
        self.button_1.clicked.connect(self.onClick)
        self.warning = QLabel(' ')
        self.warning.setStyleSheet("color:red")
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.layout.addWidget(self.label)
        self.layout.addWidget( self.url_link)
        self.rdbtn = []
        for rb in rbuttons:
            print(rb)
            self.rdbtn.append(QRadioButton(rb))
        for rbs in  self.rdbtn:  
            rbs.setStyleSheet("color : white")
            self.layout.addWidget(rbs)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.button_1)
        self.layout.addWidget( self.warning)
        self.layout.addStretch()
        self.layout.setAlignment(Qt.AlignTop)
        self.setGeometry(200, 200, 800, 400)
        self.setLayout(self.layout)
        self.setWindowTitle('Youtube downloader')

    def onClick(self):
        """
        this function reads the link and the radio buttons selected audio/video  and based on the selected options create a youtube object
        """
        check_flag = 0
        link=self.url_link.text()
        self.warning.setText('....')
        QApplication.processEvents()
       
        try: 
            # object creation using YouTube
            # which was imported in the beginning 
            yt = YouTube(link, on_progress_callback=self.secondWindow.progress_Check) 
            self.warning.setText('Please wait....')
            QApplication.processEvents()
            
        except: 
            print("Connection Error")
            if len(link) == 0:
                self.warning.setText('Please enter valid link')
                print(len(link))
            return #to handle exception 
        
        media_type = 'mp4' #for video
        self.warning.setText('Please wait....')
        for rdbtn in self.rdbtn:
            #iterating the radiobuttons to see if audio is selected or video
            if rdbtn.isChecked():
                check_flag = 1
                print(rdbtn.text())
                if 'audio' in rdbtn.text():
                    tags = [x.itag for x in yt.streams.filter(only_audio=True,)]
                    ids = [str(x.abr )for x in yt.streams.filter(only_audio=True)]
                else:
                    tags = [x.itag for x in yt.streams.filter(file_extension=media_type,progressive=True)]
                    ids = [str(x.resolution )for x in yt.streams.filter(file_extension=media_type,progressive=True)]
        file_name_original = yt.streams.filter(file_extension=media_type,progressive=True).first().default_filename
        if check_flag == 0:
            self.warning.setText('Please select audio or video....')
            return     
        else:
            self.warning.setText('Please wait....')
            QApplication.processEvents()
        
        if len(tags)<1:
            #if nothing is returned from the youtube, don't do anything
            return
        else:
            #open second layout
            self.secondWindow.init_ui(ids,tags,yt,file_name_original)
            self.close()
        

if __name__ == '__main__':
    if not os.path.isdir("Downloads"):
        os.makedirs("Downloads")
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())


