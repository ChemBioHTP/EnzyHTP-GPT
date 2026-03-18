# EnzyHTP-GPT：Assistants/Threads -> Responses 迁移评估与开发计划

更新时间：2026-03-17

## 1. 迁移背景（官方时间点）
- OpenAI 官方迁移文档说明：2025-08-26 起推荐以 `Responses API` + `Conversations API` 作为统一方向。
- Assistants API（含 Threads/Runs）计划下线时间：`2026-08-26`。
- 以当前日期（2026-03-17）计算，距下线约 5 个月，建议立即进入改造窗口。

参考：
- https://developers.openai.com/blog/responses-api
- https://platform.openai.com/docs/guides/migrate-to-responses

## 2. 项目内依赖评估（代码级）

### 2.1 强依赖（必须迁移）
1. `flask-server/services/openai_service.py`
- `OpenAIAssistant` 全量基于 `client.beta.assistants` / `client.beta.threads` / `client.beta.threads.runs`。
- 关键调用：
  - `client.beta.assistants.create`（创建 assistant 实体）
  - `client.beta.threads.create/retrieve/delete`（线程生命周期）
  - `threads.messages.create/list`（消息读写）
  - `threads.runs.stream/list/cancel`（运行控制）
  - `threads.runs.submit_tool_outputs_stream`（工具输出提交）
- 额外风险：`__del__` 中删除 assistant（每次实例化对应远端 assistant 资源），与 Responses 架构不匹配。

2. `flask-server/experiment/agents.py`
- 所有 Agent（Question/Metrics/Mutant/Result/Summarizer 等）继承 `OpenAIAssistant`。
- 业务提示词、工具定义与运行机制绑定 Assistants runtime。

3. `flask-server/experiment/views.py`
- `AssistantsApi`（GET/POST/PUT/DELETE）将业务流程直接绑定 thread 语义。
- `get_thread_messages` / `get_thread_summary` / `thread_id` 的读取与拼接贯穿流程。

4. `flask-server/experiment/models.py`
- 持久化字段显式依赖 thread：`current_thread_id`、`thread_id_list`。
- `clear_chat_threads()` 使用 `OpenAIAssistant.delete_thread(s)` 清理远端会话。

### 2.2 中等依赖（接口/命名耦合，建议兼容迁移）
1. `web-client/src/api/experiment.js`
- 前端接口命名与路径均为 `/assistants`（`getAssistants/getAssistantList/updateAssistants`）。

2. `flask-server/experiment/__init__.py`
- 路由命名固定为 `/<experiment_id>/assistants`。

3. 文档与样例
- `docs/04_api_reference.md`：明确写“Assistant thread”。
- `docs/20250419_Web APIs.postman_collection.json`：大量 `assistants` 路径与 `thread_` 示例。
- `flask-server/experiment/README.md`：示例响应包含 `current_thread_id`。

### 2.3 低优先级相关项（可选统一）
- `OpenAIChat` 仍在使用 `chat.completions.create`（非本次强制项）。
- 建议中期统一到 `responses.create`，减少双栈维护成本。

## 3. 目标架构（Responses 化）

### 3.1 概念映射（旧 -> 新）
- Assistant -> Prompt/系统指令模板（本地配置，不再创建远端 assistant 实体）
- Thread -> Conversation（或短期用 `previous_response_id` 维护上下文）
- Run -> Response
- Message/Run step -> Items（`conversation items` + `response output items`）
- submit_tool_outputs -> 在 `responses.create` 中提交 `function_call_output` 项并继续循环

### 3.2 设计原则
1. 对外接口短期兼容
- 暂不强制改前端路径，保留 `/assistants` 路由（内部实现切换为 Responses）。

2. 数据模型平滑迁移
- 新增 `conversation_id`/`conversation_id_list`，旧字段保留一段兼容期。

3. 服务层先抽象再替换
- 先构建 `ResponseWorkflowService`，再让 Agent 逐个切换，降低一次性风险。

## 4. 分阶段开发计划（可执行）

## Phase 0：准备与防回滚设计（0.5~1 天）
1. 升级 OpenAI SDK (DONE)
- 文件：`flask-server/environment.yml`
- 任务：将 `openai=1.37.0` 升到支持 Responses/Conversations 的稳定版本。 (使用pip安装了openai==2.29.0)

2. 增加开关
- 新增环境变量：`OPENAI_RUNTIME=assistants|responses`（默认 `assistants`，灰度期间可切换）。

3. 观察指标
- 增加日志字段：`response_id`、`conversation_id`、`tool_call_count`、`openai_error_code`。

验收：在不改业务逻辑下可按环境变量切换运行时。

## Phase 1：服务层双栈适配（2~3 天）
1. 新建 Responses 服务实现
- 建议文件：`flask-server/services/openai_response_service.py`
- 能力要求：
  - `ask_gpt(prompt)`
  - function tool loop（识别 `function_call`，执行本地函数，提交 `function_call_output`，直到无待执行工具）
  - conversation 模式（维护 `conversation_id`，支持读取 items）

2. 统一抽象接口
- 修改 `flask-server/services/__init__.py` 和 `openai_service.py`：
  - 提供统一基类/门面（Facade），让 `agents.py` 不感知底层栈。

3. 兼容错误码
- 将 Responses 错误映射到现有返回契约（401/429/500/504）。

验收：在测试路由下，同一 prompt 在 assistants/responses 两栈都能返回结构化响应。

## Phase 2：模型字段迁移（1~1.5 天）
1. 扩展 Experiment 字段
- 文件：`flask-server/experiment/models.py`
- 新增：`current_conversation_id`、`conversation_id_list`。
- 保留：`current_thread_id`、`thread_id_list`（兼容读取）。

2. 数据迁移脚本
- 新建脚本：`flask-server/dev-tools/migrate_thread_to_conversation.py`
- 规则：
  - 旧记录若仅有 thread 字段，则初始化 conversation 字段为空并标记 `runtime="assistants_legacy"`。
  - 新流程创建 conversation 后写入新字段；旧字段可保持原值。

3. 清理逻辑改造
- `clear_chat_threads()` 扩展为可清理 conversation（并兼容 thread 清理）。

验收：历史实验不报错；新实验优先写 conversation 字段。

## Phase 3：业务流程切换（2~3 天）
1. Agent 切换到统一门面
- 文件：`flask-server/experiment/agents.py`
- 目标：所有 Agent 继续复用现有提示词与工具定义，但底层不再依赖 `OpenAIAssistant`。

2. AssistantsApi 内部重构
- 文件：`flask-server/experiment/views.py`
- 保持 `/assistants` 路径不变，内部改成 conversation 语义：
  - GET：优先从 `chat_messages` + conversation items 组装
  - POST：走 responses tool loop
  - PUT：阶段切换逻辑不变，摘要来源改为 conversation/messages
  - DELETE：清理 conversation（兼容 thread）

3. 特殊路径补齐
- `MutationApi.post` 当前直接实例化 `OpenAIAssistant`，需改为门面服务。

验收：用户完整走通 Question -> Metrics -> Mutant 三阶段，前端无感。

## Phase 4：前端与文档对齐（1 天）
1. 前端命名去耦合（可选保留 API 路径）
- 文件：`web-client/src/api/experiment.js`
- 将函数名从 `getAssistants/updateAssistants` 逐步改为中性命名（如 `workflowChat*`），保留旧导出别名 1~2 个版本。

2. 文档更新
- `docs/04_api_reference.md`
- `docs/20250419_Web APIs.postman_collection.json`
- `flask-server/experiment/README.md`
- 将 “assistant thread” 改为 “response conversation”；标注兼容字段与弃用时间线。

验收：文档不再误导使用 thread/assistant 概念。

## Phase 5：测试、切流（1.5~2 天）
1. 自动化测试补齐
- 新增：
  - 工具调用循环单元测试
  - conversation 持久化与恢复测试
  - 三阶段端到端流程测试
  - 错误映射回归（401/429/500/504）

2. 回滚策略
- 任意阶段可通过环境变量快速切回 `assistants`。

验收：灰度期关键指标（成功率/错误率）不劣于旧栈。

## 5. 关键风险与处理
1. SDK 版本跨度大
- 风险：从 `openai=1.37.0` 升级后类型/异常行为变化。
- 处理：先引入双栈适配层，避免一次性改全局导入。

2. Tool schema 行为差异
- 风险：Responses 下 function schema/strict 行为与旧栈有差异，可能导致工具调用失败。
- 处理：逐个校验 `prompts/*_functions.json`，必要时补全 JSON Schema 字段并加集成测试。

3. 历史会话可读性
- 风险：旧 thread 消息与新 conversation items 并存，UI 展示可能重复或缺失。
- 处理：以 `chat_messages` 为统一展示层，远端会话仅用于恢复与审计。

4. 清理语义变化
- 风险：conversation 删除接口与 thread 删除语义不同。
- 处理：删除失败不阻断业务，但记录告警并可重试。

## 6. 建议的落地顺序（本项目）
1. 先完成 Phase 0 + Phase 1（不改外部接口）。
2. 再做 Phase 3（核心业务切换），并保留 `/assistants` 路由。
3. 最后做 Phase 2/4 的数据与文档收尾。

> 建议最晚在 2026-06-30 前完成全量切流，留出至少 8 周缓冲，避免逼近 2026-08-26 下线窗口。
