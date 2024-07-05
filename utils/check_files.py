import os

def get_file_list():
    file_list = []
    for root, _, files in os.walk("./Spring"):
        for file in files:
            if file.endswith(".md"):
                file_list.append(os.path.join(root, file))

    for root, _, files in os.walk("./Certifications"):
        for file in files:
            if file.endswith(".md"):
                file_list.append(os.path.join(root, file))

    file_list = sorted(file_list)
    total_file_cnt = len(file_list)
    return file_list, total_file_cnt

def make_info(file_list, total_file_cnt):
    info = f"## TIL List\nTotal TIL Count: {total_file_cnt}개\n"
    for file in file_list:
        relative_path = os.path.relpath(file, "./")
        temp = f"- [{os.path.basename(file)}](https://github.com/pie0902/TIL/blob/main/{relative_path})\n"
        info += temp
    return info

def make_read_me(info):
    return f"""# TIL<br><br>
{info}
"""

def update_readme():
    file_list, total_file_cnt = get_file_list()
    info = make_info(file_list, total_file_cnt)
    readme = make_read_me(info)
    return readme

if __name__ == "__main__":
    readme = update_readme()
    with open("./README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
