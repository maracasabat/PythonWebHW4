from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

from normalize import normalize


def get_extensions(filename: Path, scan_folder: Path) -> None:
    file_folder = filename.suffix[1:].upper()
    if filename.suffix in ['.jpg', '.png', '.jpeg', '.bmp', '.gif', 'svg']:
        return handle_folders(filename, scan_folder / 'images' / file_folder)
    if filename.suffix in ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma', '.m4a']:
        return handle_folders(filename, scan_folder / 'audio' / file_folder)
    if filename.suffix in ['.avi', '.mpg', '.mpeg', '.mkv', '.mov', '.flv', '.wmv', '.mp4', '.webm']:
        return handle_folders(filename, scan_folder / 'video' / file_folder)
    if filename.suffix in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.txt', '.rtf']:
        return handle_folders(filename, scan_folder / 'documents' / file_folder)
    if filename.suffix in ['.zip', '.tag', '.gz']:
        return handle_archives(filename, scan_folder / 'archives')
    else:
        return handle_folders(filename, scan_folder / 'other')


def handle_folders(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archives(filename: Path, target_folder: Path):
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


def handle_del_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'The folder {folder} has not been deleted!')


def scan(folder: Path) -> None:
    lists = sorted(folder.glob('**/*'))
    sorter(lists, folder)


def sorter(lists: list, folder: Path) -> None:
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(get_extensions, lists[::-1], [folder] * len(lists))


if __name__ == '__main__':
    scan(Path(input('Enter the path to the folder: ')))
    print('Done!')
