#!/usr/bin/env python3

""" Download photos from different pages of site platonphoto.com """

import os, re

def main():

    PHOTO_BASE_URL = "http://platonphoto.com/photos/"
    PHOTO_EXT = ".jpg"
    photos_full_url = []    # list of photo direct urls

    # list of pages with photos
    files = [
        "http://www.platonphoto.com/gallery/portraits/politics/barackobama/",
        "http://www.platonphoto.com/gallery/portraits/movies--television/georgeclooney/",
        "http://www.platonphoto.com/gallery/portraits/music/tonybennet/",
        "http://www.platonphoto.com/gallery/portraits/sport/serenawilliams/",
        "http://www.platonphoto.com/gallery/portraits/business--technology/edwardsnowden/",
        "http://www.platonphoto.com/gallery/portraits/arts/tomwolfe/"
    ]

    # fill photos_full_url with direct photo urls
    for photofile in files:
        # get web page content
        # 'wget' saves it to file 'index.html'
        req = "wget {}".format(photofile)
        os.system(req)

        # read data of 'index.html'
        fp = open("index.html")
        filedata = fp.read()
        fp.close()

        # remove index.html
        os.system("rm index.html")

        # fetch clean names of photos like "7248-21-c.jpg"
        photos = re.findall("/photos/(\d{1,2}-\d{3,4})-c\.jpg", filedata)

        # add direct url to the list
        for photo in photos:
            url = PHOTO_BASE_URL + photo + PHOTO_EXT
            photos_full_url.append(url)

    # download photos to "photos" dir
    for photo in photos_full_url:
        req = "wget -P photos {}".format(photo)
        os.system(req)

if __name__ == '__main__':
    main()
