from sys import argv
import queue


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
def discover(to_find):
    print(type(to_find))


if __name__ == '__main__':
    print_hi('PyCharm')
    if len(argv) == 1:
        print("Nincs mire nézni!")
        exit(2)
    else:
        print(argv)
        discover(argv[1:])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
