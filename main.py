import sys
from m.fdec import *
from m.fenc import *

if __name__ == "__main__":
    if len(sys.argv) < 4 or ("-i" not in sys.argv and "-x" not in sys.argv):
        print("사용법: [프로그램] (-i|-x) [입력 파일/폴더] [텍스트 파일/출력 폴더]")
        sys.exit(1)

    if "-i" in sys.argv:
        input_file_index = sys.argv.index("-i")
        if len(sys.argv) != input_file_index + 4:
            print("사용법: [프로그램] -i [입력 파일] [텍스트 파일] [출력 폴더]")
            sys.exit(1)
        input_file_path = sys.argv[input_file_index + 1]
        new_data_file_path = sys.argv[input_file_index + 2]
        output_folder = sys.argv[input_file_index + 3]
        main(input_file_path, new_data_file_path, output_folder)

    if "-x" in sys.argv:
        input_folder_index = sys.argv.index("-x")
        if len(sys.argv) != input_folder_index + 3:
            print("사용법: -x [폴더] [출력 폴더]")
            sys.exit(1)
        input_folder = sys.argv[input_folder_index + 1]
        output_folder = sys.argv[input_folder_index + 2]
        decrypt_data(input_folder, output_folder)