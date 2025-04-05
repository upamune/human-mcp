import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional
import sys
import os

# データベースファイルのパス
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "human_tasks.db"))

def initialize_db() -> None:
    """データベースの初期化と必要なテーブルの作成"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS human_tasks (
                task_id TEXT PRIMARY KEY,
                instruction TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                result TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"データベース初期化エラー: {e}", file=sys.stderr)
        raise

def add_task(task_id: str, instruction: str) -> None:
    """新しいタスクをデータベースに追加"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO human_tasks (task_id, instruction) VALUES (?, ?)",
                (task_id, instruction)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"タスク追加エラー: {e}", file=sys.stderr)
        raise

def get_pending_tasks() -> List[Tuple[str, str]]:
    """ステータスが'pending'のタスクを取得"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                "SELECT task_id, instruction FROM human_tasks WHERE status = 'pending' ORDER BY created_at"
            )
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"保留中タスク取得エラー: {e}", file=sys.stderr)
        return []

def get_task_result(task_id: str) -> Tuple[Optional[str], Optional[str]]:
    """指定されたタスクIDのステータスと結果を取得"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                "SELECT status, result FROM human_tasks WHERE task_id = ?",
                (task_id,)
            )
            row = cursor.fetchone()
            if row:
                return row[0], row[1]
            return None, None
    except sqlite3.Error as e:
        print(f"タスク結果取得エラー: {e}", file=sys.stderr)
        return None, None

def update_task_result(task_id: str, result: str) -> None:
    """タスクの結果を更新し、ステータスを'completed'に変更"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "UPDATE human_tasks SET status = 'completed', result = ?, updated_at = CURRENT_TIMESTAMP WHERE task_id = ?",
                (result, task_id)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"タスク結果更新エラー: {e}", file=sys.stderr)
        raise
