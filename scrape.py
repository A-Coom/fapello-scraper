from scraping_utils.scraping_utils import compute_file_hashes, download_urls
from sys import stdout, argv
import requests
import time
import os
import re


"""
Driver function to download all media from a model on Fapello
"""
def main(url, dst):
     # Sanitize the URL
    url = 'https://www.' + re.sub('(www\.)|(https?://)', '', url)
    if(url[-1] == '/'):
        url = url[:-1]

    # Get the amount of media for the model
    response = requests.get(url, headers={'Accept': 'application/json'})
    content = re.sub('\s', '', response.text)
    cnt = int(re.findall('[0-9]+', re.findall('[0-9]+<.*>Media', content)[-1])[0]) + 20

    # Get the base URL for media
    name = url.split('/')[-1]
    url = 'https://www.fapello.com/content/' + \
           name[0] + '/' + name[1] + '/' + name + \
           '/1000/' + name + '_'  #+ '0399.jpg'
    stdout.write('[main] INFO: Found %d media for %s.\n' % (cnt, name))

    # Create a list of all possible images and videos for the model
    stdout.write('[main] INFO: Creating links for all possible videos and images...\n')
    media = []
    for i in range(1, cnt + 1):
        media.append('%s%04d.jpg' % (url, i))
        media.append('%s%04d.mp4' % (url, i))

    stdout.write('[main] INFO: Trying %d download links...\n' % (len(media)))
    download_urls(dst, media)
    stdout.write('[main] INFO: Done.\n')


"""
Entry point
"""
if(__name__ == '__main__'):
    stdout.write('\n')
    if(len(argv) != 3):
        stdout.write('USAGE: %s <url> <download_dir>\n' % (argv[0]))
    else:
        if(not os.path.isdir(argv[2])):
            os.mkdir(argv[2])
        main(argv[1], argv[2])
    stdout.write('\n')
