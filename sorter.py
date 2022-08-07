import logging
from time import time

from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor


import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_documents(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))


def handle_archives(filename: Path, target_folder: Path):
    if filename.exists():
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / normalize(filename.name.replace('filename.suffix', ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
        except shutil.ReadError:
            print(f'This is not archive {filename}!')
            folder_for_file.rmdir()
            return None
        filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'The folder {folder} has not been deleted!')


def main(folder: Path):
    parser.scan(folder)

    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in parser.DOC_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'XLSX')
    for file in parser.XLS_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'XLS')
    for file in parser.PPTX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'PPTX')

    for file in parser.OTHER:
        handle_other(file, folder / 'OTHER')

    for file in parser.ARCHIVES:
        handle_archives(file, folder / 'archives')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def start():
    while True:
        folder_for_scan = input('Enter folder for scan: ')
        if folder_for_scan:
            folder_for_scan = Path(folder_for_scan)
            print(f'Start in folder {folder_for_scan.resolve()}')
            main(folder_for_scan.resolve())
            print('Successfully!')
        else:
            input('Press Enter to exit...')
            break


if __name__ == '__main__':
    start()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(message)s')
    time_start = time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(parser.scan, parser.FOLDERS)
        logging.info(f'Sorting time: {round(time() - time_start,4)} seconds')
