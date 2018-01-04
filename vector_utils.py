'''
Vector Utils

Utils to read in vectors from txt, .bin, or .pkl.

Taken from Erik Bernhardsson
Source: https://github.com/erikbern/ann-presentation/blob/master/util.py
'''
import gzip
import struct
import cPickle

def _get_vectors(fn):
    if fn.endswith('.gz'):
        f = gzip.open(fn)
        fn = fn[:-3]

    else:
        f = open(fn)

    if fn.endswith('.bin'): # word2vec format
        words, size = (int(x) for x in f.readline().strip().split())

        t = 'f' * size

        while True:
            pos = f.tell()
            buf = f.read(1024)
            if buf == '' or buf == '\n': return
            i = buf.index(' ')
            word = buf[:i]
            f.seek(pos + i + 1)

            vec = struct.unpack(t, f.read(4 * size))

            yield word.lower(), vec

    elif fn.endswith('.txt'): # Assume simple text format
        for line in f:
            items = line.strip().split()
            yield items[0], [float(x) for x in items[1:]]

    elif fn.endswith('.pkl'): # Assume pickle (MNIST)
        i = 0
        for pics, labels in cPickle.load(f):
            for pic in pics:
                yield i, pic
                i += 1


def get_vectors(fn, n=float('inf')):
    i = 0
    for line in _get_vectors(fn):
        yield line
        i += 1
        if i >= n:
            break