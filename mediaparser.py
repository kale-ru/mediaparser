# -*- coding: utf-8 -*-

import os
import shutil


class FileName:
    @staticmethod
    def is_file(filename):
        return os.path.isfile(filename) or os.path.islink(filename)

    @staticmethod
    def without_ext(filename):
        posdot = filename.rfind('.')
        return filename if posdot == -1 else filename[:posdot]

    @staticmethod
    def replace_ext(filename, new_ext):
        return FileName.without_ext(filename) + new_ext


class MediaFile:
    def __init__(self, mediafile_fullname):
        self.mediafile_fullname = mediafile_fullname
        self.descfile_fullname = self.mediafile_fullname+'.dsc'
        self.coverfile_fullname = ''
        self.category = set()
        self.title = ''
        self.description = ''

    def __str__(self):
        return self.mediafile_fullname


class Parser:
    def __init__(self):
        self.source_path = os.path.expanduser("~/Видео/Cinema")
        self.dlna_path = os.path.expanduser("~/Видео/DLNA")
        self.configfile_fullname = os.path.expanduser('~/.mediaparser')
        self.mediafile_ext = ('.avi', '.mkv')
        self.category = set()
        self.mediafiles = []

    def parse(self):
        self.mediafiles = []
        self.category = set()
        for dirpaths, dirnames, filenames in os.walk(self.source_path):
            for filename in filenames:
                if filename.endswith(self.mediafile_ext):
                    mediafile = MediaFile(os.path.join(dirpaths, filename))
                    self.mediafiles.append(mediafile)
                    if(len(mediafile.category) == 0):
                        self.category.add(u'Без категории')
                    else:
                        self.category.union(mediafile.category)
        try:
            shutil.rmtree(self.dlna_path)
        except Exception, e:
            print e

        for item in self.category:
            os.makedirs(self.dlna_path+u'/По категориям/'+item, mode=0777)

        for mfile in self.mediafiles:
            for i_category in mfile.category:
                os.symlink(mfile.mediafile_fullname, mfile.title,
                           self.dlna_path+'/'+i_category)
                if(FileName.is_file(mfile.coverfile_fullname)):
                    os.symlink(
                        mfile.coverfile_fullname, mfile.title,
                        self.dlna_path+'/'+i_category)

    def __str__(self):
        return 'Media files count:'+str(len(self.mediafiles))

parser = Parser()
parser.parse()
print parser
