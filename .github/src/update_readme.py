import os
from datetime import datetime
import re

# 탐색할 root 경로들
dir_paths = ["./Certifications", "./Spring"]

# ignore 파일을 읽어서 패턴 목록을 리스트로 저장
patterns = []
if os.path.exists('./.github/config/.ignore'):
    with open('./.github/config/.ignore', 'r') as f:
        ignore = f.readlines()
    for p in ignore:
        pattern = r""
        for c in p.strip():
            if c == '*':
                pattern = pattern + r".*"
            elif c in ".^$*+?{}[]|()":  # 메타 문자
                pattern = pattern + r"[{}]".format(c)
            else:
                pattern = pattern + r'{}'.format(c)
        patterns.append(pattern)

# ignore 패턴과 일치하는지 확인하는 함수
def check_ignore_pattern(item_path):
    for pattern in patterns:
        if re.fullmatch(pattern, os.path.relpath(item_path)):
            return True
    return False

def find_target(path, level):
    file_list = []
    # 하위 디렉토리 순환
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if check_ignore_pattern(item) or check_ignore_pattern(item_path):
            # 파일 이름이나 경로가 ignore 조건을 만족하면 무시
            continue
        # 파일(혹은 디렉토리) 리스트에 추가하기
        mtime = datetime.fromtimestamp(os.stat(item_path).st_mtime)  # 수정 날짜 가져오기
        mtime = mtime.strftime('%Y년 %m월 %d일')  # 날짜 형식 변환
        if item_path.endswith('.md'):
            file_list.append([item, item_path, mtime, []])
        # 디렉토리면 하위 디렉토리 탐색
        if os.path.isdir(item_path):
            sub_list = find_target(item_path, level+1)
            if sub_list:
                file_list.append([item, item_path, mtime, sub_list])
    return file_list

def print_file_list(f, file_list, level):
    file_list.sort(key=lambda file: file[2], reverse=True)
    for file in file_list:
        for i in range(level):
            f.write("  ")
        if file[0].endswith('.md'):
            # 파일이면 수정 날짜와 함께 출력
            file_name = file[0][:-3].replace(' ', '_')  # 공백을 언더스코어로 변경
            file_path = file[1].replace(' ', '%20')  # URL 인코딩
            f.write("- [{}]({}) - {}\n".format(file_name, file_path, file[2]))
        else:
            # 디렉토리면 날짜 빼고 출력
            f.write("- {}\n".format(file[0]))
        print_file_list(f, file[3], level+1)

all_files = []
for dir_path in dir_paths:
    all_files.extend(find_target(dir_path, 0))

# README.md 파일을 열어 파일 경로를 추가
with open("README.md", "w") as f:
    f.write("# 공부 기록\n\n")
    f.write("Certifications와 Spring 관련 학습 내용 정리\n\n")
    f.write("---\n\n")

    most = 5
    f.write("### 최근 {} 개의 학습 내용\n".format(most))
    recent_files = sorted([file for file in all_files if file[0].endswith('.md')], key=lambda x: x[2], reverse=True)[:most]
    for file in recent_files:
      file_name = file[0][:-3].replace(' ', '_')  # 공백을 언더스코어로 변경
      file_path = file[1].replace(' ', '%20')  # URL 인코딩
      f.write("- [{}]({}) - {}\n".format(file_name, file_path, file[2]))

    f.write("### 카테고리\n")
    for dir_path in dir_paths:
        f.write("- [{}]({})\n".format(os.path.basename(dir_path), dir_path))
    f.write("\n")

    for dir_path in dir_paths:
        f.write("### [{}]({})\n".format(os.path.basename(dir_path), dir_path))
        dir_files = [file for file in all_files if file[1].startswith(dir_path)]
        print_file_list(f, dir_files, 0)
        f.write("\n")
