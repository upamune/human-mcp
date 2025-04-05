import asyncio
import json
import os
import sys
import uuid
from typing import Dict, Any, List, Optional

# Add the parent directory to the Python path so we can import human_mcp
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
sys.stderr.write(f"Added to Python path: {parent_dir}\n")
sys.stderr.write(f"Python path is now: {sys.path}\n")

try:
    from mcp.server.fastmcp import FastMCP, Context
    sys.stderr.write("Successfully imported FastMCP\n")
except ImportError as e:
    sys.stderr.write(f"Error importing FastMCP: {e}\n")
    raise

try:
    import human_mcp.db_utils as db_utils
    import human_mcp.tools as tools
    sys.stderr.write("Successfully imported human_mcp modules\n")
except ImportError as e:
    sys.stderr.write(f"Error importing human_mcp modules: {e}\n")
    # Try direct import as a fallback
    try:
        sys.stderr.write("Attempting direct import...\n")
        import db_utils
        import tools
        sys.stderr.write("Successfully imported via direct import\n")
    except ImportError as e2:
        sys.stderr.write(f"Direct import also failed: {e2}\n")
        raise

# データベースの初期化
db_utils.initialize_db()

# MCPサーバーの作成
mcp = FastMCP("human-mcp")

@mcp.tool()
async def human_eye_tool(prompt: str, ctx: Context) -> Dict[str, str]:
    """人間が目で見て状況を説明したり、特定のものを探したりします。"""
    task_id = str(uuid.uuid4())
    instruction = f"👁️ 目を使って観察: {prompt}"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, instruction)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"observation": result}

@mcp.tool()
async def human_hand_tool(instruction: str, ctx: Context) -> Dict[str, str]:
    """人間が手を使って簡単な物理的操作を実行します。"""
    task_id = str(uuid.uuid4())
    formatted_instruction = f"✋ 手を使って操作: {instruction}"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, formatted_instruction)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"result": result}

@mcp.tool()
async def human_mouth_tool(utterance: str, ctx: Context) -> Dict[str, str]:
    """人間が口を使って指定された言葉を発話します。"""
    task_id = str(uuid.uuid4())
    formatted_utterance = f"👄 口を使って発話: {utterance}"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, formatted_utterance)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"response": result}

@mcp.tool()
async def human_weather_tool(ctx: Context) -> Dict[str, str]:
    """人間が現在地の天気を確認して報告します。"""
    task_id = str(uuid.uuid4())
    instruction = f"🌤️ 現在地の天気を確認してください"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, instruction)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"weather": result}

@mcp.tool()
async def human_ear_tool(instruction: str, ctx: Context) -> Dict[str, str]:
    """人間が耳を使って音を聞き、状況を説明します。

    例:
    - 周囲の環境音の確認
    - 特定の音源の識別
    - 会話の聞き取り
    """
    task_id = str(uuid.uuid4())
    formatted_instruction = f"👂 耳を使って聴取: {instruction}"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, formatted_instruction)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"sound": result}

@mcp.tool()
async def human_nose_tool(instruction: str, ctx: Context) -> Dict[str, str]:
    """人間が鼻を使って匂いを確認します。

    例:
    - 食べ物の新鮮さの確認
    - ガス漏れなどの危険な匂いの検知
    - 香りの評価
    """
    task_id = str(uuid.uuid4())
    formatted_instruction = f"👃 鼻を使って嗅覚確認: {instruction}"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, formatted_instruction)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"smell": result}

@mcp.tool()
async def human_taste_tool(instruction: str, ctx: Context) -> Dict[str, str]:
    """人間が口を使って食べ物を味わい、その味を説明します。

    例:
    - 料理の味の評価
    - 食材の新鮮さの確認
    - 味の分析（甘味、酸味、塩味、苦味、うま味）
    """
    task_id = str(uuid.uuid4())
    formatted_instruction = f"👅 口を使って味わう: {instruction}"

    # タスクをデータベースに追加
    db_utils.add_task(task_id, formatted_instruction)

    # ログ出力
    sys.stderr.write(f"Human task created: {task_id}. Waiting for completion...\n")

    # 結果を待機（非同期ポーリング）
    result = await wait_for_task_completion(task_id)

    # ログ出力
    sys.stderr.write(f"Human task {task_id} completed.\n")

    return {"taste": result}

async def wait_for_task_completion(task_id: str, timeout: int = 300) -> str:
    """タスクの完了を待機する（タイムアウト付き）"""
    start_time = asyncio.get_event_loop().time()

    while True:
        # 現在の経過時間を確認
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > timeout:
            return f"タイムアウト: {timeout}秒経過しても応答がありませんでした。"

        # タスクの状態を確認
        status, result = db_utils.get_task_result(task_id)

        if status == 'completed' and result is not None:
            return result

        # 1秒待機してから再確認
        await asyncio.sleep(1)

if __name__ == "__main__":
    mcp.run()
