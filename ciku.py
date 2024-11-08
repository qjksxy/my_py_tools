import os
import re
from pypinyin import pinyin, Style

def convert_to_pinyin(text):
    # 只保留汉字字符
    filtered_text = ''.join(re.findall(r'[\u4e00-\u9fff]', text))
    pinyin_list = pinyin(filtered_text, style=Style.NORMAL)
    pinyin_text = ' '.join([item[0] for item in pinyin_list])
    return f"{text}\t{pinyin_text}\t5"

def process_files(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_file_path):
            # 创建输出文件路径，并将后缀改为 .dict.yaml
            file_name_without_extension = os.path.splitext(filename)[0]
            output_filename = file_name_without_extension + '.dict.yaml'
            output_file_path = os.path.join(output_folder, output_filename)
            
            # 读取并处理文件内容
            with open(input_file_path, 'r', encoding='utf-8') as infile:
                lines = infile.readlines()

            # 将处理后的内容写入输出文件
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                # 写入文件头
                header = f"""---
name: {file_name_without_extension}
version: "1.0"
sort: by_weight
use_preset_vocabulary: true
...
"""
                outfile.write(header + '\n')

                # 写入每行转换后的拼音
                for line in lines:
                    line = line.strip()  # 去除换行符和空格
                    if line:  # 确保不是空行
                        result = convert_to_pinyin(line)
                        outfile.write(result + '\n')

# 使用示例
input_folder = 'input'  # 替换为你的输入文件夹路径
output_folder = 'output'  # 替换为你的输出文件夹路径
process_files(input_folder, output_folder)
