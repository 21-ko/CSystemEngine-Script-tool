import os

def xor_decrypt(data, key):
    decrypted_data = bytearray()
    is_decrypting = True  # 초기에 복호화 모드로 시작

    for byte in data:
        if is_decrypting:
            decrypted_byte = byte ^ key
            decrypted_data.append(decrypted_byte)
        else:
            decrypted_data.append(byte)

        # 다음 바이트는 반대 모드로 전환
        is_decrypting = not is_decrypting

    return decrypted_data

def decrypt_data(input_folder, output_folder):
    # 입력 폴더 내의 모든 .a0 파일을 대상으로 반복합니다.
    for filename in os.listdir(input_folder):
        if filename.endswith(".a0"):
            input_file = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".txt"  # 확장명을 제거한 파일 이름
            output_file = os.path.join(output_folder, output_filename)

            with open(input_file, 'rb') as f:
                input_data = f.read()

            data_size = len(input_data)
            decrypted_data = bytearray()

            i = 0
            while i < data_size:
                # 4바이트 길이를 읽습니다.
                data_length = int.from_bytes(input_data[i:i+4], byteorder='little')
                i += 4

                # 기본 크기보다 작거나 같다면 break.
                if data_length <= 9:
                    break

                # 1바이트 데이터 타입을 읽습니다.
                data_type = input_data[i]
                if data_type == 0x54: # T
                    i += 1
                elif data_type != 0x54:
                    i += data_length
                    continue

                # 4바이트 unk1을 읽습니다.
                unk1 = int.from_bytes(input_data[i:i+4], byteorder='little')
                i += 4

                # 4바이트 xor 키를 읽습니다.
                xor_key = int.from_bytes(input_data[i:i+4], byteorder='little')
                i += 4

                # 데이터를 읽습니다.
                data = input_data[i:i+data_length-9-4]
                i += len(data)

                # 4바이트 unk2를 읽습니다.
                unk2 = int.from_bytes(input_data[i:i+4], byteorder='little')
                i += 4

                # 데이터를 xor 복호화합니다.
                decrypted_data.extend(xor_decrypt(data, xor_key))

            # UTF-8 형식의 텍스트 파일로 저장합니다.
            if len(decrypted_data) > 0:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(decrypted_data.decode('utf-16-le'))

# 사용 예시:
input_folder = 'arc04'
output_folder = 'arc04_txt'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
decrypt_data(input_folder, output_folder)