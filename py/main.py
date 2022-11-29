import sys
import importlib

DEFAULT_INPUT_DIR="../inputs"
DEFAULT_INPUT_FORMAT="{year}/day{day}.txt"

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Insufficient arguments")
        print(f"{sys.argv[0]} <YEAR> <DAY> <PART> [<INPUT_FILE>]")
        sys.exit()

    year = sys.argv[1]
    day = sys.argv[2]
    part = sys.argv[3]

    if len(sys.argv) == 5:
        input_file_path = sys.argv[4]
    else:
        input_file_path = DEFAULT_INPUT_DIR + "/" + DEFAULT_INPUT_FORMAT.format(
            year = year, day = day, part = part
        )

    module = importlib.import_module(f"{year}.day{day}")
    part_func = getattr(module, part)

    part_func(input_file_path)