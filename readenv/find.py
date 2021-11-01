import sys
from pathlib import Path
from queue import dekju


file_kju = dekju.Queue()
folder_kju = dekju.Queue()


def finder(itt, folder_kju):
    tart = itt.iterdir()

    for item in tart:
        if item.is_dir():
            folder_kju.enqueue(item)
        elif item.is_file():
            file_kju.enqueue(item)


def main(gpath):
    finder(Path(gpath), folder_kju)
    folder_kju.print_queue()
    print(folder_kju.length)
    actual = folder_kju.dequeue()

if __name__ == '__main__':
    main('h:/pd/fin_rep')
