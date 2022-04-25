from xml.etree.ElementTree import tostring
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QPushButton, QTableWidgetItem
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from mytablewidget import MyTableWidget
import sys, datetime, re, json


def open_Area_Json(path):
	with open(path,'r',encoding='utf-8') as f:
		return json.load(f)







class Ui(object):
    CHECK_CODE_1 = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    CHECK_CODE_2 = ['1','0','X','9','8','7','6','5','4','3','2']
    Regular_Expression = "(?P<province>\d{2})(?P<city>\d{2})(?P<area>\d{2})(?P<born_year>\d{4})(?P<born_month>\d{2})(?P<born_day>\d{2})(?P<gender>\d{1}){3}"
    thisYear = datetime.datetime.now().year

    #定义UI
    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(979, 591)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        #plainTextEdit
        self.text = QPlainTextEdit(MainWindow)
        self.text.setEnabled(True)
        self.text.setGeometry(QtCore.QRect(10, 10, 291, 501))
            #设置文本框格式
        self.text.setFont(QFont('Arial',12))
        self.text.setPlaceholderText('请输入身份证号...')
        #table
        self.table = MyTableWidget(MainWindow)
        self.table.setEnabled(True)
        self.table.setGeometry(QtCore.QRect(310, 10, 661, 501))
            #设置表格格式
        self.table.setColumnCount(5)
        self.table.setColumnWidth(0, 170)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 40)
        self.table.setColumnWidth(4, 40)
        self.table.setHorizontalHeaderLabels(['身份证', '地区', '生日', '年龄', '性别'])
        #button
        self.btn = QPushButton(MainWindow)
        self.btn.setEnabled(True)
        self.btn.setGeometry(QtCore.QRect(650, 520, 321, 61))
        self.btn.setText("查询")

        #clearButtom
        self.clearBtn = QPushButton(MainWindow)
        self.clearBtn.setEnabled(True)
        self.clearBtn.setGeometry(QtCore.QRect(580, 520, 61, 28))
        self.clearBtn.setText("Clear")
        #
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "身份证信息查询"))

    def id_sum(self,ID):
        sum=0
        for x in range(0,17):
            sum += self.CHECK_CODE_1[x] * int(ID[x])
        return sum

    def clickBtn(self):
        cur_row_count = self.table.rowCount()
        if cur_row_count!=0:
            self.table.setRowCount(cur_row_count+1)
            self.table.setItem(cur_row_count,0,QTableWidgetItem(''))
            self.table.setItem(cur_row_count,1,QTableWidgetItem(''))
            self.table.setItem(cur_row_count,2,QTableWidgetItem(''))
            self.table.setItem(cur_row_count,3,QTableWidgetItem(''))
            self.table.setItem(cur_row_count,4,QTableWidgetItem(''))


        #获取textEdit内容
        text=str(self.text.toPlainText())
        if text !='':
            #分存数据
            id_list = [str(x) for x in text.split('\n')]
            #检验
            for i in range(len(id_list)):
                ID = id_list[i]

                
                #判断ID长度
                if len(ID)==18 and ID[17]=='x':
                    ID=ID.replace('x' , 'X')
                if ID == '':
                    continue
                elif len(ID) != 18 or ID[17] != self.CHECK_CODE_2[self.id_sum(ID)%11]:
                    cur_row_count = self.table.rowCount()
                    self.table.setRowCount(cur_row_count+1)
                    self.table.setItem(cur_row_count,0,QTableWidgetItem(ID))
                    self.table.setItem(cur_row_count,1,QTableWidgetItem('[格式错误]'))
                    self.table.setItem(cur_row_count,2,QTableWidgetItem(''))
                    self.table.setItem(cur_row_count,3,QTableWidgetItem(''))
                    self.table.setItem(cur_row_count,4,QTableWidgetItem(''))
            
                else:
                    #获取信息		省 市 区 年 月 日 性别
                    res = re.search(self.Regular_Expression,ID)
                    #定义变量
                    provinceName = ''
                    cityName = ''
                    areaName = ''
                    year = res['born_year']
                    month = res['born_month']
                    day = res['born_day']
                    age = self.thisYear - int(year)
                    isMale = '男' if int(res['gender'])%2 else '女'

                    #从表中查找数据
                    provinceList = data['mallProvinceList']
                    for i in range(len(provinceList)):
                        if provinceList[i]['provinceCode'][0:2]==res['province']:
                            provinceName = (provinceList[i]['provinceName'])

                            cityList = provinceList[i]['mallCityList']
                            for j in range(len(cityList)):
                                if cityList[j]['cityCode'][2:4]==res['city']:
                                    cityName = (cityList[j]['cityName'])

                                    areaList = cityList[j]['mallAreaList']
                                    for k in range(len(areaList)):
                                        if areaList[k]['areaCode'][4:6]==res['area']:
                                            areaName = areaList[k]['areaName']
                    
                    if provinceName=="" or cityName=="" or areaName=="":
                        #从老表中查找数据
                        provinceList = old_data['oldCity']
                        for i in range(len(provinceList)):
                            if provinceList[i]['provinceCode']==res['province']:

                                cityList = provinceList[i]['mallCityList']
                                for j in range(len(cityList)):
                                    if cityList[j]['cityCode']==res['province']+res['city']+res['area']:
                                        cityName = (cityList[j]['cityName'])
                                    else:
                                        pass
                        if cityName == "":
                            print('数据库不全:'+res['province']+res['city']+res['area'])
                        cur_row_count = self.table.rowCount()
                        self.table.setRowCount(cur_row_count+1)
                        self.table.setItem(cur_row_count,0,QTableWidgetItem(ID))
                        self.table.setItem(cur_row_count,1,QTableWidgetItem(cityName))
                        self.table.setItem(cur_row_count,2,QTableWidgetItem(year+'/'+month+'/'+day))
                        self.table.setItem(cur_row_count,3,QTableWidgetItem(str(age)))
                        self.table.setItem(cur_row_count,4,QTableWidgetItem(isMale))
                    else:
                        # if provinceName=="":
                        #     provinceName=' null'
                        # if cityName=="":
                        #     cityName=' null'
                        # if areaName=="":
                        #     areaName=' null'
                        if provinceName==cityName:
                            cityName==''
                        #新建一行，写入数据
                        cur_row_count = self.table.rowCount()
                        self.table.setRowCount(cur_row_count+1)
                        self.table.setItem(cur_row_count,0,QTableWidgetItem(ID))
                        self.table.setItem(cur_row_count,1,QTableWidgetItem(provinceName+cityName+areaName))
                        self.table.setItem(cur_row_count,2,QTableWidgetItem(year+'/'+month+'/'+day))
                        self.table.setItem(cur_row_count,3,QTableWidgetItem(str(age)))
                        self.table.setItem(cur_row_count,4,QTableWidgetItem(isMale))




                    
        
        
        #清空text
        self.text.setPlainText('')

    def clickClearBtn(self):
        for rowNum in range(0,self.table.rowCount())[::-1]:
            #逆序删除，正序删除会有一些删除不成功
	        self.table.removeRow(rowNum)
    
    



class MainWidow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWidow,self).__init__(parent)
        #创建UI
        ui = Ui()
        ui.setupUI(self)
        #按钮监听
        ui.btn.clicked.connect(lambda:ui.clickBtn())
        ui.clearBtn.clicked.connect(lambda:ui.clickClearBtn())
    
    





#读取json数据
data = open_Area_Json('Area.json')

old_data = open_Area_Json('AbolishedCity.json')
#创建窗口
app = QApplication(sys.argv)
#程序初始化
MainWindow = MainWidow()
#显示ui
MainWindow.show()
sys.exit(app.exec_())