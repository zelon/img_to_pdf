""" Run on python3
 First, Install imagemagick from http://www.imagemagick.org
"""

import argparse
import glob
import os
import sys

temp_filelist_filename = '__img_to_pdf_filelist.txt'
temp_label_filename = '__img_to_pdf_label.jpg'

def make_label_jpg(label, filename):
    cmd = 'magick -background white -fill black -size 600x800 -quality 100 -gravity Center -font D2Coding label:"[{}]" "{}"'.format(label, filename)
    print(cmd)
    os.system(cmd)


def make_pdf_from_filenamelist(filename_list, output_filename):
    quoted_filenames = ['"' + filename + '"' for filename in filename_list]
    f = open(temp_filelist_filename, 'w', encoding='utf-8')
    for filename in quoted_filenames:
        print(filename, file=f)
    f.close()

    cmd = 'magick @{} "{}.pdf"'.format(temp_filelist_filename, output_filename)
    print(cmd)
    os.system(cmd)


def filter_filename(filelist):
    result = []
    conditions = [".jpg", ".jpeg", ".png"]

    for filename in filelist:
        for condition in conditions:
            if os.path.splitext(filename.lower())[1] == condition:
                result.append(filename)
                break
    return result


def enumerate_by_total_size(filenames, limit_size_mb):
    if limit_size_mb == 0:
        return [filenames]
    list_of_list = []
    filename_list = []
    total_size = 0
    output_index = 0
    for filename in filenames:
        filesize = os.path.getsize(filename)
        filename_list.append(filename)
        total_size += filesize
        total_mb = total_size / 1024 / 1024
        if total_mb >= limit_size_mb:
            list_of_list.append(filename_list)
            filename_list = []
            total_size = 0
            output_index += 1

    if len(filename_list) > 0:
        list_of_list.append(filename_list)

    return list_of_list


def main(directory, output_filename, limit_size_mb):
    filenames = filter_filename(glob.glob(os.path.join(directory, "*.*")))

    filenamelist_of_list = enumerate_by_total_size(filenames, limit_size_mb)
    for i in range(len(filenamelist_of_list)):
        filename = "{} - ({} of {})".format(output_filename, i, len(filenamelist_of_list))
        if len(filenamelist_of_list) == 1:
            filename = "{}".format(output_filename)

        make_label_jpg(filename, temp_label_filename)
        make_pdf_from_filenamelist([temp_label_filename] + filenamelist_of_list[i], filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Images files to pdf file')
    parser.add_argument('directory', help='directory containing image files')
    parser.add_argument('-o', '--output', help='output pdf file name without .pdf', default='')
    parser.add_argument('-l', '--limit_size_mb', help='size by megabyte to split', type=int, default=0)

    args = parser.parse_args()

    directory = args.directory
    if not os.path.exists(directory):
        print("Cannot find directory:{}".format(directory))
        sys.exit(1)
    output_filename = os.path.basename(os.path.abspath(directory))
    if len(args.output) > 0:
        output_filename = args.output
    limit_size_mb = args.limit_size_mb

    print('Directory: {}'.format(directory))
    print('OutputFilename: {}.pdf'.format(output_filename))
    print('LimitSizeMB: {}'.format(limit_size_mb))

    main(directory, output_filename, limit_size_mb)
