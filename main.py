import re
import os
import subprocess
from collections import defaultdict

def find_files(directory):
    jpeg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                jpeg_files.append(os.path.join(root, file))

    sequences = defaultdict(list)
    pattern = re.compile(r"(.+?)(?:[\s.]?)(\d+)\.(jpg|jpeg)$", re.IGNORECASE)
    for file in jpeg_files:
        filename = os.path.basename(file)
        match = pattern.match(filename)
        if match:
            sequence_name = match.group(1).strip()
            frame_number = match.group(2)
            frame_length = len(frame_number)
            sequences[(sequence_name, frame_length)].append((int(frame_number), file))
        else:
            print(f"File not matched: {filename}")
    jpeg_files_sorted = []
    for (sequence_name, _), frames in sorted(sequences.items()):
        frames.sort(key=lambda x: x[0])
        jpeg_files_sorted.append([file for _, file in frames])
    
    return jpeg_files_sorted


def create_mov(jpeg_files_sorted, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for idx, sequence in enumerate(jpeg_files_sorted):
        if not sequence:
            continue 

        list_file_path = os.path.join(save_path, f"sequence_{idx}_list.txt")
        with open(list_file_path, 'w') as list_file:
            for file_path in sequence:
                list_file.write(f"file '{file_path}'\n")

        output_video_path = os.path.join(save_path, f"sequence_{idx}.mov")

        command = [
            'E://GitHub//Work//AlgousStudio_Task//ffmpeg-7.0.2-full_build//bin//ffmpeg.exe',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file_path,
            '-c:v', 'mjpeg',
            '-q:v', '2',
            '-r', '24',
            '-pix_fmt', 'yuvj422p',
            output_video_path
        ]
        subprocess.run(command, check=True)
        os.remove(list_file_path)

if __name__ == "__main__":
    jpeg_files_sorted = None
    save_path = None
    while True:
        state = input("1 = path to folder\n2 = path to save folder\n3 = start creating mov\n4 = exit\nYour input: ")
        match state:
            case "1":
                directory_path=str(input("Input your files path: "))
                # directory_path="P:\Downloads\source\source"
                if os.path.isdir(directory_path):
                    jpeg_files_sorted = find_files(directory_path)
                else:
                    print(f'{directory_path} is nor dir or do not exist, try again')
            case "2":
                # save_path="P:\Downloads\saved"
                save_path=str(input("Input your save path: "))
            case "3":
                if jpeg_files_sorted:
                    create_mov(jpeg_files_sorted, save_path)
                else:
                    print('Use "1" and "2" first')
            case "4":
                print("Bye!")
                quit()
