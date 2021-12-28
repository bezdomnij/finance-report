from pathlib import Path

from own_queue import dekju

file_kju = dekju.Queue()
folder_kju = dekju.Queue()


def finder(itt, kju):
    tart = itt.iterdir()

    for item in tart:
        if item.is_dir():
            kju.enqueue(item)
        elif item.is_file():
            file_kju.enqueue(item)


def main(gpath):
    finder(Path(gpath), folder_kju)
    folder_kju.print_queue()
    print(folder_kju.length)
    actual = folder_kju.dequeue()
    print(actual)


if __name__ == '__main__':
    main('h:/pd/fin_rep')
