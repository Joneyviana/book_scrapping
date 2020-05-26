import fnmatch
import os
from send_mail import upload_email


def upload():
    for file in os.listdir('/home/joney/Downloads'):
        if fnmatch.fnmatch(file, '*.mobi'):
           upload_email('/home/joney/Downloads/'+file,file)

if __name__ == '__main__':
    upload()