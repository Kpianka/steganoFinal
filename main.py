import sys


def hex_to_binary(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(4 * len(hex_string))


def binary_to_hex(binary_string):
    hex_string = hex(int(binary_string, 2))[2:].upper()
    return hex_string.zfill((len(binary_string) + 3) // 4)


def read_mess_file(mess_filename):
    with open(mess_filename, 'r') as mess_file:
        hex_data = mess_file.read().strip().split()
        binary_data = [hex_to_binary(hex_number) for hex_number in hex_data]
    return ''.join(binary_data)


def clean_html_lines(html_filename):
    with open(html_filename, 'r') as html_file:
        lines = html_file.readlines()
        cleaned_lines = [line.rstrip() for line in lines]
    return cleaned_lines


def embed_watermark_1(html_lines, binary_message):
    watermark_lines = []
    message_index = 0
    message_length = len(binary_message)
    added_end_of_message = False

    for line in html_lines:
        if message_index < message_length:
            if binary_message[message_index] == '1':
                watermark_lines.append(line + ' ')
            else:
                watermark_lines.append(line)
            message_index += 1
        elif not added_end_of_message:
            watermark_lines.append(line + '  ')
            added_end_of_message = True
        else:
            watermark_lines.append(line)

    return watermark_lines


def embed_watermark_2(html_lines, binary_message):
    watermark_lines = []
    message_index = 0
    message_length = len(binary_message)
    added_end_of_message = False

    for line in html_lines:
        if message_index < message_length:
            if binary_message[message_index] == '1':
                watermark_lines.append(line + '  ')
            else:
                watermark_lines.append(line + ' ')
            message_index += 1
        elif not added_end_of_message:
            watermark_lines.append(line + '   ')
            added_end_of_message = True
        else:
            watermark_lines.append(line)

    return watermark_lines


def write_watermarked_html(watermark_filename, watermark_lines):
    with open(watermark_filename, 'w') as watermark_file:
        watermark_file.write('\n'.join(watermark_lines) + '\n')


def process_files_1(mess_filename, html_filename, watermark_filename):
    binary_message = read_mess_file(mess_filename)
    html_lines = clean_html_lines(html_filename)
    watermark_lines = embed_watermark_1(html_lines, binary_message)
    write_watermarked_html(watermark_filename, watermark_lines)
    print(f"Plik '{html_filename}' został przetworzony i zapisany jako '{watermark_filename}'.")


def process_files_2(mess_filename, html_filename, watermark_filename):
    binary_message = read_mess_file(mess_filename)
    html_lines = clean_html_lines(html_filename)
    watermark_lines = embed_watermark_2(html_lines, binary_message)
    write_watermarked_html(watermark_filename, watermark_lines)
    print(f"Plik '{html_filename}' został przetworzony i zapisany jako '{watermark_filename}'.")


def detect_message_1(watermark_filename, detect_filename):
    with open(watermark_filename, 'r') as watermark_file:
        lines = watermark_file.readlines()

    binary_message = []

    for line in lines:
        if line.endswith('  \n') or line.endswith('  '):
            break
        elif line.endswith(' \n') or line.endswith(' '):
            binary_message.append('1')
        else:
            binary_message.append('0')

    binary_message = ''.join(binary_message)

    with open('temp.txt', 'w') as temp_file:
        temp_file.write(binary_message)

    with open('temp.txt', 'r') as temp_file:
        binary_message = temp_file.read().strip()

    hex_message = binary_to_hex(binary_message)

    with open(detect_filename, 'w') as detect_file:
        detect_file.write(hex_message + '\n')

    print(f"Wiadomość została wykryta i zapisana w '{detect_filename}'.")


def detect_message_2(watermark_filename, detect_filename):
    with open(watermark_filename, 'r') as watermark_file:
        lines = watermark_file.readlines()

    binary_message = []

    for line in lines:
        if line.endswith('   \n') or line.endswith('   '):
            break
        elif line.endswith('  \n') or line.endswith('  '):
            binary_message.append('1')
        else:
            binary_message.append('0')

    binary_message = ''.join(binary_message)

    with open('temp.txt', 'w') as temp_file:
        temp_file.write(binary_message)

    with open('temp.txt', 'r') as temp_file:
        binary_message = temp_file.read().strip()

    hex_message = binary_to_hex(binary_message)

    with open(detect_filename, 'w') as detect_file:
        detect_file.write(hex_message + '\n')

    print(f"Wiadomość została wykryta i zapisana w '{detect_filename}'.")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Użycie: python main.py -e/-d -1/-2/-3/-4 mess.txt cover.html watermark.html/detect.txt")
        sys.exit(1)

    option = sys.argv[1]
    type_of_cipher = sys.argv[2]

    if option == '-e':
        if type_of_cipher == "-1":
            message_filename = sys.argv[3]
            html_filename = sys.argv[4]
            output_filename = sys.argv[5]

            process_files_1(message_filename, html_filename, output_filename)
        elif type_of_cipher == "-2":
            message_filename = sys.argv[3]
            html_filename = sys.argv[4]
            output_filename = sys.argv[5]

            process_files_2(message_filename, html_filename, output_filename)
    elif option == '-d':
        if type_of_cipher == "-1":
            html_filename = sys.argv[3]
            output_filename = sys.argv[4]

            detect_message_1(html_filename, output_filename)
        if type_of_cipher == "-2":
            html_filename = sys.argv[3]
            output_filename = sys.argv[4]

            detect_message_2(html_filename, output_filename)
    else:
        print("Niepoprawna opcja. Użycie: -e (zanurzanie), -d (wyodrębnianie)")
        sys.exit(1)