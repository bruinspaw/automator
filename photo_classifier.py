"""图片自动分类器 Auto Photo Classifier

按照图片的拍摄设备和时间自动将文件进行移动, 在Windows中, 源目录和
目标目录不能含有冒号, 以管理员身份运行PowerShell, 并执行该程序
Sort and rename pictures according to the device and date time.
On Windows, the source and destination directories shouldn't
include colon(s); run PowerShell as adiminstrator, then execute
this program.

"""


import exifread
import os
import re
import random


def fetch_info(filename):
    """Fetch device name and date time."""

    try:
        with open(filename, 'rb') as f:
            tags = exifread.process_file(f)
		# replace characters of not number and letter
        device = re.sub('\W+', ' ', tags['Image Model'].printable)
        device = device.strip()
        device = re.sub(' ', '_', tags['Image Model'].printable)  
        time = tags['EXIF DateTimeOriginal'].printable
        return device, time
    except Exception as err:
        print('[Failed] Process %s .' % filename)
        print(str(err))
        return None, None


def create_directory(root, device, time):
    """Create directory to store photo"""

    dev_dir = os.path.join(root, device)
    if not os.path.exists(dev_dir):
        os.mkdir(dev_dir)

    time = re.split(r':| ', time)
    year_dir = os.path.join(dev_dir, str(time[0]))
    if not os.path.exists(year_dir):
        os.mkdir(year_dir)
    month_dir = os.path.join(year_dir, str(time[1]))
    if not os.path.exists(month_dir):
        os.mkdir(month_dir)

    return month_dir


def classify_photos(src_dir, dest_dir):
    """Classify photos by device and date

    Args:
        src_dir: directory holding photos before classification
        dest_dir: directory holding photos after classification
    """
    for root, sudirs, files in os.walk(src_dir, topdown=False):
        for file in files:
            if file.endswith('.jpeg') or file.endswith('.JPEG'):
                suffix = '.jpeg'
            elif file.endswith('.jpg') or file.endswith('.JPG'):
                suffix = '.jpg'
            else:     # skip
                continue

            try:
                old_path = os.path.join(root, file)
                print('Process %s' % old_path)
                device, time = fetch_info(old_path)
                if device and time:
                    subdir = create_directory(dest_dir, device, time)
                    new_name = (''.join(re.split(r':| ', time)) +
                                str(random.randint(10, 99)) + suffix)
                    new_path = os.path.join(subdir, new_name)
                    os.rename(old_path, new_path)
                    print('[OK] Move %s to %s .' % (old_path, new_path))
            except Exception as err:
                print('Failed on creating file or directory.')
                print(str(err))


if __name__ == '__main__':
    classify_photos(r'Unclassified', r'Classified')
