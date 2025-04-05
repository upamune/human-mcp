from typing import Dict, Any, List

# ツール定義
HUMAN_TOOLS = [
    {
        "name": "human_eye_tool",
        "description": "人間が目で見て状況を説明したり、特定のものを探したりします。",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "観察するための指示"}
            },
            "required": ["prompt"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "observation": {"type": "string", "description": "人間による観察結果"}
            },
            "required": ["observation"]
        }
    },
    {
        "name": "human_hand_tool",
        "description": "人間が手を使って簡単な物理的操作を実行します。",
        "input_schema": {
            "type": "object",
            "properties": {
                "instruction": {"type": "string", "description": "実行する物理的操作の指示"}
            },
            "required": ["instruction"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "result": {"type": "string", "description": "操作の結果"}
            },
            "required": ["result"]
        }
    },
    {
        "name": "human_mouth_tool",
        "description": "人間が口を使って指定された言葉を発話します。",
        "input_schema": {
            "type": "object",
            "properties": {
                "utterance": {"type": "string", "description": "発話する内容"}
            },
            "required": ["utterance"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "response": {"type": "string", "description": "発話に対する応答"}
            },
            "required": ["response"]
        }
    },
    {
        "name": "human_weather_tool",
        "description": "人間が現在地の天気を確認して報告します。",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "weather": {"type": "string", "description": "現在地の天気情報"}
            },
            "required": ["weather"]
        }
    }
]

def get_tools() -> List[Dict[str, Any]]:
    """利用可能なツールのリストを返す"""
    return HUMAN_TOOLS

def get_tool_by_name(name: str) -> Dict[str, Any]:
    """名前でツールを検索"""
    for tool in HUMAN_TOOLS:
        if tool["name"] == name:
            return tool
    raise ValueError(f"Tool not found: {name}")
