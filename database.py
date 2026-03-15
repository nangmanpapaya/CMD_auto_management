import sqlite3

def get_connection():
    conn = sqlite3.connect("football.db")
    conn.row_factory = sqlite3.Row  # 딕셔너리처럼 컬럼명으로 접근 가능하게
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 부원 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT DEFAULT '활동',
            member_type TEXT NOT NULL,
            campus TEXT,
            major TEXT,
            student_id TEXT,
            phone TEXT,
            email TEXT,
            generation INTEGER,
            years_active INTEGER,
            jersey_number INTEGER,
            offense_position TEXT,
            defense_position TEXT, 
            height_cm REAL,
            weight_kg REAL,
            helmet_status TEXT DEFAULT 'none',
            note TEXT,
            created_at TEXT DEFAULT (date('now'))
        )
    """)

    # 직책 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            season TEXT,
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # 퇴부 이력 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            leave_reason TEXT,
            leave_date TEXT,
            note TEXT,
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # 회비 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            amount INTEGER,
            paid INTEGER DEFAULT 0,
            paid_date TEXT,
            semester TEXT,
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # 물품 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_qty INTEGER DEFAULT 0,
            available_qty INTEGER DEFAULT 0
        )
    """)

    # 대여 기록 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            equipment_id INTEGER NOT NULL,
            rented_at TEXT DEFAULT (datetime('now')),
            returned_at TEXT,
            status TEXT DEFAULT '대여중',
            FOREIGN KEY (member_id) REFERENCES members(id),
            FOREIGN KEY (equipment_id) REFERENCES equipment(id)
        )
    """)

    # 출석 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            session_date TEXT NOT NULL,
            status TEXT DEFAULT '출석',
            note TEXT,
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    conn.commit()
    conn.close()
    print("DB 초기화 완료!")


# 부원 추가
def add_member(name, member_type, phone, student_id, status='활동', campus=None,
               major=None, email=None, generation=None, years_active=None,
               jersey_number=None, offense_position=None, defense_position=None, height_cm=None,
               weight_kg=None, helmet_status='none', note=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO members 
        (name, member_type, phone, student_id, status, campus, major, email,
         generation, years_active, jersey_number, offense_position, defense_position, 
         height_cm, weight_kg, helmet_status, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, member_type, phone, student_id, status, campus, major, email,
          generation, years_active, jersey_number, offense_position, defense_position, height_cm, weight_kg,
          helmet_status, note))
    conn.commit()
    conn.close()

# 전체 부원 조회
def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members ORDER BY generation, name")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("DB 초기화 완료!")