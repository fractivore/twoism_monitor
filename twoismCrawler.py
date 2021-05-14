#!/usr/bin/python3

import requests, json, sys, os
import jsonIO
from bs4 import BeautifulSoup

def main():
    if "--jsonFilePath" in sys.argv or "-j" in sys.argv:
        local_data_base_path = sys.argv[sys.argv.index("--jsonFilePath") + 1]
    else:
        local_data_base_path = 'twoism_post_counts.json'
    
    post_threshold = 10

    url = 'https://www.twoism.org/forum/viewforum.php?f=2&sid=603a39aa00d97c8f3546fc10b38bb8f8'

    page = requests.get(url)

    soup = BeautifulSoup(page.content,'lxml')

    results = soup.body
    #print(results)

    contents = results.find('div',id='wrap').find(id='page-body').find_all(class_='forumbg')[1].find_all(class_='topics')[0].find_all(class_='row')
    #print("contents:",contents)

    posts_by_topic = {}



    for topic in contents:

       # print("topic:", topic.dl.dd.contents[0])
        posts_by_topic[topic.dl.a.string] = int(topic.dl.dd.contents[0])

    if json_file_exists(local_data_base_path):
        dict_from_json = jsonIO.importCacheFile(local_data_base_path)
    else:
        dict_from_json = posts_by_topic
    print("posts_by_topic:" , posts_by_topic)

    total_new_post_count = 0
    for topic_link in posts_by_topic:
        if topic_link in dict_from_json:
            total_new_post_count += posts_by_topic[topic_link] - dict_from_json[topic_link]

    #if total_new_post_count > post_threshold:
       # send_notification()
    jsonIO.exportCacheFile(local_data_base_path, posts_by_topic)
    print("total_new_post_count:", total_new_post_count)

def json_file_exists(json_file_path):
    #This function returns true if a json file exists at the path name
    # specified (the if statement evaluates to true in this case, and false otherwise)
    #  (note that os.path.isfile() and os.access() both return true or false)
    return os.path.isfile(json_file_path) and os.access(json_file_path, os.R_OK)


if __name__ == '__main__':
    main()
