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
    # 예: 경로가 data/1-1/인공지능개론.txt이면 '1-1' 추출
    match = re.search(r'(\d{1,2}-\d{1,2})', filepath)
    if match:
        return match.group(1)
    return "미상"  # 찾지 못했을 경우

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

    return f"""과목: {subject_name}
선수과목 및 공통필수과목: {prereq}
학습목표: {learning_goal}
학습성과: {learning_outcome}
수강학년/학기: {semester}

"""

def merge_all_courses(folder_path, output_file):
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    merged_text = ""
    merged_count = 0

    for filename in sorted(files):
        filepath = os.path.join(folder_path, filename)
        try:
            merged_text += parse_course_file(filepath)
            merged_count += 1
        except Exception as e:
            print(f"⚠️ 오류: {filename} - {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_text)
    print(f"✅ {merged_count}개 파일 병합 완료: {output_file}")


# 사용 예시
merge_all_courses("data/1-2", "전체과목정리.txt")
