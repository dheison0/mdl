import subprocess
from os import chdir, mkdir
from sys import argv
from bs4 import BeautifulSoup
from typing import List
from requests import get
from dataclasses import dataclass


@dataclass
class FolderItem:
    # folder or file
    type_: str
    name: str
    id: str

@dataclass
class File:
    name: str
    url: str


def get_file(id: str) -> File:
    page = get(f"https://www.mediafire.com/file/{id}")
    html = BeautifulSoup(page.text, "html.parser")
    name = html.find("div", attrs={'class': "filename"}).getText(strip=True)
    url = html.find("a", attrs={'id': "downloadButton"}).get("href")
    return File(name, url)


def get_folder_items(id: str) -> List[FolderItem]:
    items = []
    default_params = {
        'filter': "all",
        'version': 1.5,
        'folder_key': id,
        'response_format': "json"
    }
    file_data = get(
        "https://www.mediafire.com/api/1.4/folder/get_content.php",
        params={'content_type':  "files", **default_params}
    ).json()
    folder_data = get(
        "https://www.mediafire.com/api/1.4/folder/get_content.php",
        params={'content_type':  "folders", **default_params}
    ).json()
    file_list = file_data['response']['folder_content']['files']
    folder_list = folder_data['response']['folder_content']['folders']
    for file in file_list:
        items.append(FolderItem('file', file['filename'], file['quickkey']))
    for folder in folder_list:
        items.append(FolderItem('folder', folder['foldername'], folder['quickkey']))
    return items


def download_all(folder_id: str):
    folder_items = get_folder_items(folder_id)
    print("Downloading items...")
    for i in folder_items:
        if i.type_ == 'file':
            file = get_file(i.id)
            print(f"Downloading: {file.name}")
            exit_code = 1
            while exit_code > 0:
                d = subprocess.run([
                    'aria2c', '-s', 16, '-x', 16,
                    '-o', file.name,
                    file.url
                ])
                exit_code = d.returncode
        else:
            print(f"Creating folder {i.name}...")
            try: mkdir(i.name)
            except: pass
            chdir(i.name)
            download_all(i.id)
            print("Going back to old folder...")
            chdir('..')


if __name__ == '__main__':
    if len(argv) > 1:
        download_all(argv[1])
    else:
        print(f'usage: {argv[0]} folder_id')