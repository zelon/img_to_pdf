""" Run on python3
 First, Install imagemagick from http://www.imagemagick.org
"""

import argparse
import glob
import os
import sys

def make_label_jpg(label, filename):
    # -pointsize 100
    cmd = 'magick -background white -fill black -size 600x800 -gravity Center -font D2Coding label:"[{}]" "{}"'.format(label, filename)
    print(cmd)
    os.system(cmd)


def make_pdf_from_filenamelist(filename_list, output_filename):
    quoted_filenames = ['"' + filename + '"' for filename in filename_list]
    cmd = 'magick {} "{}.pdf"'.format(" ".join(quoted_filenames), output_filename)
    print(cmd)
    os.system(cmd)


def convert(filename_list, output_filename):
    label_filename = "label.jpg"
    make_label_jpg(output_filename, label_filename)
    make_pdf_from_filenamelist([label_filename] + filename_list, output_filename)


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
    if not os.path.exists(directory):
        print("Cannot find directory:{}".format(directory))
        sys.exit(1)
    filenames = filter_filename(glob.glob(os.path.join(directory, "*.*")))

    filenamelist_of_list = enumerate_by_total_size(filenames, limit_size_mb)
    for i in range(len(filenamelist_of_list)):
        filename = "{}-{}".format(output_filename, i)
        if len(filenamelist_of_list) == 1:
            filename = "{}".format(output_filename)
        convert(filenamelist_of_list[i], filename)


def print_usage_and_exit():
    exe_filename = os.path.basename(sys.argv[0])
    print("Usage: {} directory output_filename [limit_size_mb]".format(exe_filename))
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Images files to pdf file')
    parser.add_argument('directory', help='directory containing image files')
    parser.add_argument('-o', '--output', help='output pdf file name without .pdf', default='')
    parser.add_argument('-l', '--limit_size_mb', help='size by megabyte to split', type=int, default=0)

    """
    if len(sys.argv) != 4 and len(sys.argv) != 3 and len(sys.argv) != 2:
        print_usage_and_exit()

    directory = sys.argv[1]
    output_filename = directory
    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
    limit_size_mb = 0
    if len(sys.argv) >= 4:
        limit_size_mb = int(sys.argv[3])
    """

    args = parser.parse_args()

    directory = args.directory
    output_filename = directory
    if len(args.output) > 0:
        output_filename = args.output
    limit_size_mb = args.limit_size_mb

    main(directory, output_filename, limit_size_mb)
