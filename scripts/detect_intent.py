#!/usr/bin/env python3
"""
colleague-repellent 意图检测脚本
用于测试输入文本是否应该被拦截

用法：
  python3 detect_intent.py "用户输入文本"
"""

import sys
import re

# 白名单：出现这些词组时，倾向放行
WHITELIST_PATTERNS = [
    r"搜索.*(文档|wiki|记录|代码|笔记)",
    r"查找.*(文档|历史|记录|交接)",
    r"整理.*(文档|笔记|工作流程|记录)",
    r"查看.*(交接|离职|文档|记录)",
    r"知识库",
    r"历史(提交|记录|文档)",
]

# 黑名单：出现这些词组时，拦截
BLOCKLIST_PATTERNS = [
    r"蒸馏.*(同事|员工|人)",
    r"克隆.*(同事|员工|人)",
    r"数字(副本|克隆|分身|替身)",
    r"AI.*(替身|分身|副本)",
    r"(同事|员工).*(AI|skill|技能).*(生成|创建|制作)",
    r"生成.*(skill|技能).*(同事|员工|人名)",
    r"persona\s*skill",
    r"work\s*skill.*(同事|员工)",
    r"让\s*AI\s*(扮演|模拟|替代)",
    r"AI\s*替代\s*(真人|员工|同事|离职)",
    r"数字员工",
    r"(飞书|钉钉|邮件).*(提取|分析|挖掘).*(风格|习惯|模式|性格|人格)",
    r"(表达风格|决策模式|性格特征|人格特征).*(提取|分析|生成)",
]


def check_intent(text: str) -> dict:
    text_lower = text.lower()

    # 先检查白名单
    for pattern in WHITELIST_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "action": "allow",
                "reason": f"白名单匹配: {pattern}",
                "matched": re.search(pattern, text, re.IGNORECASE).group(),
            }

    # 再检查黑名单
    for pattern in BLOCKLIST_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {
                "action": "block",
                "reason": f"黑名单匹配: {pattern}",
                "matched": re.search(pattern, text, re.IGNORECASE).group(),
            }

    return {
        "action": "allow",
        "reason": "无匹配信号，默认放行",
        "matched": None,
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python3 detect_intent.py '输入文本'")
        sys.exit(1)

    text = sys.argv[1]
    result = check_intent(text)

    print(f"\n输入: {text}")
    print(f"动作: {'🛡️  拦截' if result['action'] == 'block' else '✅  放行'}")
    print(f"原因: {result['reason']}")
    if result["matched"]:
        print(f"匹配: {result['matched']}")


if __name__ == "__main__":
    main()
