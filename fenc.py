import struct
import os
import sys

# 데이터를 암호화하는 함수
def encrypt_data(data, key):
    message_bytes = data.encode('utf-16-le')
    encrypted_bytes = []
    for i, byte in enumerate(message_bytes):
        if i % 2 == 0:
            # 암호화
            encrypted_byte = byte ^ key
        else:
            # 그대로 유지
            encrypted_byte = byte
        encrypted_bytes.append(encrypted_byte)
    return bytes(encrypted_bytes)

def main(input_file_path, new_data_file_path, output_folder):
    try:
        with open(input_file_path, 'rb') as input_file:
            input_filename = os.path.basename(input_file_path)
            #output_file_path = os.path.join(output_folder, input_filename + '.a0')
            output_file_path = os.path.join(output_folder, input_filename)
            
            with open(output_file_path, 'wb') as output_file:
                with open(new_data_file_path, 'r', encoding='utf-8') as new_data_file:
                    while True:
                        # 데이터 구조 읽기
                        data_length_bytes = input_file.read(4)
                        if not data_length_bytes:
                            break  # 파일의 끝에 도달하면 종료

                        data_length = struct.unpack('<I', data_length_bytes)[0]
                        data_type = struct.unpack('B', input_file.read(1))[0]

                        if data_type == 0x54:
                            unk1 = struct.unpack('<I', input_file.read(4))[0]
                            xor_key = struct.unpack('<I', input_file.read(4))[0]
                            # 데이터 읽기
                            data = input_file.read(data_length - 9 - 4)

                            # new_data를 파일에서 읽어오기
                            new_data = new_data_file.readline()
                            #print(f"New Data: {new_data}")  # 디버깅용

                            # 데이터를 UTF-16 LE로 인코딩하고 바이트로 변환
                            new_data_bytes = new_data.encode('utf-16-le')
                            # 데이터 뒤에 0x0a00 바이트 추가
                            #new_data_bytes += b'\x0a\x00'
                            # 암호화
                            data = encrypt_data(new_data_bytes.decode('utf-16-le'), xor_key)
                            unk2 = struct.unpack('<I', input_file.read(4))[0]

                            # 쓰기
                            output_file.write(struct.pack('<I', len(data) + 9 + 4))
                            output_file.write(struct.pack('B', data_type))
                            output_file.write(struct.pack('<I', unk1))
                            output_file.write(struct.pack('<I', xor_key))
                            output_file.write(data)
                            output_file.write(struct.pack('<I', unk2))
                        elif data_type != 0x54:
                            data = input_file.read(data_length - 1)

                            # 쓰기
                            output_file.write(struct.pack('<I', data_length))
                            output_file.write(struct.pack('B', data_type))
                            output_file.write(data)

        print("데이터 변경이 완료되었습니다.")

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 실행 예제
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("사용법: [프로그램] [입력 파일] [텍스트 파일] [출력 폴더]")
    else:
        input_file_path = sys.argv[1]
        new_data_file_path = sys.argv[2]
        output_folder = sys.argv[3]
        main(input_file_path, new_data_file_path, output_folder)
