import ftplib

def main():
    backup_folder = '/home/linu/Escritorio/backup'
    backup_name = 'zipper.zip'
   
 
    #user_name = 'whoever'
    host_ = '192.168.1.41'

    try:
        import ftplib
        host = host_
        ftp = ftplib.FTP(host)
        ftp.login()
        stat_info = ftp.sendcmd("STAT")
        
        print(stat_info)
        ftp.retrlines('LIST')
        ftp.cwd("upload")

        with open(backup_name,"rb") as f:
            ftp.storbinary(f'STOR {backup_name}', f)

        ftp.quit()
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()
