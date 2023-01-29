import os
import re
import argparse
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pydub import AudioSegment


def get_paper_name_from_arxiv(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('meta', {'name': 'citation_title'})['content']
    return title


def get_mp3_size_and_duration(path):
    file_size = os.path.getsize(path)
    song = AudioSegment.from_mp3(path)
    duration = len(song) / 1000
    minutes, seconds = divmod(duration, 60)
    duration_str = "{:02d}:{:02d}".format(int(minutes), int(seconds))
    return file_size, duration_str


def get_current_date():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    return current_date


def is_valid_date_format(date_string):
    date_format = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    if bool(date_format.match(date_string)):
        return date_string
    else:
        raise ValueError(f"{date_format} is not a valid yyyy-MM-dd date")


def run(number, link=None, paper=None, arxiv=None, date=None, title=None, overwrite=False):
    current_dir = os.getcwd()
    current_date = date or get_current_date()
    md_file_path = f'{current_dir}/_posts/{current_date}-e{number:02d}.md'
    mp3_file = f'e{number:02d}.mp3'
    mp3_file_path = f'{current_dir}/assets/audio/{mp3_file}'
    if not overwrite and os.path.exists(md_file_path):
        raise RuntimeError(f"Markdown file for episode {number} already exist. Use -o to overwrite it.")
    try:
        link = link or f"https://arxiv.org/abs/{arxiv}"
        paper = paper or get_paper_name_from_arxiv(link)
    except Exception as e:
        print(f'Failed to retrieve paper name from {link}. Got exception: {e}')
        paper = None
    try:
        mp3_file_size, duration = get_mp3_size_and_duration(mp3_file_path)
    except Exception as e:
        print(f'Failed to retrieve metadata of mp3 file {mp3_file_path}. Got exception: {e}')
        mp3_file_size, duration = None, None

    with open(md_file_path, 'w') as md:
        md.write('--- \n')
        md.write('layout: post \n')
        md.write(f'title: "{title}" \n')
        md.write(f'episode: {number} \n')
        md.write(f'paper: "{paper}" \n')
        md.write(f'audio: {mp3_file} \n')
        md.write(f'duration: "{duration}" \n')
        md.write(f'bytes: {mp3_file_size} \n')
        md.write(f'link: "{link}" \n')
        md.write('--- \n')
        md.write('\n')
        md.write('\n')
    print(f"Created new episode markdown file at {md_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', dest='number', required=True, type=int, help='Episode number [integer]')
    parser.add_argument('-l', '--link', dest='link', help='Paper URL')
    parser.add_argument('-x', '--arxiv', dest='arxiv', help='Paper arXiv ID')
    parser.add_argument('-p', '--paper', dest='paper', help='Paper name')
    parser.add_argument('-d', '--date', dest='date', type=is_valid_date_format,
                        help='Release date, must be formatted as yyyy-MM-dd')
    parser.add_argument('-t', '--title', dest='title', help='Episode title')
    parser.add_argument('-o', '--overwrite', dest='overwrite', default=False, action='store_true',
                        help='Overwrite MD file if exists (default: False)')
    args = parser.parse_args()
    run(**vars(args))
