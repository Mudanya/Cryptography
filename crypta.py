import ctypes
import hashlib
import os
import re
import sys
#connects to the UI
import pyperclip
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import cryptographer


class cryptor(QMainWindow):
    filename = None
    spanner = None
    receiver = None
    plain = None
    key = None

    def __init__(self):
        super(cryptor, self).__init__()
        loadUi('crypto.ui', self)
        self.setWindowTitle('crypto')
        self.open.clicked.connect(self.open_text)
        self.paste.clicked.connect(self.paste_text)
        self.save.clicked.connect(self.save_text)
        self.clear.clicked.connect(self.clear_text)
        self.encrypt.clicked.connect(self.enc_text)
        self.decrypt.clicked.connect(self.dec_text)
        self.file.clicked.connect(self.select_file)
        self.fclear.clicked.connect(self.clear_file)
        self.fencrypt.clicked.connect(self.enc_file)
        self.fdecrypt.clicked.connect(self.dec_file)

    def open_text(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', os.path.expanduser('~/Documents'))
        if fileName:
            try:
                with open(fileName, 'r+') as infile:
                    f = infile.read()
                    self.textpane.append(f)
            except:
                return None
        else:
            return None

    def paste_text(self):
        f = pyperclip.paste()
        self.textpane.append(f)

    def save_text(self):
        self.plain = self.textpane.toPlainText()
        if self.plain == '':
            QMessageBox.about(self, "Status", "No text to save.")
        else:
            self.saver()

    def saver(self):
        if self.plain is not None:
            filename, ok = QFileDialog.getSaveFileName(self, 'Save File', os.getenv(''))
            if ok:
                try:
                    file = open(filename, 'w')
                    file.write(self.plain)
                    file.close()
                    QMessageBox.about(self, "Status", "File saved successfully.")
                    self.cancel()
                except:
                    QMessageBox.about(self, "Status",
                                      "Failed! Could not save file.\nPlease retry using a different filename.")
                    self.cancel()
                    return None
            else:
                return None
        else:
            QMessageBox.about(self, "Error!",
                              "No text to Save!")
            self.cancel()
            return None

    def clear_text(self):
        beta = self.textpane.toPlainText()
        if beta != '':
            self.textpane.clear()
        else:
            QMessageBox.about(self, "Empty", "No text to clear")

        if ctypes.windll.user32.OpenClipboard(None):
            ctypes.windll.user32.EmptyClipboard()
            ctypes.windll.user32.CloseClipboard()

    def write_text_file(self, data):
        pdir = os.getcwd()
        outPut_file = pdir + "/temporary.txt"
        print(outPut_file)
        with open(outPut_file, "w") as out_file:
            # write bytes to file
            out_file.write(data)
            out_file.close()
        return outPut_file

    def enc_text(self):
        self.plain = self.textpane.toPlainText()
        if self.plain != '':
            outfile = self.write_text_file(self.plain)
            self.setEncryptPassword()
            self.key = hashlib.sha256(self.spanner.encode()).digest()
            print(outfile)
            cryptographer.Crypto.encryption(filename=outfile, keyfile=self.key)
            file_res = self.read_file(outfile + ".enc")
            xfile_res = int(file_res, 2).to_bytes((len(file_res) + 7) // 8, byteorder='big').decode("utf-8", "ignore")
            self.textpane.clear()
            self.textpane.append(xfile_res)
        else:
            QMessageBox.about(self, "Encryption Status", "Nothing to Encrypt")

    def dec_text(self):
        pwdir = os.getcwd()
        input_file = pwdir + "/temporary.txt.enc"
        # self.plain = self.read_file(input_file)
        if input_file != '':
            text, ok = QInputDialog.getText(self, "Password",
                                            "Kindly enter the decryption password:", QLineEdit.Password, "")
            if text != '':
                if ok:
                    self.spanner = text
                    init = hashlib.sha256(self.spanner.encode()).digest()
                    cryptographer.Crypto.decryption(filename=input_file, keyfile=init)
                    self.spanner = None
                    ntemporary_file = pwdir + "/temporary.txt"
                    results = self.read_file(ntemporary_file)
                    self.textpane.clear()
                    self.textpane.append(results)
                    os.remove(ntemporary_file)

                else:
                    return None
            else:
                if ok:
                    self.dec_text()
                else:
                    return None
        else:
            QMessageBox.about(self, "Encryption Status", "Nothing to Decrypt")

    def clear_file(self):
        alpha = self.fpath.text()
        if alpha != '':
            self.fpath.clear()
        else:
            QMessageBox.about(self, "Empty", "No text to clear")

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select File', os.path.expanduser('~/Documents'))
        if fileName:
            try:
                self.filename = fileName
                self.fpath.setText(fileName)
            except:
                return None

    def read_file(self, outfile):
        filename = outfile
        with open(filename, "r") as infile:
            file = infile.read()
        return file

    def enc_file(self):
        if self.filename:
            self.setEncryptPassword()
            self.fileEncrypt()
            QMessageBox.about(self, "Status", "File Encrypted and \nSaved Successfully")
        else:
            QMessageBox.about(self, "Status", "No File to Encrypt")
            self.cancel()

    def fileEncrypt(self):
        if self.filename is None:
            return None
        else:
            if ".enc" not in self.filename:

                self.filename = os.path.join(self.filename)

                self.key = hashlib.sha256(self.spanner.encode()).digest()
                # self.key = self.spanner.encode()
                print(self.key)
                keyfile = self.key
                filename = self.filename
                cryptographer.Crypto.encryption(filename=filename, keyfile=keyfile)
                self.filename = self.filename + '.enc'
                self.fpath.setText(self.filename)
            else:
                QMessageBox.about(self, "Status", "File already encrypted")

    def dec_file(self):

        if self.filename is None:
            return None
        else:
            self.filename = os.path.join(self.filename)
            filename = self.filename
            text, ok = QInputDialog.getText(self, "Password", "Kindly enter the decryption password:",
                                            QLineEdit.Password, "")
            if text != '':
                if ok:
                    if ".enc" in self.filename:
                        self.spanner = text
                        keyfile = hashlib.sha256(self.spanner.encode()).digest()
                        # keyfile = self.spanner.encode()
                        print(filename)
                        print(keyfile)
                        # y =  bin(int.from_bytes(keyfile, 'big'))
                        # print(y)
                        cryptographer.Crypto.decryption(filename=filename, keyfile=keyfile)
                        self.spanner = None
                        QMessageBox.about(self, "Status", "File Decrypted and \nSaved Successfully")
                    else:
                        QMessageBox.about(self, "Decryption Status", "Already in plain text")

                else:
                    return None
            else:
                if ok:
                    self.dec_file()
                else:
                    return None

    def cancel(self):
        self.filename = None

    def setEncryptPassword(self):
        text, ok = QInputDialog.getText(self, "Password",
                                        "Kindly enter the encryption password:", QLineEdit.Password, "")
        if text != '':
            if ok:
                flag = 0
                while True:
                    if (len(text) < 8):
                        flag = -1
                        break
                    elif not re.search("[a-z]", text):
                        flag = -1
                        break
                    elif not re.search("[A-Z]", text):
                        flag = -1
                        break
                    elif not re.search("[0-9]", text):
                        flag = -1
                        break
                    elif not re.search("[_@$!#%^&*-=+()}{?']", text):
                        flag = -1
                        break
                    elif re.search("\s", text):
                        flag = -1
                        break
                    else:
                        flag = 0
                        self.spanner = text
                        self.confirmPassword()

                        break

                if flag == -1:
                    QMessageBox.about(self, "Weak password",
                                      "Password should contain:\n-Atleast 8 Characters\n-Uppercase\n-Lowercase\n-Numerals &\n-Special Characters")
                    self.setEncryptPassword()
            else:
                return None
        else:
            if ok:
                self.setEncryptPassword()
            else:
                return None

    def confirmPassword(self):
        text, ok = QInputDialog.getText(self, "Confirmation",
                                        "Kindly Re-enter the encryption password:", QLineEdit.Password, "")
        if text != '':
            if ok:
                nut = text
                if nut == self.spanner:
                    self.spanner = nut

                else:
                    QMessageBox.about(self, "Miss-Match", "Password do not match \n Please re-enter")
                    self.setEncryptPassword()
            else:
                pass

        else:
            if ok:
                QMessageBox.about(self, "Error", "Password not confirmed")
                self.setEncryptPassword()
            else:
                pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('images.ico'))
    window = cryptor()
    window.setWindowTitle('crypto')
    window.show()
    sys.exit(app.exec_())
