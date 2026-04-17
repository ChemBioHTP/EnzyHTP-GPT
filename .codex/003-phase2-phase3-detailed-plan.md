# EnzyHTP-GPT：Phase 2/3 细化开发方案（会话字段迁移 + 业务流程切换）

基于文档：`/home/shaoq1/bin/EnzyHTP-GPT/.codex/001-response-migration.md`、`/home/shaoq1/bin/EnzyHTP-GPT/.codex/002-phase0-phase1-detailed-plan.md`  
更新时间：2026-03-18

## 0. 背景与本轮目标

Phase 0/1 已完成，当前进入迁移关键阶段：
- Phase 2：模型字段迁移（thread -> conversation 双轨）
- Phase 3：业务流程切换（`/assistants` 内部语义从 thread 切到 conversation）

已发现的真实问题（测试反馈）：
- `QuestionAnalyzer` 可正常运行，但后续 `MetricsPlanner` 和 `QuestionSummarizer` 未拿到正确的 `QuestionAnalyzer` 输出，导致文本异常。
- 该问题属于 Phase 2/3 范畴：会话标识与阶段输入传递链路未彻底从 thread 语义迁移到 conversation 语义。

---

## 1. Phase 2：模型字段迁移（1~1.5 天）

## 1.1 DoD（完成定义）
1. `Experiment` 支持 conversation 字段并与 thread 字段并存。
2. 新增读写 helper，业务层不再直接拼 `thread_id_list[0]`。
3. 历史数据迁移脚本可执行、可回滚、可幂等。
4. `clear_chat_threads()` 可在 responses runtime 下正确清理 conversation。

## 1.2 数据模型改造

改动文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/experiment/models.py`

新增字段：
- `current_conversation_id: str | None`
- `conversation_id_list: List[str]`
- `openai_runtime: str | None`（记录该实验最近一次运行时，`assistants|responses`）

新增 helper（建议）：
1. `append_conversation_id_list(new_conversation_id: str)`
2. `append_session_id(new_session_id: str, runtime: str)`  
说明：统一入口，根据 runtime 写入 thread 或 conversation 字段。
3. `get_primary_session_id(runtime: str) -> str | None`  
说明：`responses` 优先 `current_conversation_id`，否则回退兼容字段。
4. `get_question_analyzer_session_id(runtime: str) -> str | None`  
说明：后续阶段读取 QA 输出时使用，不再硬编码 `thread_id_list[0]`。

## 1.3 聊天消息结构增强（为 Phase 3 做铺垫）

改动文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/experiment/models.py`

扩展 `chat_messages` 元素（向后兼容）：
- `role`
- `text_value`
- `assistant_type`（可选，记录消息由哪个 agent 生成）
- `session_id`（可选，记录该条消息所属 conversation/thread）

目的：
- 为“阶段输入传递”提供稳定数据源，避免仅依赖远端会话回读。

## 1.4 数据迁移脚本

新增文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/dev-tools/migrate_thread_to_conversation.py`

迁移规则：
1. 对每个 `Experiment`：
- 若不存在 conversation 字段，补默认值（`None` / `[]`）。
- 若存在 `thread_id_list` 但无 conversation，保持 thread 字段不动并打 `openai_runtime="assistants_legacy"`。
2. 脚本幂等：重复运行不重复追加、不破坏已有 conversation 字段。
3. 支持 dry-run：输出将变更条数与样例，不落库。

验收命令建议：
```bash
python flask-server/dev-tools/migrate_thread_to_conversation.py --dry-run
python flask-server/dev-tools/migrate_thread_to_conversation.py --apply
```

## 1.5 清理逻辑改造

改动文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/experiment/models.py`

目标：
- `clear_chat_threads(openai_secret_key)` 同时尝试清理：
  - `current_conversation_id` / `conversation_id_list`
  - 兼容 `current_thread_id` / `thread_id_list`
- 删除失败不阻断主流程，但要记录失败 ID 便于重试。

## 1.6 Phase 2 测试清单
1. 模型读写单测：conversation 字段 append/get 行为正确。
2. 迁移脚本单测：空数据、混合数据、重复执行。
3. 清理逻辑单测：responses 与 assistants 双栈都可清理并保持幂等。

---

## 2. Phase 3：业务流程切换（2~3 天）

## 2.1 DoD（完成定义）
1. `/api/experiment/<id>/assistants` 在 responses 下完整跑通 `Question -> Metrics -> Mutant`。
2. `MetricsPlanner`、`QuestionSummarizer` 能稳定拿到正确的 `QuestionAnalyzer` 输出。
3. 路由外观保持不变（前端无感）。
4. 切回 `assistants` 后旧路径不回归。

## 2.2 关键问题专项：QA 输出传递异常

现状风险点：
- 当前阶段切换摘要来源仍依赖旧 thread 逻辑（如 `thread_id_list[0]`），在 responses 下可能取到 legacy thread 或空内容。

修复策略：
1. `AssistantsApi.put` 中构造下一阶段输入时，改为多级优先级：
- 优先：从 `chat_messages` 里按 `assistant_type=QuestionAnalyzer` 抽取最新 assistant 文本。
- 其次：`get_question_analyzer_session_id(runtime)` 回读远端 messages/summary。
- 最后：回退当前兼容逻辑（保底）。
2. `QuestionSummarizer` 调用同样使用上述优先级，禁止固定 `thread_id_list[0]`。

## 2.3 路由重构任务

改动文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/experiment/views.py`
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/experiment/agents.py`

任务拆解：
1. `AssistantsApi.post`
- 新会话 ID 写入统一 helper（`append_session_id`），并写 `assistant_type/session_id` 到 `chat_messages`。
2. `AssistantsApi.put`
- 阶段切换输入改为读取“QA 产物”而非固定 thread 索引。
3. `AssistantsApi.get`
- 读取消息时优先 `chat_messages`，远端会话只做补全。
4. `AssistantsApi.delete`
- 调用模型层统一清理，避免直接假设 thread 语义。
5. `agents.py`
- 保持提示词和工具定义不变，仅依赖统一服务契约（`ask_gpt/pre_process/post_process`）。

## 2.4 特殊路径与旁路

目标：
- 检查并清理所有直接依赖 `thread_id` 的路径（含 MutationApi 已切门面路径，继续核对其他旁路）。

核查方法建议：
```bash
rg -n "thread_id|thread_id_list|get_thread_summary|get_thread_messages" flask-server/experiment
```

## 2.5 Phase 3 测试清单
1. API 集成测试（responses）
- `GET/POST/PUT/DELETE /api/experiment/<id>/assistants`
- 验证阶段切换后输入链：Metrics/Summarizer 接收到 QA 输出。
2. 回归测试（assistants）
- 同路由 smoke，确认回滚可用。
3. 失败路径测试
- 无效会话 ID、远端 summary 失败、tool loop 失败时返回契约稳定。

---

## 3. 执行顺序与里程碑

## 3.1 建议顺序
1. 先完成 Phase 2 的字段与 helper（不改路由行为）。
2. 再落 Phase 3 的 `AssistantsApi` 输入链路重构。
3. 最后补自动化回归与文档状态更新。

## 3.2 里程碑验收
1. M1（Phase 2 完成）
- 数据迁移脚本可执行、模型 helper 可用、清理逻辑通过单测。
2. M2（Phase 3 完成）
- 你报告的问题（QA 输出无法传递）复现用例转绿。
- responses/assistants 双栈 smoke 均通过。

---

## 4. 风险与回滚

1. 风险：历史数据字段不一致导致阶段读取歧义。  
处理：统一通过 helper 读写，禁止业务层直接拼字段。

2. 风险：远端 conversation items 不稳定导致摘要失败。  
处理：以 `chat_messages` 为第一来源，远端仅补全。

3. 回滚：任意阶段可将 `OPENAI_RUNTIME` 切回 `assistants`，并保留旧 thread 字段路径。
