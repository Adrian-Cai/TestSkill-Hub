# requirements-testcase-generator

将需求文档、PRD、技术方案转换为结构化测试策略与测试用例，并强制产出文件交付（Markdown / XMind）。

## 目录结构

- `SKILL.md`：技能主入口（触发条件、流程、模板、质量门槛）
- `rules/`：规则库（按章节拆分）
  - `_sections.md`：规则章节与优先级
  - `artifact-file-output.md`：产物必须落地文件
  - `coverage-multi-dimension.md`：多维度覆盖
  - `quality-atomic-steps.md`：步骤原子化与可验证性
  - `trace-requirement-mapping.md`：需求覆盖追踪与待确认项
  - `xmind-structure.md`：XMind 结构与转换约束
- `scripts/`
  - `markdown_to_xmind.py`：将 Markdown 用例转换为 `.xmind`
  - 其他历史脚本：学城模板转换相关

## 核心能力

1. 支持输入：文本、本地文件摘录、公开 URL、双文档（需求 + 技术方案）
2. 支持输出：
   - 默认：`outputs/testcases/<slug>.md`
   - 可选：`outputs/testcases/<slug>.xmind`
3. 输出结构固定为五部分：
   - 测试策略
   - 冒烟用例
   - 完整测试用例
   - 覆盖与追踪
   - 待确认项

## 输出约束（重点）

- 禁止只在会话页面展示结果
- 必须写入文件并返回文件路径
- 用户要求 XMind 时，先生成 Markdown，再转换为 XMind

## XMind 转换脚本

```bash
python3 scripts/markdown_to_xmind.py \
  --input outputs/testcases/order-submit.md \
  --output outputs/testcases/order-submit.xmind \
  --title "订单提交流程测试用例"
```

## 规则机制说明

执行技能时，先读 `rules/_sections.md`，再按任务读取对应规则文件。
这种规则机制与 `react-best-practices-cn/rules` 一致：
- 用规则文件承载“限制和最佳实践”
- 用 `SKILL.md` 负责触发、流程、路由规则

