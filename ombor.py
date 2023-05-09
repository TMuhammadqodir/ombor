import sys
import mysql.connector
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from pyqtdesign import *

class Ombor(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.dbConnection()
        self.createTable()
        self.ui.pushButton.clicked.connect(self.addproduct)
        self.ui.pushButton_4.clicked.connect(self.delproduct)
        self.ui.lineEdit_4.textChanged.connect(self.changetext)
        self.changetext()
        
    def addproduct(self):
        if len(self.ui.lineEdit.text())>0 and len(self.ui.lineEdit_3.text())>0 and len(self.ui.lineEdit_2.text()):
            try:
                with self.connect.cursor() as cursor:
                    cursor.execute(f"""insert into ombor(name,price,amount) values("{self.ui.lineEdit.text()}","{self.ui.lineEdit_3.text()}","{self.ui.lineEdit_2.text()}")""")
            except Exception as err: print(err)
            else: 
                print('ok')
                self.connect.commit()
                self.changetext()
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit_3.clear()
            
    def delproduct(self):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(f"DELETE FROM ombor where name='{self.ui.lineEdit_5.text()}'")
                self.ui.lineEdit_5.setText('')
        except Exception as err: print(err)
        else: 
            self.connect.commit()
            print('ok')
            
    def changetext(self):
        try:
            with self.connect.cursor() as cursor:
                if self.ui.radioButton.isChecked():
                    cursor.execute(f"""select *from ombor where name like '{self.ui.lineEdit_4.text()}%';""")
                elif self.ui.radioButton_2.isChecked():
                    cursor.execute(f"""select *from ombor where price like '{self.ui.lineEdit_4.text()}%';""")
                elif self.ui.radioButton_3.isChecked():
                    cursor.execute(f"""select *from ombor where amount like '{self.ui.lineEdit_4.text()}%';""")  
                else:  
                    cursor.execute(f"select *from ombor;")
                temp=cursor.fetchall()
            row=0
            self.ui.tableWidget.setRowCount(len(temp))
            for i in range(len(temp)):
                self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(temp[i][1])))
                self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(temp[i][2])))
                self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(temp[i][3])))
                row+=1
        except Exception as err: print(err)
        else:
            print('ok') 
            
    def dbConnection(self):
        try:
            self.connect=mysql.connector.connect(
                host="localhost",
                database="ombordb",
                user="root",
                password="root"
            )
        except Exception as err: print(err)
        else: print('ok')
        
    def createTable(self):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute("""Create table if not exists ombor(
                    id int auto_increment primary key,
                    name varchar(32) not null,
                    price varchar(100) not null,
                    amount varchar(100) not null
                    );""")
        except Exception as err: print(err)
        else: print('ok')
        
app=QApplication([])
win=Ombor()
win.show()
sys.exit(app.exec_())
        