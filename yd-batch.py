#!/usr/bin/python

import sys
import os
import urlparse
import glob
from pyscheduler.processParallelScheduler import ProcessParallelScheduler
from pyscheduler.serialScheduler import SerialScheduler
from optparse import OptionParser

Y2MP3 = "youtube-dl %s -x --audio-format mp3 --audio-quality 0"


def get_video_id(url):
    url_data = urlparse.urlparse(url)
    video_id = urlparse.parse_qs(url_data.query)["v"][0]
    return video_id


def parse_line(line):
    parts = line.strip().split()
    url = parts[0]
    if len(parts) == 1:
        name = None
    else:
        name = " ".join(parts[1:])
    return url, name


def check_and_rename_downloaded_file(video_id, new_name):
    the_file = glob.glob("*%s.mp3*" % video_id)
    if not the_file:
        return False
    else:
        if new_name is not None:
            os.rename(the_file[0], "%s.mp3" % new_name)
        return True


def simple_download(url, name):
    os.system(Y2MP3 % url)
    video_id = get_video_id(url)
    ok = check_and_rename_downloaded_file(video_id, name)
    if not ok:
        print "[ERROR] Impossible to download url."


def batch_download_task(url, name):
    video_id = get_video_id(url)
    # Get the music
    os.system(Y2MP3 % url)
    # Rename
    all_ok = check_and_rename_downloaded_file(video_id, name)
    return all_ok, url, name


def batch_download(batch_file_name, scheduler):
    # Open the file
    batch_file = open(batch_file_name, "r")

    # Process it!
    for line in batch_file:
        url, name = parse_line(line)

        scheduler.add_task(task_name=url,
                           dependencies=[],
                           description="",
                           target_function=batch_download_task,
                           function_kwargs={"url": url, "name": name})

    results = scheduler.run()

    not_downloaded = filter(lambda x: not x[0], results)

    if not_downloaded:
        open("not_downloaded.txt", "w").write("\n".join(["%s %s" % (nd[1], nd[2]) for nd in not_downloaded]))


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-n", dest="num_procs", default=1, type="int",
                      help="Number of simultaneous processes to use.")
    (options, args) = parser.parse_args()

    if not os.path.isfile(args[0]):
        # It may be a url, download it
        url = args[0]
        if len(args) > 1:
            name = " ".join(args[1:])
        else:
            name = None
        simple_download(url, name)
    else:
        # Try batch download
        if options.num_procs is not None or options.num_procs > 2:
            scheduler = ProcessParallelScheduler(options.num_procs)
        else:
            scheduler = SerialScheduler()

        try:
            batch_download(args[0], scheduler)
        except:
            print "[ERROR] Something went wrong when trying to download the urls from batch file."

