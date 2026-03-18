# EnzyHTP-GPT：Phase 0/1 细化开发方案（Responses 迁移）

基于文档：`/home/shaoq1/bin/EnzyHTP-GPT/.codex/001-response-migration.md`
更新时间：2026-03-17

## 0. 目标与边界

本文件只细化两阶段：
- Phase 0：准备与防回滚设计
- Phase 1：服务层双栈适配

不包含：
- `Experiment` 模型字段迁移（Phase 2）
- `AssistantsApi` 业务逻辑切换（Phase 3）

---

## 1. Phase 0（准备与防回滚）细化方案

## 1.1 交付目标（DoD）
1. 环境可稳定运行 `openai==2.29.0` 且版本信息可追溯。
2. 后端新增运行时开关 `OPENAI_RUNTIME`，默认 `assistants`。
3. OpenAI 调用打点字段统一，至少覆盖：
- `openai_runtime`
- `model`
- `response_id`
- `conversation_id`
- `tool_call_count`
- `openai_error_code`
4. 任意异常可通过环境变量切回 `assistants`，无需改代码。

## 1.2 任务拆解

### 任务 P0-1：依赖与版本固化
- 状态：你已手动安装 `openai==2.29.0`（文档中已标注 DONE）。

验收命令：
```bash
python - <<'PY'
import openai
print(openai.__version__)
PY
```

---

### 任务 P0-2：运行时开关与配置注入
改动文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/config.py`
- `/home/shaoq1/bin/EnzyHTP-GPT/.env.example`
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/services/__init__.py`

新增配置项建议：
```python
OPENAI_RUNTIME = os.environ.get("OPENAI_RUNTIME", "assistants").strip().lower()
OPENAI_RUNTIME_CANDIDATES = {"assistants", "responses"}
if OPENAI_RUNTIME not in OPENAI_RUNTIME_CANDIDATES:
    OPENAI_RUNTIME = "assistants"
```

说明：
- 默认 `assistants`，保证零行为变化。
- 非法值自动回落 `assistants`，避免启动失败。

---

### 任务 P0-3：统一打点协议（先不改业务）
改动文件：
- `/home/shaoq1/bin/EnzyHTP-GPT/flask-server/services/openai_service.py`
- 新增：`/home/shaoq1/bin/EnzyHTP-GPT/flask-server/services/openai_observability.py`

建议新增结构：
```python
@dataclass
class OpenAIMeta:
    openai_runtime: str
    model: str
    response_id: str | None = None
    conversation_id: str | None = None
    tool_call_count: int = 0
    openai_error_code: str | None = None
```

打点时机：
1. API 请求前（记录 runtime/model）。
2. API 返回后（写 response_id/conversation_id/tool_call_count）。
3. 捕获异常时（写 openai_error_code/status 映射）。

日志格式建议：单行 JSON，便于后续接入 ELK/Datadog。

---

### 任务 P0-4：回滚演练脚本
改动文件：
- 新增：`/home/shaoq1/bin/EnzyHTP-GPT/flask-server/dev-tools/check_openai_runtime.py`

脚本输出：
- 当前 SDK 版本
- 当前 `OPENAI_RUNTIME`
- 当前加载服务实现（assistants/responses）
- 最小健康检查（发送一条最简单 prompt，可选 dry-run）

验收标准：
- 修改环境变量后重启服务，脚本可显示运行时已切换。

---

## 1.3 风险与防护
1. `openai` 升级引起异常类行为差异。
- 防护：先保留旧异常映射逻辑；新增异常仅追加不替换。

2. 环境变量未生效导致误判。
- 防护：服务启动日志必须打印 `OPENAI_RUNTIME` 实际值。

3. 观测字段不一致。
- 防护：由 `OpenAIMeta` 统一字段来源，禁止散落拼接。

---

## 1.4 Phase 0 完成定义（Checklist）
- [ ] `environment.yml` 与实际 SDK 版本一致
- [ ] `OPENAI_RUNTIME` 配置可用，默认值验证通过
- [ ] 启动日志输出运行时与 SDK 版本
- [ ] OpenAI 调用日志具备统一字段
- [ ] 运行时回切演练完成并记录

---

## 2. Phase 1（服务层双栈适配）细化方案

## 2.1 目标架构
采用“门面 + 双实现”结构，避免业务层（`agents.py`/`views.py`）直接感知具体 API 栈。

建议目录结构：
- `flask-server/services/openai_service.py`（保留旧实现）
- `flask-server/services/openai_response_service.py`（新实现）
- `flask-server/services/openai_runtime_facade.py`（统一入口）
- `flask-server/services/__init__.py`（导出统一类型）

---

## 2.2 接口契约（先定接口，再迁实现）

定义统一协议 `BaseLLMService`（可用 Protocol/ABC）：
```python
class BaseLLMService(Protocol):
    def ask_gpt(self, prompt: str) -> tuple[bool, int, str]: ...
    def pre_process(self, input_prompt: str) -> str: ...
    def post_process(self, response_content: str, is_finishing: bool) -> str: ...

    # 会话相关（对应 thread/conversation）
    @classmethod
    def get_messages(cls, openai_secret_key: str, session_id: str, limit: int = 20) -> tuple[bool, list[dict]]: ...
    @classmethod
    def get_summary(cls, openai_secret_key: str, session_id: str) -> tuple[bool, str]: ...
    @classmethod
    def delete_session(cls, openai_secret_key: str, session_id: str) -> bool: ...
```

关键点：
- `session_id` 作为抽象名（兼容 thread_id/conversation_id）。
- 先通过适配保持 `agents.py` 侧几乎不改签名。

---

## 2.3 新服务实现：`openai_response_service.py`

### 类设计建议
1. `ResponseRunError`：对应旧 `AssistantRunError`，保留 `code/status`。
2. `ResponseFunction`：可复用 `AssistantFunction` 逻辑，避免 schema 解析重复。
3. `OpenAIResponsesService`：主实现类。

### `OpenAIResponsesService` 的核心方法
1. `ask_gpt(prompt)`
- 入口保持与旧实现一致：返回 `(is_valid, status_code, response_content)`。

2. `_create_response(...)`
- 调用 `client.responses.create(...)`。
- 传入 `model`、`instructions`、`input`、`tools`、`conversation`（如有）。

3. `_extract_text_and_calls(response)`
- 从 output items 中抽取：
  - 文本结果
  - `function_call` 列表

4. `_run_tool_loop(response)`
- 循环处理函数调用直到无待执行 call：
  - 执行本地映射函数
  - 将输出组装为 `function_call_output`
  - 再次 `responses.create(...)` 续跑

5. `get_messages/get_summary/delete_session`
- conversation 语义实现。
- 短期可降级策略：若 conversation items API 不稳定，则回退 `chat_messages` 本地存储。

---

## 2.4 工具调用循环（执行级伪代码）

```python
def ask_gpt(self, prompt: str):
    resp = self._create_response(input=prompt)
    text, calls = self._extract_text_and_calls(resp)

    while calls:
        outputs = []
        for call in calls:
            fn = self.function_map.get(call.name)
            ok, out = fn(**json.loads(call.arguments))
            outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": out,
            })
            self.latest_tool_call_result[call.name] = ok

        resp = self._create_response(input=outputs, conversation=resp.conversation)
        text, calls = self._extract_text_and_calls(resp)

    return True, 200, text
```

注意事项：
- 保持 `latest_tool_call_result` 兼容当前前端展示。
- 对未知函数名返回可读错误，不直接抛裸异常。
- 所有工具输出建议转字符串，避免序列化歧义。

---

## 2.5 门面与导出策略

### 门面：`openai_runtime_facade.py`
职责：
- 根据 `OPENAI_RUNTIME` 实例化 `OpenAIAssistant` 或 `OpenAIResponsesService`。
- 对外暴露与原 `OpenAIAssistant` 同名/同签名入口（最小化调用方改动）。

示例：
```python
def build_openai_agent(*args, **kwargs):
    if OPENAI_RUNTIME == "responses":
        return OpenAIResponsesService(*args, **kwargs)
    return OpenAIAssistant(*args, **kwargs)
```

### `services/__init__.py`
- 导出门面构造器与统一基类；旧类继续导出以保证兼容。

---

## 2.6 错误码映射（必须对齐旧契约）

映射表建议：
- `invalid_api_key/authentication_error/permission_denied` -> `401`
- `insufficient_quota/rate_limit_exceeded` -> `429`
- `timeout` -> `504`
- 其他 OpenAI API 错误 -> `500`

用户可见错误文案要求：
- 保持当前前端依赖的 message 风格，不一次性改文案模板。

---

## 2.7 单元测试与契约测试

新增测试文件建议：
- `flask-server/test/services/test_openai_runtime_facade.py`
- `flask-server/test/services/test_openai_responses_tool_loop.py`
- `flask-server/test/services/test_openai_error_mapping.py`

最小测试集：
1. `OPENAI_RUNTIME=assistants` 时门面返回旧实现。
2. `OPENAI_RUNTIME=responses` 时门面返回新实现。
3. 单工具调用成功。
4. 多轮工具调用成功。
5. 未注册工具函数名的错误处理。
6. 401/429/500/504 映射正确。

---

## 2.8 实施顺序（建议按 PR 切分）

PR-1（基础设施）
- 配置开关
- 观测字段
- 门面骨架

PR-2（Responses 核心）
- `openai_response_service.py`
- 工具循环
- 错误映射

PR-3（兼容与测试）
- `services/__init__.py` 导出调整
- 单元测试补齐
- 文档补充

---

## 2.9 Phase 1 完成定义（Checklist）
- [ ] 新增 `OpenAIResponsesService` 并通过最小调用
- [ ] function tool loop 在 1~2 轮场景可跑通
- [ ] 门面可按 `OPENAI_RUNTIME` 正确切换
- [ ] 旧 `OpenAIAssistant` 路径不受影响
- [ ] 错误码映射与旧接口契约一致
- [ ] 新增测试全部通过

