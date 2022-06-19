import sys
from PyQt5 import QtWidgets
import htmlViewUi


class htmlViewWindow(QtWidgets.QDialog, htmlViewUi.Ui_Dialog):
    
   
    
    def __init__(self,page):
        super().__init__()
        self.setupUi(self)
        #print(page)
        self.textBrowserHtmlView.setHtml(page)
        #self.QWebView=QtWidgets.QWebView(Dialog)
        #self.QWebView.setObjectName("webViewTemp")
        #self.verticalLayout.addWidget(self.QWebView)
        #self.QWebView=setHtml(page)
        #self.QWebView.show()
        