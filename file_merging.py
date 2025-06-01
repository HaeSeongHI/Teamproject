import os
import chardet
import re

def read_file_with_encoding(filepath):
    with open(filepath, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding is None:
            raise ValueError(f"{filepath}의 인코딩을 감지할 수 없습니다.")
    with open(filepath, 'r', encoding=encoding) as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def extract_semester_from_path(filepath):
    # 경로 중에 '1-1', '2-2'처럼 생긴 폴더 이름을 찾아냄
    match = re.search(r'(\d{1,2}-\d{1,2})', filepath)
    if match:
        return match.group(1)
    return "미상"

def parse_course_file(filepath):
    lines = read_file_with_encoding(filepath)
    filename = os.path.basename(filepath)
    subject_name = os.path.splitext(filename)[0]

    if len(lines) == 3:
        course_desc, learning_goal, learning_outcome = lines
        prereq = "없음"
    elif len(lines) == 4:
        course_desc, prereq, learning_goal, learning_outcome = lines
    else:
        raise ValueError(f"{filename}의 줄 수가 3 또는 4가 아님 (현재 {len(lines)}줄)")

    semester = extract_semester_from_path(filepath)

    return f"""과목명: {subject_name}
과목설명: {course_desc}
선수과목 및 공통필수과목: {prereq}
학습목표: {learning_goal}
학습성과: {learning_outcome}
수강학년/학기: {semester}

"""

def merge_all_courses(root_folder, output_file):
    merged_text = ""
    merged_count = 0

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.txt'):
                filepath = os.path.join(dirpath, filename)
                try:
                    merged_text += parse_course_file(filepath)
                    merged_count += 1
                except Exception as e:
                    print(f"⚠️ 오류: {filename} - {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_text)

    print(f"✅ 총 {merged_count}개 파일 병합 완료: {output_file}")


# 사용 예시
merge_all_courses("data", "academic.txt")
