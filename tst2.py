from ftplib import FTP
import os
def getFilelistFTP(ip,port,user, psw):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    files = []

    try:
        files = ftp.nlst()
    except ftp.error_perm as resp:
        if str(resp) == "550 No files found":
            print
            "No files in this directory"
        else:
            raise
    n=50
    for f in files:
        print (f)
        n=n-1
        if n==0: break


    ftp.close()


def download20Ftp(workFolder,ip,port,user,psw):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    files = []
    filenames = ftp.nlst()  # get filenames within the directory

    n=20
    for filename in filenames:
        local_filename = os.path.join(workFolder, filename)
        print(local_filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)

        file.close()
        try:
            ftp.delete(filename)
            print("file was deletd:",filename)
        except Exception:
            ftp.rmd(filename)
        n=n-1
        if n==0 :break
    ftp.quit()  #
ip= "192.168.201.45"
port= "21"
user = "dcontrol10m"
psw= "23d-CONTROL"
wdir= r"C:\Users\office22\Desktop\zmani\ftp"
getFilelistFTP(ip,port,user,psw)
download20Ftp(wdir,ip,port,user,psw)