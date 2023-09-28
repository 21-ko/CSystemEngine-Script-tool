import os
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom

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

def create_xml_element(root, tag, text):
    element = ET.Element(tag)
    element.text = text
    root.append(element)

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8")

def decrypt_data(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".a0"):
            input_file = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".xml"
            output_file = os.path.join(output_folder, output_filename)

            with open(input_file, 'rb') as f:
                input_data = f.read()

            data_size = len(input_data)
            root = ET.Element("root")

            i = 0
            while i < data_size:
            
                # 4바이트 길이를 읽습니다.
                data_length = int.from_bytes(input_data[i:i+4], byteorder='little')
                i += 4

                if data_length <= 9:
                    break

                # 1바이트 데이터 타입을 읽습니다.
                data_type = input_data[i]
                if data_type == 0x54:  # 'T'
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
                decrypted_data = xor_decrypt(data, xor_key)
                text = decrypted_data.decode('utf-16-le')

                # 개행 문자 교체.
                text = text.replace('\n', '\\n')

                if len(decrypted_data) > 0:
                    create_xml_element(root, "data", text)

            if len(root) > 0:
                xml_content = prettify(root)
                with open(output_file, 'wb') as output:
                    output.write(xml_content)