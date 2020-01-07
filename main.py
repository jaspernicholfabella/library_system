import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from sqlalchemy import asc
from fpdf import FPDF
from PIL import Image
import sqlconn as sqc
import shutil
from collections import OrderedDict
import datetime
import os
from pytz import timezone
global settings_account_table
ui, _ = loadUiType('library.ui')
accounts_ui, _ = loadUiType('admin.ui')
info_ui, _ = loadUiType('info.ui')

class Accounts_Dialogue(QDialog,accounts_ui):
    edit_id = 0
    operationType = ''

    def __init__(self,parent=None):
        super(Accounts_Dialogue,self).__init__(parent)
        self.setupUi(self)

    def ShowDialogue(self,id,username,password,operationType=''):
        self.username.setText(username)
        self.password.setText(password)
        self.edit_id = id
        self.operationType = operationType
        self.buttonBox.accepted.connect(self.ok_button)

    def ok_button(self):
        engine = sqc.Database().engine
        library_admin = sqc.Database().library_admin
        conn = engine.connect()

        if self.operationType == 'edit':
            self.account_label.setText('Edit Account')
            s = library_admin.update().where(library_admin.c.userid == self.edit_id).\
                values(username = self.username.text(),
                       password = self.password.text())
            conn.execute(s)
            self.show_settings()

        elif self.operationType == 'add':
            self.account_label.setText('Add Account')
            s = library_admin.insert().values(
                username=self.username.text(),
                password=self.password.text())
            conn.execute(s)
            self.show_settings()
        conn.close()

    def show_settings(self):
        global settings_account_table
        settings_account_table.setRowCount(0)
        engine = sqc.Database().engine
        library_admin = sqc.Database().library_admin
        conn= engine.connect()
        #admin_table
        s = library_admin.select().order_by(asc(library_admin.c.username))
        s_value = conn.execute(s)
        table = settings_account_table
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))
        conn.close()

class Info_Dialogue(QDialog,info_ui):
    edit_id = 0
    infoType = ''
    operationType = ''

    def __init__(self,parent=None):
        super(Info_Dialogue,self).__init__(parent)
        self.setupUi(self)

    def ShowDialogue(self,id,infoType='',operationType = 'view'):
        self.edit_id = id
        self.infoType = infoType
        self.operationType = operationType
        self.show_values()
        self.info_ok_button.clicked.connect(self.info_ok_button_action)
        self.info_cancel_button.clicked.connect(self.info_cancel_button_action)

    def show_values(self):
        self.tabWidget.tabBar().setVisible(False)
        engine = sqc.Database().engine
        conn = engine.connect()

        if self.infoType == 'govpub':
            self.tabWidget.setCurrentIndex(0)
            library = sqc.Database().library_publication
            s = library.select().where(library.c.pubid == self.edit_id)
            s_value = conn.execute(s)
            for val in s_value:
                self.govpub_title.setText(val[4])
                self.govpub_ordinance_num.setText(str(val[3]))
                self.govpub_ordinance.setText(val[2])
                self.govpub_author_list.setText(val[5])
                self.govpub_subject.setText(val[6])
                self.govpub_department.setText(val[7])
                self.govpub_place_issued.setText(val[8])
                self.govpub_date_issued.setText(str(val[9]))
                self.govpub_date_recieved.setText(str(val[10]))
                self.govpub_date_archived.setVisible(False)
                self.govpub_description.setPlainText(val[11])

        elif self.infoType == 'lochis':
            self.tabWidget.setCurrentIndex(1)
            library = sqc.Database().library_localhistory
            s = library.select().where(library.c.id == self.edit_id)
            s_value = conn.execute(s)
            for val in s_value:
                self.lochis_title.setText(val[4])
                self.lochis_source.setText(val[2])
                self.lochis_author_list.setText(val[5])
                self.lochis_pages.setText(str(val[3]))
                self.lochis_date_archived.setVisible(False)
                self.lochis_description.setPlainText(val[7])

        elif self.infoType == 'periodicals':
            self.tabWidget.setCurrentIndex(2)
            library = sqc.Database().library_periodicals
            s = library.select().where(library.c.id == self.edit_id)
            s_value = conn.execute(s)
            for val in s_value:
                self.periodicals_title.setText(val[2])
                self.periodicals_subject.setText(val[3])
                self.periodicals_author_list.setText(val[4])
                self.periodicals_volume.setText(val[5])
                self.periodicals_num.setText(str(val[6]))
                self.periodicals_issn.setText(val[7])
                self.periodicals_number_of_pages.setText(str(val[8]))
                self.periodicals_pubdate.setText(str(val[9]))
                self.periodicals_date_archived.setVisible(False)
                self.periodicals_description.setPlainText(val[10])

        elif self.infoType == 'audiobook':
            self.tabWidget.setCurrentIndex(3)
            library = sqc.Database().library_realia
            s = library.select().where(library.c.id == self.edit_id)
            s_value = conn.execute(s)
            for val in s_value:
                self.audiobook_title.setText(val[2])
                self.audiobook_subject.setText(val[3])
                self.audiobook_author_list.setText(val[7])
                self.audiobook_number_of_copies.setText(str(val[8]))
                self.audiobook_series.setText(val[10])
                self.audiobook_location.setText(val[9])
                self.audiobook_length.setText(str(val[4]))
                self.audiobook_width.setText(str(val[5]))
                self.audiobook_dimension.setText(val[6])
                self.audiobook_date_archived.setVisible(False)
                self.audiobook_description.setPlainText(val[11])


        if self.operationType == 'view':
            self.info_cancel_button.setVisible(False)
            self.govpub_title.setReadOnly(True)
            self.govpub_ordinance_num.setReadOnly(True)
            self.govpub_ordinance.setReadOnly(True)
            self.govpub_author_list.setReadOnly(True)
            self.govpub_subject.setReadOnly(True)
            self.govpub_department.setReadOnly(True)
            self.govpub_place_issued.setReadOnly(True)
            self.govpub_date_issued.setReadOnly(True)
            self.govpub_date_recieved.setReadOnly(True)
            self.govpub_date_archived.setReadOnly(True)
            self.govpub_description.setReadOnly(True)
            self.lochis_title.setReadOnly(True)
            self.lochis_source.setReadOnly(True)
            self.lochis_author_list.setReadOnly(True)
            self.lochis_pages.setReadOnly(True)
            self.lochis_date_archived.setReadOnly(True)
            self.lochis_description.setReadOnly(True)
            self.periodicals_title.setReadOnly(True)
            self.periodicals_subject.setReadOnly(True)
            self.periodicals_author_list.setReadOnly(True)
            self.periodicals_volume.setReadOnly(True)
            self.periodicals_num.setReadOnly(True)
            self.periodicals_issn.setReadOnly(True)
            self.periodicals_number_of_pages.setReadOnly(True)
            self.periodicals_pubdate.setReadOnly(True)
            self.periodicals_date_archived.setReadOnly(True)
            self.periodicals_description.setReadOnly(True)
            self.audiobook_title.setReadOnly(True)
            self.audiobook_subject.setReadOnly(True)
            self.audiobook_author_list.setReadOnly(True)
            self.audiobook_number_of_copies.setReadOnly(True)
            self.audiobook_series.setReadOnly(True)
            self.audiobook_location.setReadOnly(True)
            self.audiobook_length.setReadOnly(True)
            self.audiobook_width.setReadOnly(True)
            self.audiobook_dimension.setReadOnly(True)
            self.audiobook_date_archived.setReadOnly(True)
            self.audiobook_description.setReadOnly(True)







    def info_ok_button_action(self):
        if self.operationType == 'view':
            self.close()
        elif self.operationType == 'edit':
            pass

    def info_cancel_button_action(self):
        self.close()



    def ok_button(self):
        engine = sqc.Database().engine
        library_admin = sqc.Database().library_admin
        conn = engine.connect()

        if self.operationType == 'edit':
            self.account_label.setText('Edit Account')
            s = library_admin.update().where(library_admin.c.userid == self.edit_id).\
                values(username = self.username.text(),
                       password = self.password.text())
            conn.execute(s)
            self.show_settings()

        elif self.operationType == 'add':
            self.account_label.setText('Add Account')
            s = library_admin.insert().values(
                username=self.username.text(),
                password=self.password.text())
            conn.execute(s)
            self.show_settings()
        conn.close()

    def show_settings(self):
        global settings_account_table
        settings_account_table.setRowCount(0)
        engine = sqc.Database().engine
        library_admin = sqc.Database().library_admin
        conn= engine.connect()
        #admin_table
        s = library_admin.select().order_by(asc(library_admin.c.username))
        s_value = conn.execute(s)
        table = settings_account_table
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))
        conn.close()

class MainApp(QMainWindow, ui):
    pdfjs_drive = os.getcwd()
    PDFJS = 'file:///' + pdfjs_drive.replace('\\', '/') + '/pdfjs/web/viewer.html'
    PDF = ''
    PDF_NOIMAGE = 'file:///' + pdfjs_drive.replace('\\', '/') + '/pdfjs/web/sample.pdf'

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.show_settings()
        self.Handle_UI_Changes()
        self.Handle_Globals()
        self.Handle_Buttons()



    def Handle_Globals(self):
        global settings_account_table
        settings_account_table = self.settings_account_table

    def Handle_UI_Changes(self):
        ##first setup
        self.tabWidget.tabBar().setVisible(False)
        self.archive_web_engine.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (self.PDFJS, self.PDF)))
        self.tabWidget.setCurrentIndex(0)
        self.menu_widget.setVisible(False)
        self.library_tab.tabBar().setVisible(False)
        self.library_tab_refresh()
        ##settings
        self.settings_account_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.settings_account_table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.settings_account_table.setColumnHidden(0,True)

    def Handle_Buttons(self):
        self.home_admin_login.clicked.connect(self.home_admin_login_action)
        self.home_guest_login.clicked.connect(self.home_guest_login_action)
        self.login_back.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
        ##menu
        self.menu_logo.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
        self.menu_archive.clicked.connect(self.menu_archive_action)
        self.menu_library.clicked.connect(self.menu_library_action)
        self.menu_settings.clicked.connect(self.show_settings)
        self.menu_logout.clicked.connect(self.menu_logout_action)
        ##library
        self.library_govpub.clicked.connect(self.library_govpub_action)
        self.library_lochis.clicked.connect(self.library_lochis_action)
        self.library_periodicals.clicked.connect(self.library_periodicals_action)
        self.library_audiobook.clicked.connect(self.library_audiobook_action)
        ##library_sub
        self.govpub_cancel.clicked.connect(self.library_tab_refresh)
        self.lochis_cancel.clicked.connect(self.library_tab_refresh)
        self.periodicals_cancel.clicked.connect(self.library_tab_refresh)
        self.audiobook_cancel.clicked.connect(self.library_tab_refresh)
        #login
        self.login_button.clicked.connect(self.login_button_action)
        self.login_username.textChanged.connect(lambda: self.login_error_message.setText(''))
        self.login_password.textChanged.connect(lambda: self.login_error_message.setText(''))
        #settings
        self.settings_add_account.clicked.connect(self.settings_add_account_action)
        self.settings_edit_account.clicked.connect(lambda: self.settings_edit_account_action(self.settings_account_table))
        self.settings_delete_account.clicked.connect(lambda: self.settings_delete_account_action(self.settings_account_table))
        self.settings_edit_sharedrive.clicked.connect(self.settings_edit_sharedrive_action)
        #govpub
        self.govpub_upload.clicked.connect(self.govpub_upload_action)
        self.govpub_add_author.clicked.connect(self.govpub_add_author_action)
        self.govpub_save_button.clicked.connect(self.govpub_save_button_action)
        #lochis
        self.lochis_add_author.clicked.connect(self.lochis_add_author_action)
        self.lochis_save_button.clicked.connect(self.lochis_save_button_action)
        self.lochis_upload.clicked.connect(self.lochis_upload_action)
        #periodicals
        self.periodicals_add_author.clicked.connect(self.periodicals_add_author_action)
        self.periodicals_save_button.clicked.connect(self.periodicals_save_button_action)
        self.periodicals_upload.clicked.connect(self.periodicals_upload_action)
        #audiobook
        self.audiobook_add_author.clicked.connect(self.audiobook_add_author_action)
        self.audiobook_save_button.clicked.connect(self.audiobook_save_button_action)
        self.audiobook_upload.clicked.connect(self.audiobook_upload_action)
        #archive
        self.archive_options.currentTextChanged.connect(self.archive_options_action)
        self.archive_doclist.doubleClicked.connect(self.archive_doclist_action)
        self.archive_info.clicked.connect(self.archive_info_action)
        QtWebEngineWidgets.QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_download_request)

    def home_admin_login_action(self):
        self.login_username.setText('')
        self.login_password.setText('')
        self.login_error_message.setText('')
        self.tabWidget.setCurrentIndex(1)

    def home_guest_login_action(self):
        self.tabWidget.setCurrentIndex(2)
        self.menu_widget.setVisible(True)
        self.menu_library.setVisible(False)
        self.menu_settings.setVisible(False)
        self.archive_admin_widget.setVisible(False)
        self.home_welcome.setText('Welcome Guest!')
##LOGIN

    def login_button_action(self):
        username = self.login_username.text()
        password = self.login_password.text()

        engine = sqc.Database().engine
        library_admin = sqc.Database().library_admin
        conn = engine.connect()
        s = library_admin.select()
        s_value = conn.execute(s)

        for val in s_value:
            if str(username).lower() == str(val[1]).lower() and str(password).lower() == str(val[2]).lower():
                self.tabWidget.setCurrentIndex(2)
                self.menu_widget.setVisible(True)
                self.menu_library.setVisible(True)
                self.menu_settings.setVisible(True)
                self.archive_admin_widget.setVisible(True)
                self.home_welcome.setText('Welcome Admin!')

            else:
                self.login_username.setText('')
                self.login_password.setText('')
                self.login_error_message.setText('Wrong username or password!!')

        conn.close()

    def menu_logout_action(self):
        self.menu_widget.setVisible(False)
        self.tabWidget.setCurrentIndex(0)



    def menu_library_action(self):
        self.tabWidget.setCurrentIndex(4)
        self.library_tab_refresh()

    def library_tab_refresh(self):
        self.library_tab.setCurrentIndex(0)
        ##government publication clear data fields
        self.govpub_ordinance.setText('')
        self.govpub_ordinance_num.setText('0')
        self.govpub_title.setText('')
        self.govpub_author_list.clear()
        self.govpub_subject.setText('')
        self.govpub_department.setText('')
        self.govpub_place_issued.setText('')
        self.govpub_date_issued.setText('')
        self.govpub_date_recieved.setText('')
        self.govpub_description.setPlainText('')
        self.govpub_upload_list.clear()
        ##localhistory clear data fields
        self.lochis_title.setText('')
        self.lochis_source.setText('')
        self.lochis_author_list.clear()
        self.lochis_subject.setText('')
        self.lochis_pages.setText('')
        self.lochis_description.setPlainText('')
        self.lochis_upload_list.clear()
        ##periodicals clear data fields
        self.periodicals_title.setText('')
        self.periodicals_subject.setText('')
        self.periodicals_author_list.clear()
        self.periodicals_volume.setText('')
        self.periodicals_number.setText('0')
        self.periodicals_issn.setText('')
        self.periodicals_number_of_pages.setText('0')
        self.periodicals_pubdate.setText('')
        self.periodicals_description.setPlainText('')
        self.periodicals_upload_list.clear()
        ##audiobook clear data fields
        self.audiobook_title.setText('')
        self.audiobook_subject.setText('')
        self.audiobook_author_list.clear()
        self.audiobook_no_of_copies.setText('0')
        self.audiobook_series.setText('')
        self.audiobook_length.setText('0')
        self.audiobook_width.setText('0')
        self.audiobook_description.setPlainText('')
        self.audiobook_upload_list.clear()

    def library_govpub_action(self):
        self.library_tab_refresh()
        self.library_tab.setCurrentIndex(1)

    def library_lochis_action(self):
        self.library_tab_refresh()
        self.library_tab.setCurrentIndex(2)

    def library_periodicals_action(self):
        self.library_tab_refresh()
        self.library_tab.setCurrentIndex(3)

    def library_audiobook_action(self):
        self.library_tab_refresh()
        self.library_tab.setCurrentIndex(4)

    ##SETTINGS
    def show_settings(self):
        #accounts
        self.tabWidget.setCurrentIndex(5)
        self.settings_account_table.setRowCount(0)
        engine = sqc.Database().engine
        library_admin = sqc.Database().library_admin
        conn= engine.connect()
        s = library_admin.select().order_by(asc(library_admin.c.username))
        s_value = conn.execute(s)
        table = self.settings_account_table
        for val in s_value:
            row_position = table.rowCount()
            table.insertRow(row_position)
            table.setItem(row_position, 0, QTableWidgetItem(str(val[0])))
            table.setItem(row_position, 1, QTableWidgetItem(str(val[1])))
            table.setItem(row_position, 2, QTableWidgetItem(str(val[2])))
        #sharedrive
        library_sharedrive = sqc.Database().library_sharedrive
        s = library_sharedrive.select()
        s_value = conn.execute(s)
        for val in s_value:
            self.settings_sharedrive_loc.setText(str(val[1]))

    def settings_edit_account_action(self, table):
        try:
            r = table.currentRow()
            id = table.item(r, 0).text()
            username = table.item(r, 1).text()
            password = table.item(r, 2).text()
            ad = Accounts_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id, username, password, operationType='edit')
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Rows Selected')
            msg.setWindowTitle("Error")
            msg.exec_()

    def settings_add_account_action(self):
        try:
            ad = Accounts_Dialogue(self)
            ad.show()
            ad.ShowDialogue(id, '', '', operationType='add')
        except:
            pass

    def settings_delete_account_action(self, table):
        try:
            r = table.currentRow()
            id = table.item(r, 0).text()
            engine = sqc.Database().engine
            conn = engine.connect()
            library_admin = sqc.Database().library_admin
            s = library_admin.delete().where(library_admin.c.userid == id)
            conn.execute(s)
            conn.close()
            self.show_settings()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Rows Selected')
            msg.setWindowTitle("Error")
            msg.exec_()

    def settings_edit_sharedrive_action(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        engine = sqc.Database().engine
        conn = engine.connect()
        library_sharedrive = sqc.Database().library_sharedrive

        s = library_sharedrive.update().where(library_sharedrive.c.sdid == 1).\
            values(sharedrive = '{}/archive_data'.format(file))

        conn.execute(s)
        self.show_settings()

    ##govpub
    def govpub_add_author_action(self):
        item = QtWidgets.QListWidgetItem('---')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.govpub_author_list.addItem(item)

    govpub_upload_list_dictionary = {}
    def govpub_upload_action(self):
        self.govpub_upload_list_dictionary= {}
        self.govpub_upload_list.clear()
        self.govpub_upload_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_files, _ = QFileDialog.getOpenFileNames(self, "Open Images",
                                                      '',
                                                      "Image File (*.jpg *.png)", options=options)
        for image_file in image_files:
            temp = image_file.split('/')
            self.govpub_upload_list_dictionary.update({temp[len(temp) - 1]: image_file})
            self.govpub_upload_list.addItem(temp[len(temp) - 1])

    def govpub_save_button_action(self):
        if self.govpub_upload_list.count() > 0:
            if len(self.govpub_title.text()) > 1:
                dir = self.settings_sharedrive_loc.text()
                alias = str(self.govpub_title.text() + '_govpub').replace('-', '_').replace(' ', '_').lower()
                try:
                    os.makedirs(dir)
                except:
                    print('directory already exists.')

                ## ERROR MESSAGES
                error_message = ''
                is_insert_db = True
                try:
                    temp = float(self.govpub_ordinance_num.text())
                except:
                    is_insert_db = False
                    error_message = 'Ordinance Number should be number'

                try:
                    author_string = ''
                    if len(self.govpub_author_list) > 0:
                        for i in range(0,self.govpub_author_list.count()):
                            author_string += ', ' + self.govpub_author_list.item(i).text()
                    else:
                        is_insert_db = False
                        error_message = 'Add an Author'
                except:
                    is_insert_db = False
                    error_message = 'Add an Author'


                try:
                    date_issued = datetime.datetime.strptime(self.govpub_date_issued.text(),'%m/%d/%Y')
                    date_issued_utc = date_issued.replace(tzinfo=timezone('UTC'))
                except:
                    is_insert_db = False
                    error_message = 'Date Issued not in proper format/ value'

                try:
                    date_recieved = datetime.datetime.strptime(self.govpub_date_recieved.text(),'%m/%d/%Y')
                    date_recieved_utc = date_recieved.replace(tzinfo=timezone('UTC'))
                except:
                    is_insert_db = False
                    error_message = 'Date Recieved not in proper format / value'

                ##PDF CONVERSION
                if is_insert_db:
                    try:
                        pdf = FPDF()
                        for i in range(self.govpub_upload_list.count()):
                            imageFile = self.govpub_upload_list_dictionary[self.govpub_upload_list.item(i).text()]
                            cover = Image.open(imageFile)
                            width, height = cover.size
                            width, height = float(width * 0.264583), float(height * 0.264583)
                            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
                            orientation = 'P' if width < height else 'L'
                            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
                            pdf.add_page(orientation=orientation)
                            pdf.image(imageFile, 0, 0, width, height)

                        pdf.output(dir+'/'+alias+'.pdf',"F")
                    except:
                        is_insert_db = False
                        error_message = 'Pdf Conversion Failed'

                ##connection to the database
                if is_insert_db:
                    engine = sqc.Database().engine
                    conn = engine.connect()
                    library_publication = sqc.Database().library_publication
                    s = library_publication.select().where(library_publication.c.alias == alias)
                    s_value = conn.execute(s)
                    x = 0
                    for val in s_value:
                        x+=1
                    if x < 1:
                        ins = library_publication.insert().values(
                            alias = alias,
                            ordinance = self.govpub_ordinance.text(),
                            ordinanceno = self.govpub_ordinance_num.text(),
                            title = self.govpub_title.text(),
                            author = author_string,
                            subject = self.govpub_subject.text(),
                            department = self.govpub_department.text(),
                            placeissued = self.govpub_place_issued.text(),
                            dateissued = date_issued_utc,
                            daterecieved = date_recieved_utc,
                            description = self.govpub_description.toPlainText(),
                            datearchived = datetime.datetime.utcnow()
                        )
                        conn.execute(ins)
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Succesfully Inserted to the Dabase!")
                        msg.setInformativeText('Government Publication Updated')
                        msg.setWindowTitle("Success")
                        msg.exec_()
                        self.library_tab_refresh()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Document Name Error!")
                        msg.setInformativeText('Document Name Exists')
                        msg.setWindowTitle("Error")
                        msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Something Went Wrong!")
                    msg.setInformativeText(error_message)
                    msg.setWindowTitle("Error")
                    msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Add Title')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Uploads Yet')
            msg.setWindowTitle("Error")
            msg.exec_()

    ##lochis
    def lochis_add_author_action(self):
        item = QtWidgets.QListWidgetItem('---')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.lochis_author_list.addItem(item)

    lochis_upload_list_dictionary = {}
    def lochis_upload_action(self):
        self.lochis_upload_list_dictionary= {}
        self.lochis_upload_list.clear()
        self.lochis_upload_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_files, _ = QFileDialog.getOpenFileNames(self, "Open Images",
                                                      '',
                                                      "Image File (*.jpg *.png)", options=options)
        for image_file in image_files:
            temp = image_file.split('/')
            self.lochis_upload_list_dictionary.update({temp[len(temp) - 1]: image_file})
            self.lochis_upload_list.addItem(temp[len(temp) - 1])

    def lochis_save_button_action(self):
        if self.lochis_upload_list.count() > 0:
            if len(self.lochis_title.text()) > 1:
                dir = self.settings_sharedrive_loc.text()
                alias = str(self.lochis_title.text() + '_lochis').replace('-', '_').replace(' ', '_').lower()
                try:
                    os.makedirs(dir)
                except:
                    print('directory already exists.')

                ## ERROR MESSAGES
                error_message = ''
                is_insert_db = True
                try:
                    temp = float(self.lochis_pages.text())
                except:
                    is_insert_db = False
                    error_message = 'Pages should be number'

                try:
                    author_string = ''
                    if len(self.lochis_author_list) > 0:
                        for i in range(0,self.lochis_author_list.count()):
                            author_string += ', '+ self.lochis_author_list.item(i).text()
                    else:
                        is_insert_db = False
                        error_message = 'Add an Author'
                except:
                    is_insert_db = False
                    error_message = 'Add an Author'


                ##PDF CONVERSION
                if is_insert_db:
                    try:
                        pdf = FPDF()
                        for i in range(self.lochis_upload_list.count()):
                            imageFile = self.lochis_upload_list_dictionary[self.lochis_upload_list.item(i).text()]
                            cover = Image.open(imageFile)
                            width, height = cover.size
                            width, height = float(width * 0.264583), float(height * 0.264583)
                            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
                            orientation = 'P' if width < height else 'L'
                            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
                            pdf.add_page(orientation=orientation)
                            pdf.image(imageFile, 0, 0, width, height)

                        pdf.output(dir+'/'+alias+'.pdf',"F")
                    except:
                        is_insert_db = False
                        error_message = 'Pdf Conversion Failed'

                ##connection to the database
                if is_insert_db:
                    engine = sqc.Database().engine
                    conn = engine.connect()
                    library_localhistory = sqc.Database().library_localhistory
                    s = library_localhistory.select().where(library_localhistory.c.alias == alias)
                    s_value = conn.execute(s)
                    x = 0
                    for val in s_value:
                        x+=1
                    if x < 1:
                        ins = library_localhistory.insert().values(
                            alias = alias,
                            source = self.lochis_source.text(),
                            pages = self.lochis_pages.text(),
                            title = self.lochis_title.text(),
                            author = author_string,
                            subject = self.lochis_subject.text(),
                            description = self.lochis_description.toPlainText(),
                            datearchived = datetime.datetime.utcnow()
                        )
                        conn.execute(ins)
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Succesfully Inserted to the Dabase!")
                        msg.setInformativeText('Local History Updated')
                        msg.setWindowTitle("Success")
                        msg.exec_()
                        self.library_tab_refresh()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Document Name Error!")
                        msg.setInformativeText('Document Name Exists')
                        msg.setWindowTitle("Error")
                        msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Something Went Wrong!")
                    msg.setInformativeText(error_message)
                    msg.setWindowTitle("Error")
                    msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Add Title')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Uploads Yet')
            msg.setWindowTitle("Error")
            msg.exec_()

    ##periodicals
    def periodicals_add_author_action(self):
        item = QtWidgets.QListWidgetItem('---')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.periodicals_author_list.addItem(item)

    periodicals_upload_list_dictionary = {}
    def periodicals_upload_action(self):
        self.periodicals_upload_list_dictionary= {}
        self.periodicals_upload_list.clear()
        self.periodicals_upload_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_files, _ = QFileDialog.getOpenFileNames(self, "Open Images",
                                                      '',
                                                      "Image File (*.jpg *.png)", options=options)
        for image_file in image_files:
            temp = image_file.split('/')
            self.periodicals_upload_list_dictionary.update({temp[len(temp) - 1]: image_file})
            self.periodicals_upload_list.addItem(temp[len(temp) - 1])

    def periodicals_save_button_action(self):
        if self.periodicals_upload_list.count() > 0:
            if len(self.periodicals_title.text()) > 1:
                dir = self.settings_sharedrive_loc.text()
                alias = str(self.periodicals_title.text() + '_periodicals').replace('-', '_').replace(' ', '_').lower()
                try:
                    os.makedirs(dir)
                except:
                    print('directory already exists.')

                ## ERROR MESSAGES
                error_message = ''
                is_insert_db = True
                try:
                    temp = float(self.periodicals_number_of_pages.text())
                except:
                    is_insert_db = False
                    error_message = 'Number of Pages should be Integer'

                try:
                    author_string = ''
                    if len(self.periodicals_author_list) > 0:
                        for i in range(0,self.periodicals_author_list.count()):
                            author_string += ', ' + self.periodicals_author_list.item(i).text()
                    else:
                        is_insert_db = False
                        error_message = 'Add an Author'
                except:
                    is_insert_db = False
                    error_message = 'Add an Author'


                try:
                    periodicals_pubdate = datetime.datetime.strptime(self.periodicals_pubdate.text(),'%m/%d/%Y')
                    periodicals_pubdate_utc = periodicals_pubdate.replace(tzinfo=timezone('UTC'))
                except:
                    is_insert_db = False
                    error_message = 'Publication Date Wrong Format!'

                ##PDF CONVERSION
                if is_insert_db:
                    try:
                        pdf = FPDF()
                        for i in range(self.periodicals_upload_list.count()):
                            imageFile = self.periodicals_upload_list_dictionary[self.periodicals_upload_list.item(i).text()]
                            cover = Image.open(imageFile)
                            width, height = cover.size
                            width, height = float(width * 0.264583), float(height * 0.264583)
                            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
                            orientation = 'P' if width < height else 'L'
                            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
                            pdf.add_page(orientation=orientation)
                            pdf.image(imageFile, 0, 0, width, height)

                        pdf.output(dir+'/'+alias+'.pdf',"F")
                    except:
                        is_insert_db = False
                        error_message = 'Pdf Conversion Failed'

                ##connection to the database
                if is_insert_db:
                    engine = sqc.Database().engine
                    conn = engine.connect()
                    library_periodicals = sqc.Database().library_periodicals
                    s = library_periodicals.select().where(library_periodicals.c.alias == alias)
                    s_value = conn.execute(s)
                    x = 0
                    for val in s_value:
                        x+=1
                    if x < 1:
                        ins = library_periodicals.insert().values(
                            alias = alias,
                            title = self.periodicals_title.text(),
                            subject = self.periodicals_subject.text(),
                            author = author_string,
                            volume = self.periodicals_volume.text(),
                            periodiclano = self.periodicals_number.text(),
                            issn = self.periodicals_issn.text(),
                            noofpages = self.periodicals_number_of_pages.text(),
                            publicationdate = periodicals_pubdate_utc,
                            description = self.periodicals_description.toPlainText(),
                            datearchived = datetime.datetime.utcnow()
                        )
                        conn.execute(ins)
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Succesfully Inserted to the Dabase!")
                        msg.setInformativeText('Periodicals Updated')
                        msg.setWindowTitle("Success")
                        msg.exec_()
                        self.library_tab_refresh()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Document Name Error!")
                        msg.setInformativeText('Document Name Exists')
                        msg.setWindowTitle("Error")
                        msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Something Went Wrong!")
                    msg.setInformativeText(error_message)
                    msg.setWindowTitle("Error")
                    msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Add Title')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Uploads Yet')
            msg.setWindowTitle("Error")
            msg.exec_()

    ##REALIA
    def audiobook_add_author_action(self):
        item = QtWidgets.QListWidgetItem('---')
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.audiobook_author_list.addItem(item)

    audiobook_upload_list_dictionary = {}
    def audiobook_upload_action(self):
        self.audiobook_upload_list_dictionary= {}
        self.audiobook_upload_list.clear()
        self.audiobook_upload_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_files, _ = QFileDialog.getOpenFileNames(self, "Open Images",
                                                      '',
                                                      "Image File (*.jpg *.png)", options=options)
        for image_file in image_files:
            temp = image_file.split('/')
            self.audiobook_upload_list_dictionary.update({temp[len(temp) - 1]: image_file})
            self.audiobook_upload_list.addItem(temp[len(temp) - 1])

    def audiobook_save_button_action(self):
        if self.audiobook_upload_list.count() > 0:
            if len(self.audiobook_title.text()) > 1:
                dir = self.settings_sharedrive_loc.text()
                alias = str(self.audiobook_title.text() + '_realia').replace('-', '_').replace(' ', '_').lower()
                try:
                    os.makedirs(dir)
                except:
                    print('directory already exists.')

                ## ERROR MESSAGES
                error_message = ''
                is_insert_db = True

                try:
                    temp = float(self.audiobook_length.text())
                except:
                    is_insert_db = False
                    error_message = 'Length should be number!'

                try:
                    temp = float(self.audiobook_width.text())
                except:
                    is_insert_db = False
                    error_message = 'Width should be number'

                try:
                    author_string = ''
                    if len(self.audiobook_author_list) > 0:
                        for i in range(0,self.audiobook_author_list.count()):
                            author_string += ', ' + self.audiobook_author_list.item(i).text()
                    else:
                        is_insert_db = False
                        error_message = 'Add an Artist'
                except:
                    is_insert_db = False
                    error_message = 'Add an Artist'


                ##PDF CONVERSION
                if is_insert_db:
                    try:
                        pdf = FPDF()
                        for i in range(self.audiobook_upload_list.count()):
                            imageFile = self.audiobook_upload_list_dictionary[self.audiobook_upload_list.item(i).text()]
                            cover = Image.open(imageFile)
                            width, height = cover.size
                            width, height = float(width * 0.264583), float(height * 0.264583)
                            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
                            orientation = 'P' if width < height else 'L'
                            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
                            pdf.add_page(orientation=orientation)
                            pdf.image(imageFile, 0, 0, width, height)

                        pdf.output(dir+'/'+alias+'.pdf',"F")
                    except:
                        is_insert_db = False
                        error_message = 'Pdf Conversion Failed'

                ##connection to the database
                if is_insert_db:
                    engine = sqc.Database().engine
                    conn = engine.connect()
                    library_realia = sqc.Database().library_realia
                    s = library_realia.select().where(library_realia.c.alias == alias)
                    s_value = conn.execute(s)
                    x = 0
                    for val in s_value:
                        x+=1
                    if x < 1:
                        ins = library_realia.insert().values(
                            alias = alias,
                            title = self.audiobook_title.text(),
                            subject = self.audiobook_subject.text(),
                            length = self.audiobook_length.text(),
                            width = self.audiobook_width.text(),
                            dimension = self.audiobook_dimension.text(),
                            author = author_string,
                            noofcopies = self.audiobook_no_of_copies.text(),
                            location = self.audiobook_location.text(),
                            series = self.audiobook_series.text(),
                            description = self.govpub_description.toPlainText(),
                            datearchived = datetime.datetime.utcnow()
                        )
                        conn.execute(ins)
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Succesfully Inserted to the Dabase!")
                        msg.setInformativeText('REALIA Updated')
                        msg.setWindowTitle("Success")
                        msg.exec_()
                        self.library_tab_refresh()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Document Name Error!")
                        msg.setInformativeText('Document Name Exists')
                        msg.setWindowTitle("Error")
                        msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Something Went Wrong!")
                    msg.setInformativeText(error_message)
                    msg.setWindowTitle("Error")
                    msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Add Title')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No Uploads Yet')
            msg.setWindowTitle("Error")
            msg.exec_()

    ##Archive
    archive_govpub_dict = {}
    archive_lochis_dict = {}
    archive_periodicals_dict = {}
    archive_realia_dict = {}

    def archive_dictionary_refresh(self):
        engine = sqc.Database().engine
        conn = engine.connect()
        library = sqc.Database().library_publication
        s = library.select()
        s_value = conn.execute(s)
        for val in s_value:
            self.archive_govpub_dict.update({val[4]:
            {   'pubid' : val[0],
                'alias' : val[1],
                'ordinance' : val[2],
                'ordinanceno' : val[3],
                'author' : val[5],
                'subject' : val[6],
                'department': val[7],
                'placeissued' : val[8],
                'dateissued' : val[9],
                'daterecieved' : val[10],
                'description' : val[11],
                'datearchived': val[12]} })

        library = sqc.Database().library_localhistory
        s = library.select()
        s_value = conn.execute(s)
        for val in s_value:
            self.archive_lochis_dict.update({val[4]:
            {  'id' : val[0],
                'alias' : val[1],
                'source': val[2],
                'pages': val[3],
                'author' : val[5],
                'subject' : val[6],
                'description' : val[7],
                'datearchived' : val[8]} })

        library = sqc.Database().library_periodicals
        s = library.select()
        s_value = conn.execute(s)
        for val in s_value:
            self.archive_periodicals_dict.update({val[2]:
            {
            'id' : val[0],
            'alias' : val[1],
            'subject' : val[3],
            'author' : val[4],
            'volume' : val[5],
            'periodiclano' : val[6],
            'issn' : val[7],
            'noofpages' : val[8],
            'publicationdate' : val[9],
            'description' : val[10],
            'datearchived' : val[11]} })

        library = sqc.Database().library_realia
        s = library.select()
        s_value = conn.execute(s)
        for val in s_value:
            self.archive_realia_dict.update({val[2]:
            {
               'id' : val[0],
               'alias' : val[1],
               'subject' : val[3],
               'length' : val[4],
               'width' : val[5],
               'dimension' : val[6],
               'author' : val[7],
               'noofcopies' : val[8],
               'location' : val[9],
               'series' : val[10],
               'description' : val[11],
               'datearchived' : val[12]} })




    def menu_archive_action(self):
        self.tabWidget.setCurrentIndex(3)
        self.archive_dictionary_refresh()
        self.archive_doclist.clear()
        self.archive_options.setCurrentIndex(0)
        self.archive_web_engine.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (self.PDFJS, self.PDF)))

    def archive_options_action(self):
        self.archive_web_engine.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (self.PDFJS, self.PDF)))
        if self.archive_options.currentText() == 'Government Publication':
            self.archive_doclist.clear()
            for key in self.archive_govpub_dict.keys():
                self.archive_doclist.addItem(key)
        elif self.archive_options.currentText() == 'Local History':
            self.archive_doclist.clear()
            for key in self.archive_lochis_dict.keys():
                self.archive_doclist.addItem(key)
        elif self.archive_options.currentText() == 'Periodicals':
            self.archive_doclist.clear()
            for key in self.archive_periodicals_dict.keys():
                self.archive_doclist.addItem(key)
        elif self.archive_options.currentText() == 'REALIA':
            self.archive_doclist.clear()
            for key in self.archive_realia_dict.keys():
                self.archive_doclist.addItem(key)

    def archive_doclist_action(self):
        dir = self.settings_sharedrive_loc.text()
        if self.archive_options.currentText() == 'Government Publication':
            alias = self.archive_govpub_dict[self.archive_doclist.currentItem().text()]['alias']
        elif self.archive_options.currentText() == 'Local History':
            alias = self.archive_lochis_dict[self.archive_doclist.currentItem().text()]['alias']
        elif self.archive_options.currentText() == 'Periodicals':
            alias = self.archive_periodicals_dict[self.archive_doclist.currentItem().text()]['alias']
        elif self.archive_options.currentText() == 'REALIA':
            alias = self.archive_realia_dict[self.archive_doclist.currentItem().text()]['alias']

        path_to_pdf = os.path.abspath(dir+'\\'+alias+'.pdf')
        if os.path.exists(path_to_pdf):
            self.archive_web_engine.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (self.PDFJS, path_to_pdf)))
        else:
            self.archive_web_engine.load(QtCore.QUrl.fromUserInput('%s?file=%s' % (self.PDFJS, self.PDF_NOIMAGE)))

    def archive_info_action(self):
        try:
            if self.archive_options.currentText() == 'Government Publication':
                id = self.archive_govpub_dict[self.archive_doclist.currentItem().text()]['pubid']
                d = Info_Dialogue(self)
                d.show()
                d.ShowDialogue(int(id),'govpub', operationType='view')
            elif self.archive_options.currentText() == 'Local History':
                id = self.archive_lochis_dict[self.archive_doclist.currentItem().text()]['id']
                d = Info_Dialogue(self)
                d.show()
                d.ShowDialogue(int(id), 'lochis', operationType='view')
            elif self.archive_options.currentText() == 'Periodicals':
                id = self.archive_periodicals_dict[self.archive_doclist.currentItem().text()]['id']
                d = Info_Dialogue(self)
                d.show()
                d.ShowDialogue(int(id), 'periodicals', operationType='view')
            elif self.archive_options.currentText() == 'REALIA':
                id = self.archive_realia_dict[self.archive_doclist.currentItem().text()]['id']
                d = Info_Dialogue(self)
                d.show()
                d.ShowDialogue(int(id), 'audiobook', operationType='view')
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Something Went Wrong!")
            msg.setInformativeText('No Selection Made')
            msg.setWindowTitle("Error")
            msg.exec_()






    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def on_download_request(self,download):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "sample.pdf", "*.pdf")
        if path:
            download.setPath(path)
            download.accept()



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()