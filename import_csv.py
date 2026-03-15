import csv
from database import get_connection, init_db

# 노션 값 -> DB 값 변환 매핑
STATUS_MAP = {
    '활동 중': '활동',
    '활동 중지': '활동중지',
    '퇴부': '퇴부',
    '부상': '부상',
    '군입대': '군입대',
    '미정': '미정',
    'OB': 'OB',
}

HELMET_MAP = {
    '보유': 'owned',
    '미보유': 'none',
    '기부': 'donated',
    '': 'none',
}

def import_from_csv(filepath):
    conn = get_connection()
    cursor = conn.cursor()

    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # 값 변환
            status = STATUS_MAP.get(row['활동 여부'].strip(), '활동')
            helmet = HELMET_MAP.get(row['개인 헬멧 보유 여부'].strip(), 'none')

            # 숫자 변환 (비어있으면 None)
            def to_int(val):
                try:
                    return int(val.strip()) if val.strip() else None
                except:
                    return None

            def to_float(val):
                try:
                    return float(val.strip()) if val.strip() else None
                except:
                    return None

            # 기수 텍스트에서 숫자 추출 (예: '4기' -> 4)
            generation_raw = row['기수'].strip()
            generation = to_int(generation_raw.replace('기', ''))

            # members 테이블에 삽입
            cursor.execute("""
                INSERT INTO members 
                (name, member_type, status, campus, major, student_id, phone,
                 email, generation, years_active, jersey_number,
                 offense_position, defense_position,
                 height_cm, weight_kg, helmet_status, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['이름'].strip(),
                row['부원 종류'].strip(),
                status,
                row['캠퍼스'].strip() or None,
                row['전공'].strip() or None,
                row['학번'].strip() or None,
                row['전화번호'].strip() or None,
                row['이메일'].strip() or None,
                generation,
                to_int(row['연차']),
                to_int(row['등번호']),
                row['공격 포지션'].strip() or None,
                row['수비 포지션'].strip() or None,
                to_float(row['키']),
                to_float(row['몸무게']),
                helmet,
                row['비고'].strip() or None,
            ))

            member_id = cursor.lastrowid

            # 직책 있으면 member_roles에 삽입
            role = row['직책'].strip()
            if role:
                cursor.execute("""
                    INSERT INTO member_roles (member_id, role, season)
                    VALUES (?, ?, ?)
                """, (member_id, role, '2025'))

    conn.commit()
    conn.close()
    print("임포트 완료!")

if __name__ == "__main__":
    import_from_csv("부원명단.csv")