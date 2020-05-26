import os
import fnmatch

def remove_books():
    for file in os.listdir('/home/joney/Downloads'):
        if fnmatch.fnmatch(file, '*.mobi'):
           os.remove('/home/joney/Downloads/'+file)

if __name__ == '__main__':
    remove_books()