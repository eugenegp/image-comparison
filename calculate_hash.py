#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from PIL import Image
import six
from pyemd import emd

import imagehash
import numpy as np


def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

"""
Demo of hashing
"""
def find_similar_images(userpaths, hashfunc = imagehash.average_hash):
    import os
    def is_image(filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
            f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif") or '.jpg' in f

    image_filenames = []
    for userpath in userpaths:
        image_filenames += [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    images = []
    hashes = []

    for img in sorted(image_filenames):
        try:
            hash = hashfunc(Image.open(img))
            print(img)
            print(hash)
            hashes.append(hash)
            images.append(img)
        except Exception as e:
            print('Problem:', e, 'with', img)

    base = hashes[0]
    i=0
    for hash in hashes:
        diff = hamming2(str(base), str(hash))
        first_histogram = np.array([0.0, 1.0])
        second_histogram = np.array([5.0, 3.0])
        distance_matrix = np.array([[0.0, 0.5],[0.5, 0.0]])
        emd(first_histogram, second_histogram, distance_matrix)

        print(images[i] + ': ' + str(diff) + ' - ' +  str(diff/len(str(base))))
        i = i + 1


if __name__ == '__main__':
    import sys, os
    def usage():
        sys.stderr.write("""SYNOPSIS: %s [ahash|phash|dhash|...] [<directory>]
Identifies similar images in the directory.
Method:
  ahash:      Average hash
  phash:      Perceptual hash
  dhash:      Difference hash
  whash-haar: Haar wavelet hash
  whash-db4:  Daubechies wavelet hash
(C) Johannes Buchner, 2013-2017
""" % sys.argv[0])
        sys.exit(1)

    hashmethod = sys.argv[1] if len(sys.argv) > 1 else usage()
    if hashmethod == 'ahash':
        hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
        hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
        hashfunc = imagehash.dhash
    elif hashmethod == 'whash-haar':
        hashfunc = imagehash.whash
    elif hashmethod == 'whash-db4':
        hashfunc = lambda img: imagehash.whash(img, mode='db4')
    else:
        usage()
    userpaths = sys.argv[2:] if len(sys.argv) > 2 else "."
    find_similar_images(userpaths=userpaths, hashfunc=hashfunc)
