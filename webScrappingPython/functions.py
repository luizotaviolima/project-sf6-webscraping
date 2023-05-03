import requests
import pandas as pd
import os
import glob
from bs4 import BeautifulSoup


def site_content(url: str):
    response = requests.get(url)
    site_full_content = response.content
    return site_full_content


def site_target_content(site_full_content: bytes, tag: str, attrs: dict):
    siteContentParsed = BeautifulSoup(site_full_content, "html.parser")
    siteTargetContent = siteContentParsed.find(tag, attrs)
    return siteTargetContent


def get_web_info(site_target_content, tag):
    webInfo = site_target_content.find_all(tag)
    return webInfo


def get_character_link(html_content):
    characterLinkList = []
    for info in html_content:
        characterLink = info["href"]
        characterLinkList.append(characterLink)
    return characterLinkList


def char_detail_text(char_detail, tag: str, attrs: dict):
    charDetailText = char_detail.find_all(tag, attrs)
    return charDetailText


def dataframe(char_full_info, columns_name):
    df = pd.DataFrame([char_full_info], columns=columns_name)
    return df


def export_to_csv(dataframe, name):
    dataframe.to_csv(name + '.csv', index=False)


def work_directory():
    cwd = os.getcwd()
    currentFolderName = cwd.split('/')[-1]
    if currentFolderName == 'webScrappingPython':
        os.chdir('../')
    folderName = 'data/'
    dataPath = os.path.join(os.getcwd(), folderName)
    return dataPath


def clean_directory(work_directory):
    for csvFile in glob.glob(work_directory + '*.csv'):
        os.remove(csvFile)
