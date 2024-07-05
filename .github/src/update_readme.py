import os
from datetime import datetime
import re

# 설정
DIR_PATHS = ["./Certifications", "./Spring"]
IGNORE_FILE_PATH = './.github/config/.ignore'

def load_ignore_patterns():
    patterns = []
    if os.path.exists(IGNORE_FILE_PATH):
        with open(IGNORE_FILE_PATH, 'r') as f:
            for line in f:
                pattern = line.strip()
                pattern = pattern.replace("*", ".*")
                pattern = re.escape(pattern).replace(r"\*", ".*")
                patterns.append(pattern)
    return patterns

def is_ignored(item_path, patterns):
    return any(re.fullmatch(pattern, os.path.relpath(item_path)) for pattern in patterns)

def sort_key(item):
    match = re.match(r'^(\d+)', item[0])
    return int(match.group(1)) if match else float('inf')

def print_file_list(f, file_list, level=0):
    for file in sorted(file_list, key=sort_key):
        indent = "  " * level
        if file[0].endswith('.md'):
            file_name = file[0][:-3].replace(' ', '_')
            file_path = file[1].replace(' ', '%20')
            f.write(f"{indent}- [{file_name}]({file_path}) - {file[2]}\n")
        else:
            f.write(f"{indent}- {file[0]}\n")
        print_file_list(f, file[3], level + 1)

def find_files(path, level=0, ignore_patterns=None):
    if ignore_patterns is None:
        ignore_patterns = []

    file_list = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if is_ignored(item_path, ignore_patterns):
            continue

        mtime = datetime.fromtimestamp(os.stat(item_path).st_mtime).strftime('%Y-%m-%d')

        if item_path.endswith('.md'):
            file_list.append([item, item_path, mtime, []])
        elif os.path.isdir(item_path):
            sub_list = find_files(item_path, level + 1, ignore_patterns)
            if sub_list:
                file_list.append([item, item_path, mtime, sub_list])

    return file_list

def write_readme(file_lists):
    with open("README.md", "w") as f:
        f.write("# 공부 기록\n\n")
        f.write("Certifications와 Spring 관련 학습 내용 정리\n\n")
        f.write("---\n\n")

        f.write("### 카테고리\n")
        for dir_path in DIR_PATHS:
            f.write(f"- [{os.path.basename(dir_path)}]({dir_path})\n")
        f.write("\n")

        for dir_path, file_list in zip(DIR_PATHS, file_lists):
            f.write(f"### [{os.path.basename(dir_path)}]({dir_path})\n")
            print_file_list(f, file_list)
            f.write("\n")

def main():
    ignore_patterns = load_ignore_patterns()
    file_lists = [find_files(dir_path, ignore_patterns=ignore_patterns) for dir_path in DIR_PATHS]
    write_readme(file_lists)

if __name__ == "__main__":
    main()
