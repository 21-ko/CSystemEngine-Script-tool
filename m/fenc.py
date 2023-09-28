import struct
import os
import xml.etree.ElementTree as ET

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

def main(input_file_path, xml_file_path, output_folder):
    try:
        with open(input_file_path, 'rb') as input_file:
            input_filename = os.path.basename(input_file_path)
            output_file_path = os.path.join(output_folder, input_filename)
            
            with open(output_file_path, 'wb') as output_file:
                tree = ET.parse(xml_file_path)
                root = tree.getroot()
                data_elems = root.findall('data')
                
                data_index = 0  # data 요소 인덱스
                
                while True:
                    # 데이터 구조 읽기
                    data_length_bytes = input_file.read(4)
                    if not data_length_bytes:
                        break  # 파일의 끝에 도달하면 종료

                    data_length = struct.unpack('<I', data_length_bytes)[0]
                    data_type = struct.unpack('B', input_file.read(1))[0]

                    if data_type == 0x54:
                        unk1 = struct.unpack('<I', input_file.read(4))[0]
                        org_xor_key = struct.unpack('<I', input_file.read(4))[0]
                        # 데이터 읽기
                        data = input_file.read(data_length - 9 - 4)

                        if data_index < len(data_elems):
                            new_data_elem = data_elems[data_index]
                            new_data = new_data_elem.text.strip()  # <data> 요소의 내용을 가져옴
                            new_data = new_data.replace('\\n', '\n')  # '\n'을 \n으로 변경

                            # 데이터를 UTF-16 LE로 인코딩하고 바이트로 변환
                            new_data_bytes = new_data.encode('utf-16-le')

                            # 새로운 XOR 키 값 계산.
                            xor_key = len(new_data_bytes) // 2

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

                            data_index += 1  # 다음 <data> 요소로 이동

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