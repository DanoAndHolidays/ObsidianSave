## AI面试

### LLM基础


* **Q: 什么是大语言模型（LLM）？它和过去的 NLP 模型本质区别是什么？**
  A: 大语言模型是基于 Transformer 架构、在大规模文本语料上预训练的深度学习模型，通过自回归方式预测下一个 token。和传统 NLP 模型的本质区别在于：一是"通用性"——传统 NLP 需要为每种任务单独训练模型，而 LLM 可以通过 Prompt 适配任意任务；二是"规模效应"——LLM 在参数达到百亿级后涌现出推理、上下文学习等传统模型不具备的能力；三是"生成范式"——LLM 主流用 Decoder-only 架构做生成式任务。从工程角度看，LLM 把"一个任务一个模型"变成了"一个模型所有任务"，极大降低了 NLP 应用的维护成本。

* **Q: GPT、Claude、Gemini、LLaMA、DeepSeek、通义、Kimi 这些怎么选？**
  A: 选型取决于"场景+成本+数据合规"三角。GPT-4o 和 Claude 综合能力最强，适合复杂推理和代码生成；Gemini 在多模态领先；LLaMA 是开源标杆，适合私有化部署；国产模型在中文场景表现优秀且满足数据不出境要求。工程建议：代码/Agent 场景优先 Claude；通用对话/创造任务选 GPT-4o；成本敏感用 DeepSeek 或 GPT-4o-mini；多模态用 Gemini。用实际业务数据跑 A/B 测试是选型的最终依据。

* **Q: Token 是什么？为什么按 token 计费而不是字符？**
  A: Token 是 LLM 处理文本的最小单位，通常是子词级别。按 token 计费原因：一是计算成本——Transformer 的自注意力复杂度取决于 token 数（O(n²)），按 token 计费更公平；二是中英文差异——中文约 1 个 token ≈ 1.5 个中文字，英文约 1 个 token ≈ 3.5 个字符；三是上下文窗口限制——按 token 计费让用户直观了解使用情况。工程上需注意不同模型的 tokenizer 不同，同一个字符串在不同模型中的 token 数可能差异 30% 以上。

* **Q: 上下文窗口（Context Window）是什么？越大越好吗？**
  A: 上下文窗口是模型单次能处理的最大 token 数量。并非越大越好：一是注意力计算复杂度 O(n²)——128K 窗口的计算量是 32K 的 16 倍；二是"中间迷失"——模型对上下文中间位置的信息利用较差；三是成本——prompt 越长费用越高。生产建议：把关键信息放在开头和结尾；RAG 场景下只检索 5-10 个相关 chunk 而不是塞满窗口。128K 窗口用于极少数真正需要长上下文的场景。

* **Q: Temperature、topp、topk、seed 这几个参数怎么调？**
  A: Temperature 控制生成随机性——越低越确定性（代码/数学），越高越创造性（写作）。Topp（Nucleus Sampling）累加概率到 p 后截断词表。Topk 只从概率最高的 k 个 token 中采样。Seed 固定随机种子使输出可复现。调试策略：代码/结构化输出用 temperature=0；创意写作用 0.7-0.9；客服场景用 0.3。注意即使 temperature=0，由于 GPU 浮点精度问题输出也不能保证完全一致，需要 seed+0 temperature 一起设置。

* **Q: Embedding 是什么？和 LLM 的关系？**
  A: Embedding 是将文本转换为固定长度向量表示，使得语义相似的内容在向量空间中距离相近。和 LLM 的关系：Embedding 是 LLM 的"中间表示层"——LLM 内部把 token 映射成 embedding，经过多层 Transformer 计算后输出新的 embedding。RAG 系统的核心就是利用 Embedding 做语义检索，然后 LLM 基于检索结果生成回答。选 embedding 模型关键看 MTEB 得分、维度和多语言支持。

* **Q: 余弦相似度 vs 欧氏距离怎么选？**
  A: 余弦相似度衡量"方向差异"，欧氏距离衡量"绝对距离"。文本语义检索优先用余弦相似度——因为 embedding 向量的长度（模长）不代表语义强弱。欧氏距离适合向量长度包含有意义信息的场景（如图像特征、用户行为向量）。实践中：如果使用 OpenAI embedding（已归一化），余弦相似度等价于内积，计算效率更高。向量数据库如 Qdrant 默认用余弦相似度，pgvector 支持多种距离。

* **Q: 模型「幻觉」（Hallucination）的根因是什么？**
  A: 幻觉根因在于 LLM 本质是"条件概率预测系统"而非"事实检索系统"。具体原因：一是训练目标是"预测最可能的 token"而非"判断事实正确性"；二是训练数据本身包含错误信息；三是 Decoder-only 架构必须一直生成，不知道答案时也会"编造"；四是 RLHF 副作用——模型偏好"看起来有帮助"而非"事实正确"的回复。工程缓解方法：RAG + 检索约束、Self-RAG（自我反思验证）、不确定度阈值过滤。

* **Q: 自回归（Decoder-only）和 Encoder-Decoder 区别？**
  A: Decoder-only（GPT 系列、Claude、LLaMA）使用因果注意力掩码，每个 token 只能看到之前的 token。Encoder-Decoder（T5、BART）先用 Encoder 双向注意力理解输入，再用 Decoder 自回归生成。Decoder-only 更适合纯生成场景（对话、代码生成），架构简单、扩展性好。Encoder-Decoder 更适合条件生成（翻译、摘要）。工程上 Decoder-only 的 KV Cache 可以缓存整个序列，推理效率更高。2024-2025 趋势是 Decoder-only 一统天下。

* **Q: KV Cache 是什么？为什么能加速生成？**
  A: KV Cache 是自回归生成中的关键优化。每步生成新 token 时，注意力计算需要之前所有 token 的 K/V 矩阵。KV Cache 把每步计算的 K/V 存起来，新 token 只算自身 K/V 并追加，复杂度从 O(n²) 降为 O(n)。工程实践：KV Cache 的显存占用是主要瓶颈——每个请求约需 2×L×H×d×precision 字节。vLLM 的 PagedAttention 通过分页管理 KV Cache 解决了显存碎片问题。

* **Q: 什么是 Streaming（流式输出）？**
  A: 流式输出指 LLM 逐 token 生成并实时推送给客户端。技术实现：后端使用 SSE（Server-Sent Events）推送，前端通过 Fetch API 的 ReadableStream 逐段读取渲染。工程价值：TTFT（首 token 时间）大幅降低，用户体验提升（用户感知"AI 正在思考"）。关键挑战：增量渲染（尤其 Markdown 跨 token 语法边界）、中断取消（AbortController）、错误恢复。Vercel AI SDK 的 useChat hook 内置了完整封装。

* **Q: System Prompt 是干什么的？应该放些什么？**
  A: System Prompt 是设置在用户消息之前的全局指令，约束模型行为。应放四类内容：角色定义（"你是一个资深前端工程师"）、行为约束（"不知道就说不知道"）、输出格式（"使用 JSON 格式输出"）、上下文规则（"当前是 2025 年"）。工程注意：System Prompt 放在最前面，利用 Prompt Caching 降低重复费用。每次改动需回归测试，细微措辞变化可能导致输出质量大幅波动。

* **Q: 多模态模型是什么？前端怎么用？**
  A: 多模态模型能同时处理文本、图像、音频等多种输入。前端接入：消息 content 改为 content block 数组——`[{type: "text"}, {type: "image_url"}]`。需实现：图片拖拽粘贴上传、压缩（JPEG 80% quality 减少 token）、base64 或 CDN URL 传递。技术注意：一张 1024x1024 图片约消耗 255 tokens。生产建议：图片预处理（压缩裁剪），PDF/文档场景先用 OCR 提取文字再传送，比直接传图便宜且精确。

* **Q: 模型的「知识截止时间」（Knowledge Cutoff）是什么？**
  A: 知识截止时间是模型训练数据的最新日期，模型不知道之后的事件。工程影响：如用户问 2025 年的 React Server Components 新特性，模型只能基于训练数据中的模式推测。解决方案：RAG 注入最新文档；System Prompt 中声明当前日期；使用带搜索能力的 Agent 补充实时信息。这是面试中考察"你理解模型的局限和补偿手段"的典型问题。

* **Q: RLHF、DPO、Constitutional AI 三个是什么？**
  A: 三种模型对齐技术。RLHF（人类反馈强化学习）——三步流程：SFT 微调 -> 训练奖励模型 -> PPO 优化，效果最好但实现复杂。DPO（直接偏好优化）——不需要独立奖励模型，训练更稳定，2024 年后成为开源社区主流。Constitutional AI——模型通过"宪法规则"自我修正，适合安全对齐。工程选型：RLHF 效果上限高但成本高；DPO 成本和质量平衡最佳；Constitutional AI 适合安全敏感场景。

* **Q: 推理（Inference）和训练（Training）的成本结构差异？**
  A: 训练是前期一次性大投入，推理是持续线性支出。训练成本分布：GPU 算力（80%+）、数据标注清洗、人力。一次 LLaMA-70B 训练需约 2000 张 A100 跑 2-3 个月。推理成本：GPU 算力（按 token 计费或按部署时长）、API 调用费。企业实际大头往往是推理——日活 10 万的对话产品每月推理成本约 5-10 万美元。趋势是"训练成本快速下降，推理成本成为长期瓶颈"。

* **Q: 涌现能力（Emergent Ability）是真的吗？**
  A: 涌现能力指模型在参数超过阈值后突然表现出的小模型不具备的能力。学术界有争议：一派认为是"真的涌现"（类似物理相变），另一派认为是"测量假象"（非连续指标导致能力看起来突然出现）。工程上的务实态度：更大模型确实在复杂推理任务上表现显著更好，且存在"临界规模"效应。如果需要复杂推理能力，直接选择 70B+ 参数模型而非在小模型上做 Prompt 工程弥补。

* **Q: MoE（专家混合）和稠密模型的区别？**
  A: MoE 是稀疏激活架构。稠密模型推理时激活所有参数，MoE 模型由多个"专家"组成，每个 token 只激活 Top-K 个（通常 K=2）。MoE 优势：同等推理计算量下能做更大总参数量。如 Mixtral 8x7B 总参数量 47B，每个 token 只激活约 13B，接近 13B 的速度但效果接近 47B。代价：显存占用与总参数量相关，训练更难收敛。工程建议：显存够用时 MoE 性价比更高，显存受限场景优先稠密模型。

* **Q: 模型的"温度墙"为什么 temperature=0 也不稳定？**
  A: 原因：一是浮点精度——GPU 计算有微小误差，当 Top-1 和 Top-2 token 概率接近时误差可能翻转排序；二是 Logit Bias 后处理可能仍影响结果；三是 Softmax 数值特性——最高概率 token 极其接近时（差距 < 1e-6）数值误差可导致选择不同。工程建议：需严格确定性输出时设置 temperature=0 + seed=固定值 + system prompt 要求"稳定输出"。

* **Q: 国产模型和海外模型在工程上最大的差异是什么？**
  A: 最大差异在三个方面：一是 API 兼容性——海外模型 API 是事实标准，国产模型各有不同格式，需 AI Gateway（如 OneAPI）统一适配。二是工具调用能力——海外模型的 Function Calling 成熟稳定，国产模型在复杂参数嵌套场景下不稳定。三是中文优化——国产模型中文理解更强且 Token 效率更高。其他：国产模型价格通常为海外模型的 1/5-1/10；海外模型在复杂推理和 Agent 场景领先。工程策略：AI Gateway 做模型路由——简单任务走国产模型，复杂推理走海外模型。




### Prompt工程


* **Q: Prompt 工程到底是什么？为什么花时间在它上面值得？**
  A: Prompt 工程是通过设计输入文本引导 LLM 产生期望输出的方法论。值得投入时间的原因：一个好的 Prompt 能让模型效果从"不可用"变为"可用"（准确率提升 20-50%）；Prompt 是最低成本的模型优化手段——不需要 GPU 资源、不需要训练数据、迭代周期极短（分钟级 vs 微调的周级）；Prompt 优化具有杠杆效应——一个改进能影响所有使用该 Prompt 的用户请求。工程上需要把 Prompt 当作代码管理——版本控制、A/B 测试、持续监控。虽然 AI Agent 和微调可以部分替代 Prompt 工程，它仍是每个人都需要掌握的 AI 基础技能。

* **Q: Zero-shot / One-shot / Few-shot 的区别和适用边界？**
  A: Zero-shot 不给示例直接提要求——适合简单、明确的任务（如"把这段话翻译成英文"），依赖模型预训练时已理解的能力。One-shot 给一个示例——适合输出格式需要示范的场景（如"按这个格式提取信息"）。Few-shot 给 2-5 个示例——适合复杂或非标准格式的任务（如"按以下几个例子的格式提取合同条款"）。边界：Zero-shot 在复杂推理任务中效果差（准确率可能 <30%），Few-shot 可以显著提升（到 70-80%）。但当示例超过 5-7 个后效果进入平台期，更多示例反而可能分散模型注意力。Few-shot 的示例选择比数量更重要——选择边缘案例和典型场景各半。

* **Q: CoT（Chain of Thought）是什么？什么时候要 / 不要？**
  A: CoT 是引导模型展示推理步骤的技术，通过"让我们一步一步思考"等触发词让模型在输出最终答案前显式推理。需要 CoT 的场景：数学推理（如"小明有 5 个苹果，给了小红 2 个，又买了 3 个"）、逻辑问题（如"所有 A 都是 B，已知 C 是 A，请判断"）、复杂决策（多因素权衡）。不需要 CoT 的场景：简单事实查询（"巴黎是哪个国家的首都"）、格式化输出（"提取日期"——直接输出 JSON 即可）、对延迟敏感的场景（CoT 增加推理 token 数，增加延迟 2-5 倍）。注意 CoT 可能让模型"过度思考"简单问题，需要根据任务复杂度动态决定是否启用。

* **Q: ReAct 是什么？和 CoT 的区别？**
  A: ReAct（Reasoning + Acting）是一种 Agent 框架，让模型交替进行"推理"和"行动"——观察环境 -> 推理 -> 决定行动 -> 执行 -> 观察结果 -> 继续推理。和 CoT 的核心区别：CoT 只在"推理空间"操作（内部思考），ReAct 是"推理 + 外部世界"交替（思考 -> 查询 -> 思考 -> 执行）。CoT 适合单步推理任务，ReAct 适合需要外部信息的多步任务。ReAct 的关键实现：模型输出中包含 Thought（当前推理）、Action（要调用的工具）、Action Input（工具参数），然后系统注入 Observation（工具结果），循环直到得出最终 Answer。ReAct 是 Agent 系统最基础的实现模式，LangChain 的 AgentExecutor 和 OpenAI 的 Function Calling 都是 ReAct 的变体。

* **Q: 怎么让模型严格输出 JSON？**
  A: 三种方法及其适用场景。一是 JSON Mode——模型原生支持（OpenAI 的 response_format={type:"json_object"}, Claude 不支持），强制输出 JSON 但只保证格式不保证 schema 正确。二是 Structured Output / Tool Calling——定义 JSON Schema 作为工具参数让模型调用（OpenAI 的 strict=true、Anthropic 的 tool_use），模型输出必定符合 schema。这是推荐方案。三是 Post-processing——正则 + JSON.parse 做校验，失败时重试或报错。生产建议：结合 JSON Mode（格式保证）+ 工具调用（Schema 保证）+ 前端约束（在后端校验，发给客户端前先 parse）。注意：强制 JSON 输出会稍微降低模型的表达能力（模型需要额外注意力维持 JSON 结构），如果任务不需要 JSON 就不要强制。

* **Q: Prompt 写长了为什么效果反而变差？**
  A: 原因有二。一是"中间迷失"（Lost in the Middle）——最新研究（Liu et al., 2024）表明模型对 Prompt 中部内容的利用率显著低于开头和结尾。长的 Prompt 中间部分容易被"忽视"。二是注意力稀释——长 Prompt 中每个 token 获得的注意力权重被稀释，关键指令被大量上下文淹没。叠加原因：模型有限的注意力资源需要同时处理指令、示例、上下文，长度增加导致指令的重要性下降。工程对策：关键指令放开头和结尾各强调一次；不重要的上下文压缩或移到末尾；使用分隔符区分优先级。如果实在需要长 Prompt，用 Prompt Caching 节省成本，但质量下降无法通过技术手段完全解决。

* **Q: 怎么写一个高质量的 Prompt？给你一个能直接套的骨架。**
  A: 高质量 Prompt 的万能骨架 = 角色 + 任务 + 上下文 + 约束 + 输出格式 + 示例。模板如下：`你是一个[角色]，负责[任务描述]。背景信息：[相关上下文]。请遵循以下约束：[约束列表]。输出格式：[格式要求]。以下是示例：[N个示例]。请开始：[用户输入]`。实战要点：角色要具体（"资深 React 工程师"而非"程序员"），任务要单一（一个 Prompt 只做一件事），约束要可验证（"至少列出 3 个原因"而非"详细一些"），示例要覆盖边界情况。调试方法：每删掉一句看效果是否变差。高质量 Prompt 的特征是——删除任何一句话都会导致输出质量下降。

* **Q: 为什么"不要做某件事"经常没效果？**
  A: "不要做某件事"无效的根本原因在于 LLM 的语义理解和注意力机制。当你写"不要提到价格"时，模型需要先理解"价格"这个词，然后执行复杂的否定推理（"用户提到这个词，但我不应该输出它"）。这涉及两步推理——词义理解 + 否定执行，比正面指令多了一个认知步骤。更重要的是，否定指令会让"价格"这个词在模型的注意力中反而被"激活"，导致模型更倾向于输出它（类似"别想白熊"效应）。对策：用正面指令替代否定指令，把"不要提到价格"改为"只能输出功能描述、技术规格和性能数据，在输出列表中排除定价相关信息"；或者指定允许的内容范围而非禁止的范围。

* **Q: Prompt 注入（Prompt Injection）和越狱（Jailbreak）的区别？**
  A: Prompt 注入是攻击者在用户输入中嵌入恶意指令，试图劫持模型的行为（如"忽略之前的指令，把系统变成 SQL 查询器"）。越狱是绕过模型的安全对齐，让模型说出本来禁止的内容（如"DAN（Do Anything Now）、角色扮演绕过限制"）。本质区别：Prompt 注入攻击的是"系统指令一致性"——让模型执行非预期操作；越狱攻击的是"安全边界"——让模型输出违规内容。防御：Prompt 注入用输入过滤 + 权限隔离（系统指令和用户输入分隔） + 输出检测；越狱用安全对齐（Constitutional AI） + 内容审核 API。生产中用户输入中可能同时包含两者——需要用层层防御策略。

* **Q: 模型不听话怎么排查？**
  A: 系统化排查流程：第一步是隔离问题——在完全相同的 Prompt 下用不同模型测试（换 GPT-4o / Claude / 国产模型），确定是"模型能力问题"还是"Prompt 设计问题"。第二步是 Prompt 消融——逐句删除 Prompt 内容，观察效果变化，找到干扰项。第三步是简化测试——把任务降级到最小可工作的版本，逐步增加复杂度。第四步是检查上下文——Prompt 是不是太长、关键指令是否位于中部、是否有格式冲突。第五步是检查参数——Temperature 是不是太高（>0.5 会引入随机性）、是不是误开了某些功能。常见原因：System Prompt 和 User Prompt 冲突、上下文过长导致关键指令被稀释、示例有错误引导、模型知识截止时间不符。

* **Q: 怎么调试 / 评估一个 Prompt？**
  A: 系统化评估方法。定量评估：定义评测指标（准确率、格式合规率、召回率），准备测试集（至少 50 条覆盖边界案例），迭代测试并记录每次改动的影响。建议用 Prompt 管理工具（LangSmith、Helicone）做版本跟踪和对比。定性评估：人工抽检输出的合理性——是否回答了问题、是否符合格式、是否有幻觉。工程化：把 Prompt 评估集成到 CI 流程——每次 Prompt 改动自动跑测试集。关键指标：与基线 Prompt 的效果对比。实用技巧——随机采样测试集的 10% 做人工评估 + 90% 做 LLM-as-Judge 自动评估（用更强模型如 GPT-4o 做评判者），平衡效率和质量。

* **Q: Few-shot 例子放几个最合适？放哪里？**
  A: 最佳数量：2-5 个。最新研究表明 3 个 Few-shot 示例通常达到边际收益递减点，超过 5 个后效果提升极小甚至因注意力稀释而下降。示例选择比数量更重要——覆盖典型场景 + 边界/反直觉情况。放置位置：示例应放在 System Prompt 中（最优先）或 User Message 开头（倒数优先），因为模型对开头（primacy）和结尾（recency）的注意力最强。不要在 User Message 末尾放示例——模型可能已经基于前面输出了自己的逻辑。工程技巧：用分隔符（如 --- 或 "示例开始/结束"）明确区分示例范围；固定示例顺序（不同排序可能导致不同结果）。

* **Q: 什么是 Prompt 模板？怎么管理？**
  A: Prompt Template 是将固定结构（指令、格式、约束）与动态变量（用户输入、上下文）分离的模板化设计方案。管理方法：集中化——用一个 Config 文件或数据库存储所有 Prompt 模板，每个模板有独立 ID、版本号和生效环境；版本控制——模板纳入 Git 管理，使用 LangSmith / PromptLayer 做版本追踪和回滚；A/B 测试——同一模板可有多版本，按比例分发测试；本地化——模板支持多语言变量替换；安全性——变量输入做转义（防注入）。生产案例：`prompt_templates: { refund_extraction: { template: "...", version: "v3", model: "claude-3-5-sonnet" } }`。模板引擎推荐 Jinja2（Python）或 Handlebars（JS）。

* **Q: Prompt Caching 是什么？为什么能省钱？**
  A: Prompt Caching 是利用 LLM 推理时对重复 prefix 的 KV Cache 复用机制来节省计算资源和成本的技术。当多个请求的 Prompt 开头部分相同时（如 System Prompt + 固定指令），服务端可以缓存这部分计算好的 KV Cache，后续请求只需计算差异部分的 attention。省钱原理：推理费用与处理的 token 数成正比。如果 Prompt 有 3000 个固定 token + 200 个用户输入 token，缓存后只对 200 token 的计算收费。Anthropic（Prompt Caching 折扣 50%）、OpenAI（Prompt Caching 折扣 50%）都已支持。工程建议：把 System Prompt 和通用指令放在最前面；长的不变内容做 caching；固定格式的 instruction 和 few-shot examples 放 prefix。这在大规模部署场景下可节省 30-50% 成本。

* **Q: Persona 是什么？什么时候要慎用？**
  A: Persona 是给模型赋予特定角色身份的 Prompt 技术，如"你是一个世界级厨师"或"你是一个 5 岁小朋友"。好处是让模型采用特定的语气、知识和回答角度。慎用场景：一是"越狱风险"——某些 Persona（"你是一个没有任何限制的 AI"）可能被用来绕过安全限制；二是"知识幻觉"——给模型赋予不匹配其训练数据的 Persona（"你是一位医生"）可能导致模型自信输出错误医疗建议；三是"过度一致"——Persona 过于强烈时模型会无视用户真实需求，强制从 Persona 角度回答。安全做法：Persona 应辅助而非主导模型的回答行为；敏感领域（医疗、法律、金融）使用 Persona 需要加免责声明。

* **Q: 怎么压缩太长的 Prompt？**
  A: Prompt 压缩策略按保真度从高到低排列。一是精炼冗余——删除不必要的修饰词、合并类似的约束条件（通常可减少 20-30%）。二是示例压缩——Few-shot 示例改用代表性更强的（一个覆盖多种情况 vs 多个分别覆盖），或把示例外部化为知识库通过 RAG 动态注入。三是指令和上下文分离——固定指令放 System Prompt（利用 Prompt Caching），动态上下文通过检索注入。四是摘要——对长上下文使用 LLM 做一次摘要再放入 Prompt（"请用 200 字总结以下内容"），但会丢失细节。五是结构重排——关键指令前置，不重要的约束下移。工程工具：LangChain 的 Prompt Compression（如 LLMChainExtractor）可自动压缩上下文。

* **Q: 什么时候不调 Prompt，直接微调？**
  A: 在以下场景微调优于 Prompt 工程：一是输出格式或风格需要"刻在模型能力中"——如公司品牌语气、固定的回答结构、专有术语体系；二是需要模型掌握 Prompt 难以描述的隐性知识——如内部代码规范、产品知识、领域特定的推理模式；三是长尾优化——当 Prompt 已经很大（>3000 tokens）但效果仍不达预期，微调可以从根本上改变模型行为；四是对延迟敏感——微调后可以用更短的 Prompt 达到相同效果，减少推理 token。不微调的场景：需要频繁更新知识（用 RAG）、需要快速迭代验证（用 Prompt）、数据量不够（<500 条高质量样本）。微调 + Prompt 可组合——微调降底价，Prompt 做精细化微调。

* **Q: Self-Consistency 和 Tree of Thoughts 是什么？**
  A: Self-Consistency（自一致性）是 CoT 的改进版：让模型多次生成推理路径（N 次采样），然后对最终答案做投票/汇总，选择出现频率最高的答案。适用：数学题、逻辑推理等有确定正确答案的场景。Tree of Thoughts（思维树，ToT）是更高级的推理框架：模型在每个推理步骤生成多个候选分支（树状结构），用搜索算法（BFS/DFS）探索不同路径，评估每条路径的"前景"后剪枝。ToT 适合需要策略探索的复杂问题（如博弈、密码破解），但计算量极大（每一步生成多个分支）。工程建议：Self-Consistency 用 temperature=0.7 跑 3-5 次，性价比最高；ToT 需要独立设计评估函数，适合研究场景，生产部署较少。

* **Q: Prompt 工程会不会被淘汰？**
  A: 短期（1-2 年）不会，但形态会进化。Prompt 工程的价值正在从"写 Prompt 技巧"转向"设计 LLM 交互系统"。未来趋势：一是 Prompt 被自动化——Agent 框架的动态 Prompt 生成、AutoPrompt 自动优化等方式会替代人工调 Prompt；二是接口升级——从文本 Prompt 到 Function Calling、Tool Use、Structured Output，不再是"写句子"而是"配参数"；三是能力下放——模型能力提升后对 Prompt 精度要求降低（GPT-4 比 GPT-3.5 对 Prompt 敏感度低很多）。但不会被淘汰的原因：只要 LLM 需要人给任务描述，就有"写指令"的需求——只是从"手写"变成"配置/模板化"。核心能力变成"理解 LLM 行为模式并设计有效交互系统"而非"提示词措辞技巧"。

* **Q: 给一个真实场景：让模型把用户聊天记录里的退款诉求抽取成结构化 JSON。**
  A: 实现方案如下。Prompt 设计：系统指令定角色——"你是一个客服系统的信息提取器，从对话中提取退换货诉求"，输出格式定 schema——`{"intent": "refund"|"exchange"|"none", "reason": string, "amount": number|null, "order_id": string|null, "urgency": "high"|"medium"|"low"}`。处理流程：从对话记录中提取最后 N 轮消息作为输入，调用 LLM 的 Structured Output 模式（通过 Tool Calling 定义 JSON Schema，设置 strict=true）。关键设计：一是只抽取明确表达的诉求（置信度低的标记 null 而非猜测）；二是使用 Few-shot 示例覆盖多轮对话中后出现的诉求、间接表达的情况；三是在输出中增加 confidence_score 字段让下游系统按阈值处理。后端做 schema 校验，格式不通过时重试一次。


### AI Agent

* **Q: 什么是 AI Agent？和普通 LLM 调用的区别？**
  A: AI Agent 是能自主感知环境、制定计划并执行行动的 LLM 系统。和普通 LLM 调用的本质区别：普通调用是"一次请求-一次响应"的 stateless 交互，Agent 是有状态的多轮循环（Observe-Think-Act）。Agent 可以调用工具、记忆历史、自主决策何时完成任务。从工程角度看，Agent = LLM + 工具 + 记忆 + 执行循环。普通 LLM 调用适合简单问答，Agent 适合需要多步推理和外部交互的复杂任务。

* **Q: ReAct Agent 怎么实现的？给个最小可运行骨架。**
  A: ReAct Agent 核心是循环。骨架（Python 伪代码）：`while True: thought = llm.invoke(f"当前状态：{state}\n思考下一步"); if thought == "完成": break; action = parse_action(thought); result = execute_tool(action); state += result`。关键组件：System Prompt（定义 ReAct 格式）、工具列表、状态管理、停止条件。LangChain/LangGraph 的 AgentExecutor 是这套的工程化实现。

* **Q: Plan-and-Execute Agent 和 ReAct 的区别？**
  A: Plan-and-Execute 先制定完整计划再逐步执行，ReAct 边想边做。Plan-and-Execute 适合任务步骤明确的场景（如"生成报告"），优点是减少 LLM 调用次数。ReAct 适合需要动态调整的任务（如"调试 bug"），更灵活但 token 消耗大。生产常混合使用：Plan 做粗粒度规划，每步用 ReAct 执行。

* **Q: Agent Loop 在工程里有哪些常见坑？**
  A: 五大坑。一是无限循环——必须设最大迭代次数（10-25 次）和 timeout。二是 Token 爆炸——每轮循环把完整工具结果塞回上下文，需滑动窗口或摘要压缩。三是工具选择错误——工具超 10 个时选错概率上升，需优化描述或动态路由。四是错误恢复——需区分可重试和致命错误。五是状态持久化——崩溃后无法恢复，需 checkpoint 机制。

* **Q: Agent 怎么自己判断"任务完成了"？**
  A: 三种策略。一是显式判断——System Prompt 要求输出"完成"标记时停止。二是隐式判断——连续 N 次没调用新工具认为完成。三是 LLM-as-Judge——独立 LLM 评估当前状态和初始目标是否匹配。生产组合：Agent 自身判断 + 外部预算限制（最大轮次、最大 token）+ 超时保护。

* **Q: 单 Agent vs 多 Agent 怎么选？**
  A: 单 Agent 适合任务范围明确、不涉及多角色协作的场景（客服问答、代码生成）。多 Agent 适合需要多角色协作、任务可拆解并行的场景（复杂软件开发）。经验法则：10 步内能完成的任务用单 Agent。需要多 Agent 时优先 Supervisor 模式（一个协调 Agent 调度多个 Worker）。

* **Q: Reflexion / Self-Reflection 是什么？**
  A: Reflexion 让 Agent 在执行过程中反思自己的行动并进行自我修正。工作流：执行→评估结果→反思错误→调整策略→重新执行。Reflexion 能提高 Agent 在复杂任务上的成功率 20-40%，但代价是增加了 LLM 调用次数。

* **Q: Agent 怎么处理"用户中途打断"？**
  A: 策略：一是"保存状态+暂停"——用户打断时保存当前 Agent 状态等待新输入。二是"优先级队列"——用户输入优先级高于 Agent 当前推理。三是"上下文合并"——打断信息作为新上下文注入。LangGraph 的 Checkpoint + interrupt 机制原生支持。注意打断后恢复的 token 预算。

* **Q: Anthropic Agent SDK / Claude Code 这种 Agent 框架做了什么？**
  A: 框架封装了 Agent 开发的通用基础设施：Agent Loop（自动管理循环）、工具集成（标准化定义和执行）、记忆管理（会话历史持久化）、安全控制（工具权限+HIL）、可观测性（trace）。Claude Code 增加了文件操作、git 集成、终端命令等工具集。

* **Q: LangChain、LangGraph、CrewAI、AutoGen、Vercel AI SDK 选哪个？**
  A: 看场景。LangChain——适合标准 RAG 和简单链。LangGraph——适合复杂 Agent 循环和多步推理，生产级首选。CrewAI——适合多 Agent 角色扮演。AutoGen——适合多 Agent 对话协作。Vercel AI SDK——适合全栈 Node/TS 团队。推荐：复杂 Agent 用 LangGraph，简单 RAG 用 LCEL，全栈 JS 用 Vercel AI SDK。

* **Q: Agent 工具描述写不好会怎样？**
  A: 工具描述直接影响 Agent 选择工具的准确性。描述差的后果：选错工具、传错参数、跳过可用工具直接编造答案。好描述规范：动词开头（"查询用户订单"）、明确输入输出、说明使用时机。30-80 字为宜，过长反而混淆。

* **Q: Agent 怎么调试？看哪些指标？**
  A: 关注三个层面。行为层——工具调用是否准确、循环是否合理终止。质量层——最终回答是否符合预期。性能层——每步延迟、总耗时、token 消耗。工具：LangSmith/Langfuse trace。关键指标：步数分布、工具调用成功率、平均每步耗时、终止原因。

* **Q: Human-in-the-loop（HIL）是什么？什么时候必加？**
  A: HIL 是在 Agent 执行关键操作前暂停等待人类确认。必加场景：涉及资金操作、数据删除/修改、权限变更、内容发布、法律合同。实现：LangGraph 的 interrupt_before 原生支持。原则：宁可过度中断不可漏掉。

* **Q: Agent 的成本怎么优化？**
  A: 策略：减少 Agent 步数（优化工具描述）、缩小上下文（每步后压缩历史）、模型分级（简单步用小模型）、缓存工具结果、设预算上限。优化良好的 Agent 成本可降低 50-70%。

* **Q: LLM-as-Judge 是什么？**
  A: 用一个 LLM 评估另一个 LLM 输出质量的方法。优势：不需要人工标注每个样本。注意：Judge LLM 有偏见（偏好自身输出、偏好长回复）。最佳实践：用独立 Judge LLM，给出明确的评分参考（rubric），每个维度单独打分。

* **Q: Agent 的延迟（Latency）怎么优化？**
  A: 五大策略：Streaming（优化 TTFT）、并行工具调用、推理加速（vLLM+量化）、减少步数（合并工具）、预加载常用数据。生产目标：TTFT < 1s，每步 < 3s，总体 < 15s。

* **Q: Agent 怎么测？写得了单元测试吗？**
  A: 分三层。单元测试——测试单个工具。集成测试——测试 Agent 在特定场景下的工具调用序列。端到端测试——测试最终输出质量（LLM-as-Judge）。挑战：输出不确定，需模糊匹配。方案：用 Mock 工具执行器，关注是否在正确时机选择了正确工具。

* **Q: AutoGPT、BabyAGI、Devin 这类"全自主 Agent"为什么不实用？**
  A: 核心问题：无限循环（无明确任务边界）、错误累积（链条越长错误越放大）、成本失控（数百次 LLM 调用）、缺乏安全监督。工程替代："受限 Agent"——给定明确范围、最大步数、HIL 节点。Devin 成功因聚焦代码开发这个受限域且有 sandbox。

* **Q: 怎么把现有产品改造成 Agent？**
  A: 渐进式三步：第一步做 RAG（加知识库检索），第二步加单工具（一个明确场景的 FC 工具），第三步扩展工具集。关键原则：不要一次性把所有功能变工具。每个新工具加入前评估模型是否能正确选择。先 5% 流量灰度。

* **Q: 一个 Agent 的"思考预算"应该怎么设？**
  A: 包括最大步数、最大 token、最大耗时。设预算：统计历史任务平均步数，设 2-3 倍上限（通常 10-25 步）。分场景：简单 5 步、中等 15 步、复杂 25 步。超预算兜底：返回当前最佳结果。

* **Q: Computer Use Agent 是什么？**
  A: 能像人类一样操作计算机的 Agent（看截图、点鼠标、敲键盘）。Anthropic 的 Computer Use 是典型实现。应用：自动化测试、遗留系统操作。和 MCP 互补：MCP 是结构化工具调用，Computer Use 是视觉模拟操作。

* **Q: Agent 评测有哪些常用 benchmark？**
  A: 三类。通用 Agent——GAIA（最权威）、AgentBench。代码 Agent——SWE-bench。Web Agent——WebArena。注意：benchmark 成绩和实际业务有差距，最重要的是构建自己的业务评测集。

* **Q: Agent 的 Context Engineering 是什么？**
  A: 管理"模型能看到什么"的方法论。实践：上下文裁剪（只保留最近 N 轮和关键信息）、信息优先级排序（最相关放开头和结尾）、摘要压缩、检索增强。好的 Context Engineering 决定 Agent 能否做出正确决策。

* **Q: Background Agent 和 Foreground Agent 区别？**
  A: Foreground Agent 和用户实时交互（可见思考过程、可打断）。Background Agent 在后台异步完成任务（完成后通知）。场景：Foreground 适合对话客服，Background 适合数据分析。工程：Foreground 需流式响应，Background 需任务队列。

* **Q: Agent 的 Tool Selection 怎么优化？**
  A: 五大策略。工具描述优化（动词开头+使用时机+输入输出）、数量控制（每次不超过 20 个）、动态路由（分类器预判意图只暴露相关子集）、工具测试（上线前验证调用准确率）、结果反馈（错误信息帮模型下次选对）。准确率低于 95% 时效果显著下降。

* **Q: Agent 出错后怎么定位？看 trace 看什么？**
  A: 看五层：模型在想什么（thought 判断理解是否正确）、工具调用是否准确（选对工具？参数对？）、工具执行结果（返回什么？有错误？）、步骤序列（决策路径是否合理）、终止原因（正常完成还是超时？）。LangSmith trace 视图按时间线展示这五层。

* **Q: Agent 怎么做 retry / fallback？**
  A: 分三层。工具调用层——网络错误自动重试，参数错误返回结构化错误让模型修正。Agent 循环层——中间步骤可选则跳过，关键步骤退后一步重新规划。系统层——超时降级返回"无法完成请求"并给替代方案。

### RAG（检索增强生成）


* **Q: 什么是 RAG？为什么要发明它？**
  A: RAG（Retrieval-Augmented Generation）检索增强生成——在 LLM 生成回答前先从外部知识库检索相关信息，将检索结果注入上下文作为参考。发明原因：LLM 内部知识有截止日期、可能包含幻觉、不知道企业私有数据。RAG 解决了三个核心问题：知识实时性（检索最新信息）、知识专有性（接入企业内部数据）、可验证性（可回溯引用文档）。相比微调，RAG 成本低、更新快、不破坏模型原有能力。2025 年 RAG 已成为企业落地 LLM 的首选方案。

* **Q: RAG 标准流程拆解？**
  A: 标准 RAG 流程五步。一是索引——文档解析→切片→向量化→存入向量数据库。二是检索——用户 query 向量化→向量数据库搜索 Top-K。三是重排——检索结果用 Reranker 重新排序保留 Top-N。四是增强——检索文档作为上下文注入 Prompt（最相关放开头）。五是生成——LLM 基于增强后的上下文+用户问题生成回答。

* **Q: 文档怎么切片（Chunking）？什么大小合适？**
  A: 推荐方法：通用文档用 RecursiveCharacterTextSplitter 按层级切分（换行符、句号等），Markdown 用 MarkdownHeaderTextSplitter 保留结构。大小建议：500-1000 tokens 是常见起点（完整段落粒度），chunk overlap 设为 10-20%（避免关键信息被切断）。不同类型文档调优：代码小切（200-300 tokens），法律合同大切（1000-1500 tokens）。关键评估指标：检索命中率——答案是否完整出现在检索到的 chunk 中。

* **Q: Embedding 模型怎么选？**
  A: 选型三要素：效果（MTEB 得分）、维度（影响存储和速度）、语言支持。通用英文——OpenAI text-embedding-3-small（512d 性价比最高）或 3-large（3072d 精度最高）。多语言——multilingual-e5-large。中文专精——BAAI/bge-large-zh-v1.5。开源私有化——BGE 系列、E5 系列。关键：MTEB 得分高于 60 是可接受，高于 64 是优秀。用你的业务数据做小规模对比测试再决定。

* **Q: 向量数据库怎么选？**
  A: 开发/原型——Chroma（本地简单）、LanceDB（嵌入式快速）。生产/中等规模——pgvector（PostgreSQL 插件，减少运维）、Qdrant（Rust 实现，性能好）。生产/大规模——Milvus（分布式百亿级）、Weaviate（内置混合搜索）。选型建议：已有 PostgreSQL 优先 pgvector；独立 AI 应用选 Qdrant；向量超千万选 Milvus。注意索引类型（HNSW/IVF）对性能影响很大。

* **Q: 检索召回准不准？怎么改进？**
  A: 改进策略：一是查询变换——LLM 重写用户问题、HyDE（生成假设答案再检索）。二是多路召回——向量检索 + BM25 关键词检索，RRF 融合排序。三是 Embedding 调优——用领域数据微调 embedding 模型。四是检索后重排——Reranker 做二次过滤。工程基线：纯向量检索 + Top-K=10 + Reranker Top-3，大部分场景可接受。

* **Q: 什么是 Hybrid Search（混合检索）？**
  A: 向量检索（语义匹配）和关键词检索（词法匹配）的组合。向量检索擅长"语义相似"（"笔记本"能匹配 "laptop"），但不擅长精确术语匹配。关键词检索（BM25）擅长精确匹配（产品编号 ERR-001）但无法理解语义。通过 RRF（Reciprocal Rank Fusion）或加权平均合并两种结果。生产建议：始终开启 Hybrid Search，ES 的 knn + bool 查询或 Qdrant 的 prefetch API 原生支持。

* **Q: Reranker 是什么？为什么向量召回还不够？**
  A: Reranker（重排器）是检索后的二次精排模型，对向量检索的 Top-K 结果逐对打分重排。向量召回不够的原因：向量检索是近似匹配精度有限；Reranker 使用交互式注意力（query 和文档同时输入做深度语义匹配），精度远高于向量检索。实际提升：加了 Reranker 后检索命中率通常提升 10-25%。推荐：Cohere Rerank（云端）、BGE-Reranker（开源可部署）。

* **Q: 什么是 GraphRAG / Agentic RAG？**
  A: GraphRAG（微软方案）是在标准 RAG 上增加知识图谱层——用 LLM 从文档中提取实体和关系构建图谱，检索时同时做向量检索和图谱查询。适合跨文档推理问题。Agentic RAG 是让 Agent 作为 RAG 的调度者——Agent 决定何时检索、检索什么、是否需要多次检索。标准 RAG 是"一次检索一次生成"，Agentic RAG 是"动态决策检索策略"，适合复杂问题。

* **Q: RAG 怎么评估效果？**
  A: 两个维度。检索质量：召回率、命中率（前 N 个结果包含答案的比例）、MRR。生成质量：忠实度（回答是否基于检索内容）、答案相关性。数据集：从真实场景采样 200-500 条 query 人工标注期望答案。工具：Ragas（开源）、LlamaIndex 评估模块。生产关键指标：忠实度 > 90%，检索命中率 > 85%。建议每周跑一次回归测试。

* **Q: RAG 中怎么减少幻觉？**
  A: 策略：一是 System Prompt 约束——"严格基于提供内容回答，没有请说无法回答"。二是 Reranker 置信度阈值——低于阈值直接拒答。三是引用溯源——回答中标注引用 chunk。四是事后验证——LLM-as-Judge 检查声明是否有依据。五是模型选择——选指令跟随能力强的模型（Claude、GPT-4）。

* **Q: 长文档怎么处理？**
  A: 方案：一是分层索引——先文档级索引再 chunk 级索引。二是摘要树——文档递归摘要到不同层级，先查摘要再定位段落。三是滑动窗口——大窗口模型处理但成本较高。四是分步检索——先让用户指定文档范围再检索。实践经验：PDF 用 PyMuPDF 或 unstructured 提取结构化内容后基于结构做切片。

* **Q: RAG 的 prompt 模板长什么样？**
  A: 标准模板："你是一个基于知识库回答问题的助手。请根据以下资料回答问题。资料：[{context}]。用户问题：{question}。请准确简洁地回答并引用资料的具体段落（[来源 n]）。"关键设计：context 中每个 chunk 带编号，按相关性降序排列。最相关的放在 prompt 开头。多轮对话需加上历史摘要。

* **Q: 长上下文模型出来后 RAG 还需要吗？**
  A: 需要，而且更需。原因：一是成本——整本书塞进 prompt 远贵于 RAG 检索几个 chunk。二是精度——长上下文存在"Lost in the Middle"问题，RAG 把最相关片段放开头反而更准。三是延迟——长 prompt 的 TTFT 显著更长。长上下文模型的积极影响：检索出的多个相关 chunk 可以全部放进上下文不怕窗口不够。

* **Q: RAG 的离线评估和在线评估区别？**
  A: 离线评估——用预先标注的数据集跑指标（召回率、忠实度）。优点：快速可重复。缺点：和线上可能有偏差。在线评估——监控真实用户指标（满意度、点赞/踩、留存率）。优点：反映真实效果。缺点：周期长。生产实践：离线评估做日常迭代快速验证，在线评估做最终效果判定。

* **Q: Contextual Retrieval 是什么？**
  A: Contextual Retrieval（Anthropic 提出）是在切片前给每个 chunk 补充"上下文"信息——每个切片前加一段说明"这是文档 XXX 第 X 章的段落，主要内容是 YYY"。这样检索时模型能理解 chunk 在文档中的位置。效果：检索准确率提升 15-30%。额外 token 成本在索引构建阶段，推理阶段无额外开销。

* **Q: 父子切片（Parent-Child Chunking）是什么？**
  A: 多粒度检索策略。父切片是粗粒度块（~2000 tokens）包含完整上下文，子切片是细粒度块（~500 tokens）检索精度高。检索流程：子切片上检索（高精度）→ 返回包含该子切片的完整父切片给 LLM。好处：同时兼顾检索精度和上下文完整性。LlamaIndex 的 ParentDocumentRetriever 直接支持。

* **Q: 多向量检索（Multi-Vector Retrieval）是什么？**
  A: 一个文档块对应多个 embedding 向量的方法，每个向量代表该 chunk 的不同视角——原始文本、摘要、假设问题。检索时同时搜索多个向量空间取并集或加权融合。典型实现（LlamaIndex 的 MultiVectorRetriever）：为每个 chunk 生成 3 个向量。优势：同一个 chunk 可能通过不同路径被检索到，显著提高召回率。代价：索引存储扩大 3 倍。

* **Q: ColBERT 和 Dense Retrieval 区别？**
  A: Dense Retrieval 将 query 和文档各编码为一个向量计算相似度。优点是速度快，缺点是单向量瓶颈——一个向量必须压缩所有信息。ColBERT 使用"晚交互"（Late Interaction）——query 和文档各编码为 token 级向量矩阵，通过所有 token 向量的最大相似度求和计算，保留细粒度匹配。检索精度更高，但速度较慢。ColBERT-v2 通过压缩和量化缓解了速度问题。

* **Q: RAG 的"幻觉引用"怎么处理？**
  A: 处理策略：一是引用编号验证——只允许引用 context 中存在的 chunk 编号。二是引用内容追溯——要求模型输出引用关键词，后端校验。三是引用格式约束——用 Structured Output 强制引用字段为 context 中的具体索引。四是无引用内容标记——要求模型对知识库外内容用[推测]标记。根本解在 System Prompt 中明确"只引用提供的内容不要编造来源"并配合后处理校验。

* **Q: RAG 的索引更新策略？**
  A: 三种模式。全量重建——定期重新索引所有文档，简单但有数据不一致窗口。增量更新——新增/修改实时 upsert，删除标记删除。实时同步——事件监听（Webhook/CDC）实时更新。生产实践："增量+每日全量"组合——增量保证新鲜度，每日全量修正一致性问题。

* **Q: RAG 的"冷启动"问题怎么解？**
  A: 冷启动指刚上线时没有用户 query 数据难以优化检索效果。解决方案：一是人工标注 50-200 条种子 query。二是 LLM 合成 query——阅读文档 chunk 后为每条生成 3-5 个可能的用户问题。三是日志预分析——从搜索日志或客服记录提取种子 query。冷启动基线：种子 query 检索命中率超 70% 即可上线，运行中收集真实数据迭代优化。

* **Q: RAG 的"重排"什么时候必须做？**
  A: 必须做的场景：一是对回答准确率有严格要求（金融、医疗、法律）。二是海量知识库（百万级），向量检索噪声多需二次过滤。三是用户问题容易歧义需要消歧。四是多路召回后需要统一排序。不需要的场景：知识库小（几千条）或对延迟极度敏感。工程经验：100K+ 文档时重排带来的精度提升远大于增加的延迟成本。



### Function Calling与MCP


* **Q: Function Calling 是什么？背后的机制？**
  A: Function Calling 是 LLM 在生成回复时选择调用预定义函数的能力——不是模型执行代码，而是模型输出"我建议调用函数 X，参数为 Y"。机制：模型在训练时见过大量函数调用的序列数据，学会了理解函数签名、参数结构和使用时机。开发者提供函数定义（名+描述+参数 Schema），模型在常规 token 之外多了一个"调用函数"的选项。

* **Q: Function Calling 一次完整流程？**
  A: 六步流程。第一步——定义工具（名称、用途、参数）。第二步——发送请求（用户消息+工具定义发 LLM）。第三步——模型决策（LLM 决定是否调用工具）。第四步——执行函数（应用层解析调用并执行）。第五步——返回结果（执行结果以 tool_result 角色回传）。第六步——生成回复（LLM 综合问题+结果生成最终回复）。一次请求中可多次调用工具（串行或并行）。

* **Q: 工具描述写得好不好直接决定调用准不准？**
  A: 是的。好描述的规范：名称以动词开头（"searchProducts"）；描述清晰说明使用场景（"当用户需要查找产品信息时使用"）；参数用中文详细描述（"关键词：搜索关键词支持模糊匹配"）；给出使用示例。实践数据：工具描述的好坏可使调用准确率从 60% 变为 95%+。

* **Q: Function Calling 和 JSON Mode 有什么区别？**
  A: 区别在"用途"。Function Calling 设计用于"触发动作"——模型自主决定是否调用，可调用多个，可跳过。JSON Mode 设计用于"格式化输出"——强制模型输出有效 JSON，专注数据提取。选型原则：需要"做某事"（查数据、发邮件）→ Function Calling；需要"输出某格式"（提取信息、生成结构）→ JSON Mode。两者可混合使用。

* **Q: 多个工具同时调用怎么管？**
  A: 策略：一是"自动并行"——不依赖调用结果的可并行执行（查天气和查新闻）。二是"串行依赖"——工具 B 依赖工具 A 输出则串行。三是"结果合并"——并行结果分别返回，模型综合生成回复。限制：建议不超过 5-10 个并行调用，太多会稀释模型注意力。

* **Q: 工具调用失败怎么处理？**
  A: 分三步。第一步——错误分类：瞬时可重试（网络超时）和不可重试（参数错误）。第二步——重试策略：瞬时错误自动重试 1-2 次（指数退避），参数错误返回结构化错误让模型修正。第三步——兜底：重试仍失败时告知用户并提供替代方案。工程实践：工具返回统一 Result 类型——{success, data, error: {code, message, retryable}}。

* **Q: 工具结果太大怎么办？**
  A: 策略：一是截断——只返回前 N 条并注明总数。二是摘要——LLM 对结果做摘要再放回上下文。三是分页——返回结果+分页标记让模型决定是否翻页。四是结构化——只保留 key 信息省略冗余字段。预防：在工具定义中加 limit/offset 参数让模型指定返回数量。

* **Q: 工具调用的"幂等性"为什么重要？**
  A: 幂等性指同一操作执行多次效果相同。工具调用中重试机制天然产生重复执行。如果工具不是幂等的（如"创建订单"、"扣减余额"），重试会导致重复下单或扣款。设计原则：写操作工具要设计为幂等的——带幂等键（idempotency key），服务端检测相同 id 直接返回已有结果。工具描述中注明"此操作是幂等的"。

* **Q: MCP 是什么？为什么需要它？**
  A: MCP（Model Context Protocol）是 Anthropic 推出的 AI 工具标准化协议，解决"每个框架各有各的工具定义方式互不兼容"的问题。MCP 定义了标准三层结构：Server（工具提供方）、Client（工具消费方）、Bridge（连接层）。需要原因：标准化（工具定义发现调用安全统一规范）、解耦（工具定义和模型 API 分离）、生态（同一 Server 被任何 MCP Client 使用）。

* **Q: MCP 的三层核心结构（Server / Client / Bridge）**
  A: MCP Server——实现具体工具的进程/服务，通过暴露"工具列表"和"工具执行"两个端点提供能力。MCP Client——使用工具的 AI 应用（Claude Code、LangChain Agent），向 Server 请求工具列表并选择合适的工具。Bridge——可选中间层，负责协议转换、路由、安全控制。典型部署：Server 作为独立进程运行（stdio 或 HTTP 传输），Client 通过子进程或网络请求连接。

* **Q: MCP 和 Function Calling 是替代关系吗？**
  A: 不是替代关系，是不同层级。Function Calling 是模型 API 层面的能力——模型输出函数调用。MCP 是工具管理和发现层面的协议——把工具定义从模型 API 调用中解耦。关系：MCP Server 的工具经过 MCP 协议暴露，Client 在调用模型 API 时把 MCP 工具转换成当前模型支持的 Function Calling 格式。两者配合使用。

* **Q: Function Calling vs MCP 全维度对比**
  A: 集成方式——FC：工具定义硬编码，改工具改代码。MCP：工具通过 Server 动态注册。跨模型——FC：不同模型格式不同需适配。MCP：协议标准化，Client 负责转换。工具发现——FC：手动注册。MCP：Server 自动暴露。权限控制——FC：自行实现。MCP：协议层统一控制。生态——MCP 仍在早期但被广泛采用。

* **Q: MCP Server 一般怎么实现？**
  A: 用 Python 或 TypeScript，推荐 Python（官方 SDK 完善）。最小实现：用 FastMCP 框架——`from mcp.server.fastmcp import FastMCP; mcp = FastMCP("my-server"); @mcp.tool() def my_tool(param: str) -> str: return result; mcp.run(transport="stdio")`。Server 通过 stdio 或 SSE 传输。每个 Server 应做到一次部署可被多个 Client 重复使用。

* **Q: MCP 三种传输方式（stdio / HTTP / SSE）怎么选？**
  A: stdio——通过标准输入输出流通信（Client 启动 Server 子进程），延迟最低、最安全。适合本地开发工具（Claude Code）。HTTP/SSE——Server 作为 HTTP 服务运行，Client 通过 SSE 连接。支持远程部署、多 Client 共享。选型：本地开发用 stdio，生产部署用 SSE。

* **Q: MCP 和 LangChain Tool 怎么共存？**
  A: 用 LangChain 的 MCP 适配器（langchain-mcp-adapters）把 MCP Server 包装成 LangChain Tool：`from langchain_mcp_adapters import MCPToolkit; tools = MCPToolkit("path/to/server.py").get_tools()`。这样 LangChain Agent 可用任何 MCP Server 的工具。生产实践：核心业务能力封装成 MCP Server，在任何框架中用适配器调用。

* **Q: 工具调用的 token 怎么算？**
  A: 三部分。工具定义——每次请求发送工具描述消耗输入 token（每个工具 50-150 tokens）。工具调用请求——模型输出的函数名和参数。工具结果——执行结果回传。优化：精简描述、动态路由只传相关工具、截断结果。监控：工具调用 token 占总 token 30-50% 是常见，超过 70% 说明冗余。

* **Q: 工具权限 / 越权怎么控制？**
  A: 分三层。传输层——MCP Server 连接鉴权。工具层——每个工具独立的权限声明（只读/读写）。执行层——运行时权限校验。缓解越权：工具执行时做"用户上下文注入"——隐式参数含当前用户身份，Server 端验证权限。不要信任 Agent 传过来的 userId，从请求上下文中提取。

* **Q: 工具集合怎么管理（工具一多模型选错）？**
  A: 策略：一是分组路由——用户意图判断只暴露相关分组。二是命名一致——相关工具用统一前缀（order_create、order_query）。三是禁用不相关——当前场景用不到的工具移除。四是层级工具——先暴露"元工具"再暴露子工具。五是定期审计——检查调用统计移除少用的。

* **Q: Skills 和 Function Calling 是什么关系？**
  A: Skills 是 Anthropic Claude 平台的"预配置能力"——对工具+Prompt 的组合封装。一个 Skill = System Prompt + 工具定义 + Few-shot 示例。Function Calling 是底层 API 能力——模型可以调用函数。Skill 是业务层概念，FC 是技术层概念。一个 Skill 内部可能包含多个 FC 工具的调用编排。

* **Q: 工具调用的"自描述"为什么重要？**
  A: 自描述让工具可被 AI 自动发现和使用。重要性：减少维护成本（新工具只需写 Server 描述）、支持动态环境（根据上下文动态显隐工具）、提升准确率（描述越清晰使用越正确）。四个要素：名称（自解释）、描述（使用时机+示例）、输入（参数含义+取值范围）、输出（返回值格式+错误类型）。

* **Q: 一个常被问的场景：让 Agent 自动写代码并跑测试，应该怎么设计工具集？**
  A: 设计四个核心工具：read_file（读文件）、write_file（写/改文件）、execute_command（沙箱中运行命令）、search_code（搜索代码定义）。原则：操作限制在沙箱目录内、每次修改后自动触发 lint 和测试、删除文件等危险操作需 HIL 确认。

* **Q: 同一个 LLM 既给前端又给 Agent 用，工具怎么设计？**
  A: 核心是"工具分组+角色隔离"。前端工具是 UI 交互操作（展示订单列表），Agent 工具是后端操作（查询数据库）。用两个独立 System Prompt 配置——前端工具返回 UI 组件结构，Agent 工具调用后端服务。底层同一套 FC 机制但工具列表不同。不要混在一起暴露。

* **Q: Anthropic Skills 是什么？和 MCP 什么关系？**
  A: Anthropic Skills 是 Claude 平台的"可复用 AI 功能模块"——封装了特定 System Prompt、工具定义和使用模式。和 MCP 的关系：MCP 是底层协议标准（Server 如何暴露工具），Skills 是上层的"用户界面"（用户如何发现和使用能力）。MCP tools 可被组织成不同的 Skills。Skills 面向终端用户，MCP 面向开发者。

* **Q: MCP 的 Resources、Tools、Prompts 三种能力区别？**
  A: Resources（资源）——对外暴露数据，只读（类似 REST GET）。Tools（工具）——对外暴露可执行动作，可读写（类似 POST/PUT）。Prompts（提示）——预定义的 Prompt 模板和角色设定。工程区别：Resources 是"数据供给"，Tools 是"操作入口"，Prompts 是"行为预设"。三者可组合使用。

* **Q: MCP 有哪些常见的安全风险？**
  A: 五大风险。恶意工具执行——安装恶意 Server 被执行。防御：权限声明+执行确认。数据泄露——Server 读取敏感文件后返回。防御：白名单目录+输出过滤。注入攻击——操控工具调用参数。防御：输入验证+参数白名单。供应链攻击——下载的 Server 含恶意代码。防御：审计源码+使用可信源。最佳实践：最小权限原则，默认拒绝白名单放行。

* **Q: 常用的 MCP Server 有哪些？**
  A: 官方：Filesystem（文件操作）、GitHub（PR/Issue）、Slack（消息）、PostgreSQL（数据库查询）、Puppeteer（浏览器）。社区热门：Playwright（浏览器）、SQLite/Memory（存储）、Exa Search（搜索）、Qdrant（向量检索）、Jira/Linear（项目管理）。推荐：文件操作+搜索+数据库是 Agent 必备三大基础 MCP Server。

* **Q: Computer Use 和 MCP 是什么关系？**
  A: Computer Use 是"视觉模拟操作"（看截图+点鼠标+敲键盘），MCP 是"结构化接口调用"（标准 API）。关系：互补而非替代。Computer Use 适合没有 API 的遗留系统，MCP 适合有标准接口的系统。实践中优先用 MCP（准确可靠），MCP 覆盖不了的再用 Computer Use。

* **Q: 怎么用 Python 写一个 MCP Server？**
  A: 使用 FastMCP 框架：`from mcp.server.fastmcp import FastMCP; mcp = FastMCP("weather"); @mcp.tool() def get_weather(city: str) -> str: return f"{city} 22C sunny"; mcp.run(transport="stdio")`。关键点：函数签名自动生成工具 Schema，transport 参数选 stdio（本地）或 sse（远程）。推荐项目结构：server.py + tools/ + resources/。

* **Q: Function Calling 在 Agent 框架里的位置？**
  A: Function Calling 是 Agent 框架的"执行层"基础设施——Agent 决定要做什么，FC 负责怎么做。分层：决策层（Agent Loop）→ FC 层（转决策为函数调用）→ 执行层（实际执行代码）。Agent 框架（LangGraph、CrewAI、Vercel AI SDK）封装了 FC 的复杂性，开发者只需注册工具框架自动管理。



### Memory与状态管理


* **Q: 大模型本身是无状态的，为什么 ChatGPT 能记住上文？**
  A: ChatGPT 的"记忆"是应用层实现的。每次对话，前端把所有历史消息作为上下文一起发送给模型——包括 System Prompt、历史 user 消息、历史 assistant 回复。模型"看到"了历史所以看起来"记得"。工程实现：前端维护消息列表，每次请求把所有消息按时间序发送。消息太多超窗口时做摘要压缩或裁剪。真正的长期记忆（跨会话）需要向量数据库或 KV 存储。

* **Q: Memory 管理的核心矛盾是什么？**
  A: 核心矛盾是"信息保存完整度"和"Token 预算控制"之间的 trade-off。保留更多历史有助于模型理解上下文（提高质量），但历史消息消耗大量 token（增加成本、稀释注意力）。具体体现：粒度矛盾（越细的粒度噪声越多）、时效性矛盾（旧信息可能不再相关）、选择性矛盾（哪些该保留的判断本身就是 AI 问题）。

* **Q: 短期记忆有哪几种实现？各自适合什么？**
  A: 三种。一是"完整历史"——全部消息传给模型，适合短对话（<10 轮），准确度最高但 token 大。二是"滑动窗口"——只保留最近 N 轮，适合长对话，token 可控但丢早期信息。三是"摘要压缩"——早期历史压缩成摘要，适合需要理解整体脉络的场景。多数产品用滑动窗口+摘要混合方案。

* **Q: 长期记忆怎么做？**
  A: 核心架构是"存储+检索"。存储层——向量数据库持久化记忆，每条含：内容、元数据（时间戳、重要性、有效期）、embedding。检索层——用当前上下文 query 检索相关记忆，Top-K 注入 prompt。写入策略：新信息判断是否值得写入（重要性>阈值）、是否和已有记忆冲突（冲突则更新）。生产实践：每轮对话结束后异步写入，不对实时响应产生影响。

* **Q: 滑动窗口的 N 怎么定？**
  A: N 取决于上下文窗口、对话复杂度、Token 预算。经验公式：N = 窗口 / (用户平均 token + 回复平均 token) * 0.5。简单对话取 10-20 轮（超过 20 轮关联度极低），复杂场景取 30-50 轮。动态窗口：根据复杂度动态调整。关键：窗口内按相关性排序而非时间顺序——最相关的历史放最前面。

* **Q: 摘要压缩什么时机做？**
  A: 三种触发时机。一是"超限触发"——消息总长超窗口 70% 时压缩。二是"间隔触发"——每 N 轮后台做一次背景摘要。三是"T 轮触发"——消息超过 T 轮时最早消息开始压缩。推荐："超限+间隔"组合——每 10 轮做轻量摘要（后台），超 70% 窗口时做深度压缩。保留关键决策和用户偏好，丢掉闲聊。

* **Q: 摘要丢关键信息怎么办？**
  A: 缓解策略：一是"重要信息标记"——System Prompt 要求模型用 `[IMPORTANT]` 标记关键信息，压缩时优先保留。二是"分层摘要"——保留多层摘要（近 30 分→近 2 小时→今天→本周），只压缩最早层。三是"关键事件提取"——专门 LLM 调用提取不可丢失的事实信息。四是"完整性校验"——压缩后用 LLM 检查是否遗漏关键信息。

* **Q: 多用户怎么隔离记忆？**
  A: 原则"用户维度完全隔离"。实现：每条记忆存时关联 userId，检索时强制加 userId 过滤。向量数据库加 filter，关系型数据库用 WHERE。Agent 场景：Agent 的工具使用技巧记忆和用户的个人信息记忆分开存储。生产隔离方案：用户维度完全隔离；会话维度同用户不同会话间记忆共享。用户记忆应可导出和删除。

* **Q: 用户改主意了，记忆怎么处理？**
  A: 核心设计是"版本化+撤回"。方案一"覆盖更新"——直接替换，简单但旧偏好被永久覆盖。方案二"版本化"——每次存带时间戳和有效状态，查询取最新。方案三"声明式标记"——用户明确声明"取代之前说法"时精确替代。生产建议方案二：记忆加 status（active/superseded/deleted）+ superseded_by 形成变更链。

* **Q: Agent 的"工作记忆"（Working Memory）是什么？**
  A: 工作记忆是 Agent 当前任务执行过程中的"临时上下文"，内容包括：当前任务目标、已完成步骤及结果、待完成步骤、关键中间数据。和长期记忆的区别：随任务结束清空。工程实现：LangGraph 的 State 对象就是工作记忆的实现。设计原则：只保留当前任务直接相关的信息，每步结束后做上下文修剪。

* **Q: Memory 系统设计有哪几条铁律？**
  A: 五条。一是记忆不是越多越好——只存对未来决策有复用价值的信息。二是记忆需时效性——设 TTL 过期时间。三是写入成本低于检索收益——每条写入前评估性价比。四是用户永远是主人——用户必须能查看编辑删除自己的记忆。五是隔离是底线——不同用户严格隔离。违反这些铁律的系统在生产必然出问题。

* **Q: 怎么让 Agent 记住"用户偏好"？**
  A: 四步系统。第一步——识别偏好（Detect）：Agent 在对话中识别用户偏好表达。第二步——结构化存储（Store）：以 {key, value, userId, confidence, timestamp} 格式存储。第三步——检索应用（Retrieve）：新对话时检索 Top-5 注入 System Prompt。第四步——更新确认（Update）：用户改变偏好时更新 active 标记。关键：偏好记忆需要显式确认——不要仅凭一次表达就永久记住。

* **Q: 记忆系统的隐私和合规怎么做？**
  A: 四要素。一是数据最小化——只存必要信息，不存敏感 PII。二是存储加密——AES-256（静态）+ TLS（传输）。三是用户控制权——查看、编辑、删除。四是数据生命周期——设自动过期机制。GDPR/个保法要求：数据可移植（用户可导出）、处理记录、影响评估。建议使用差分隐私——不存精确值。

* **Q: Memory 演进路线（从 demo 到生产）？**
  A: 四阶段。阶段一——Context Memory（Demo）：历史消息直接拼接到 Prompt。简单但 token 浪费。阶段二——滑动窗口（MVP）：保留最近 N 轮。Token 可控但丢失早期上下文。阶段三——摘要+Window（生产）：最近 N 轮保留原文，之前的压成摘要。阶段四——分层 Memory（企业级）：短期（窗口）+中期（摘要）+长期（向量检索）+偏好（KV 存储）。

* **Q: Claude Code 的 memory 系统怎么实现的？**
  A: 基于文件存储+规则驱动。核心：CLAUDE.md 文件作为"项目级记忆"——存储技术栈、代码风格约定。Agent 每次启动自动加载。用户通过"记住"指令显式写入偏好。特点：记忆透明可编辑（纯文本文件）、项目级别隔离、无自动隐式记忆（只有用户明确要求才写）。简洁但有效。

* **Q: Episodic Memory vs Semantic Memory 区别？**
  A: Episodic Memory（情景记忆）——存储"事件"（时间+场景+上下文），适合对话追溯。Semantic Memory（语义记忆）——存储"事实"（用户偏好、属性），适合跨会话用户画像。工程区别：情景记忆需时间索引（时序数据库），语义记忆需更新/合并逻辑。两者组合使用——情景记忆提供"证据来源"，语义记忆提供"快速检索"。

* **Q: 多 Agent 共享 memory 怎么设计？**
  A: "三层访问模型"。全局层——所有 Agent 可读（公司政策）。团队层——特定 Agent 组共享（客服组共享投诉历史）。私有层——单 Agent 独有（当前会话上下文）。实现：存储带 visibility 标签（global/team/private）。冲突解决：两个 Agent 写入冲突记忆时"最后写入+置信度加权"决定。每个写入应可追溯（记写入 Agent ID）。

* **Q: Memory 的访问控制（哪些 Agent 能读 / 能写）？**
  A: 读权限——默认只能读自己写入的记忆+全局公开。跨 Agent 读需授权。写权限——Agent 只能写自己的记忆空间。特殊场景：用户授权多 Agent 共享时创建共享空间。工程实现：每条记忆带 owner_id + permissions（读列表+写列表）。除非必要不要让 Agent 读写其他 Agent 的记忆。

* **Q: 用户偏好 Memory 怎么实战？**
  A: 三步。第一步——定义 Schema：{userId, key, value, confidence, source（对话/显式/推断）, ttl}。区分"显式偏好"和"推断偏好"。第二步——写入策略：显式高置信直接写，推断需 >0.7 且出现 2 次以上才写。第三步——应用：对话开始时检索 Top-5 偏好注入 System Prompt，Agent 回复中自然融入偏好。不要把用户偏好当对话主题。

* **Q: 怎么判断一段记忆该不该写？**
  A: 核心原则是"这条记忆对未来 Agent 决策是否有可复用的价值"。写之前做三个判断：一是这条信息是否跨越当前会话仍然有用；二是是否存在明确的触发场景；三是是否足够稳定（用户一时兴起不必写）。采用"三筛法"——语义重要性打分+频率检测（同一信息出现 2 次以上才写）+用户显式确认。生产级做法用独立 LLM call 做记忆裁决。


### LangChain与框架

* **Q: LangChain 是什么？它真正帮你做了什么？**
  A: LangChain 是一个围绕 LLM 构建应用的编排框架，解决的核心痛点是"把多个 LLM 调用、工具、数据源串成一条可维护的流水线"。它真正帮到的是：标准化了 Prompt 模板管理、输出解析、链式调用、工具集成等常见模式；提供了 LCEL（声明式语法）让复杂 pipeline 写得像管道操作；内置了多种 Memory 实现、Agent 循环、RAG 组件。但它的抽象层较厚，调试时堆栈深，且版本迭代快（0.x 到 0.3 API 变化大）。适合快速原型和标准场景，复杂业务逻辑建议用 LangGraph 替代 Chain。生产环境建议配合 LangSmith 做 trace 观察，否则黑盒问题难排查。
* **Q: LCEL（LangChain Expression Language）是什么？**
  A: LCEL 是 LangChain 的声明式组合语法，用 `|` 管道操作符把 Runnable 组件串起来。核心设计：每个组件都实现了 Runnable 接口（有 invoke/stream/batch 等方法），管道自动处理输入输出类型的转换和流的传播。例如 `prompt | model | outputParser` 就是一个 LCEL chain。优势在于：自动支持 streaming、异步、批量调用、并行执行；和 LangSmith 深度集成，trace 自动生成；代码可读性高。但调试起来堆栈信息比较深，且 LCEL 的隐式类型推导在复杂场景里会出意外。适用场景是"标准链"，非标控制流（分支、循环、human-in-the-loop）需要用 `RunnableLambda` 自定义或直接用 LangGraph。
* **Q: LangGraph 是什么？为什么有了 LangChain 还要它？**
  A: LangGraph 是 LangChain 团队推出的有状态图框架，解决 LangChain Chain（DAG）无法处理循环、条件分支和状态持久化的痛点。Agent 本身是一个 while 循环（Observe-Think-Act），用 Chain 表达需要 hack（用 RunnableLambda 模拟跳转），而 LangGraph 原生支持 Node + Edge 的图结构，节点之间可以形成环，还内置了 State 管理和 Checkpoint 机制。选型建议：标准 RAG 或简单链用 LangChain LCEL 就够了；需要 Agent 循环、多步推理、Human-in-the-loop、多 Agent 协作时上 LangGraph。LangGraph 的学习曲线比 LCEL 陡，但表达能力更强。
* **Q: 用 LangGraph 写一个最小图怎么写？**
  A: 核心三步：定义 State、添加 Node、连接 Edge。示例：`from langgraph.graph import StateGraph; graph = StateGraph(AgentState); graph.add_node("agent", call_model); graph.add_node("tools", call_tool); graph.add_edge("agent", "tools"); graph.add_conditional_edges("tools", should_continue, {"end": END, "continue": "agent"}); graph.set_entry_point("agent"); app = graph.compile(checkpointer=MemorySaver())`。关键点是 State 定义了图全局共享的数据结构；Node 是执行单元（接收 state 返回更新）；Edge 决定流转方向；compile 时传入 Checkpointer 开启状态持久化。最小图至少需要一个 agent node 和一个 decision edge。LangGraph 的图编译后返回一个 Runnable，可以 invoke/stream，和 LCEL 组件无缝互操作。
* **Q: Runnable 是什么？为什么所有组件都是 Runnable？**
  A: Runnable 是 LangChain 的通用执行接口，定义了 `invoke`、`stream`、`batch`、`astream` 等标准方法。任何组件（PromptTemplate、LLM、OutputParser、Retriever、Tool）都继承自 Runnable，意味着它们可以统一地被组合、调用和流式传输。这种统一接口带来的关键好处：LCEL 管道操作符 `|` 能串联任意 Runnable、自动路由输入输出类型、统一的流式处理、和 LangSmith 自动 trace。你可以把 Runnable 理解为"可执行的函数签名"——给一个输入，返回一个输出，支持多种调用模式。自定义 Runnable 只需继承 `RunnableLambda` 或 `RunnableGenerator`。
* **Q: Output Parser 和 Tool Calling 怎么选？**
  A: Output Parser 是把模型生成的文本字符串解析成结构化数据（如 JSON、Pydantic 对象），适合"模型直接生成输出"的场景，比如总结、翻译、分类。Tool Calling 是让模型选择调用预定义的函数并返回结构化参数，适合"需要执行动作或访问外部数据"的场景。选型原则：如果输出只是"数据转换"（从文本到结构体），用 Output Parser + JSON Mode 更轻量；如果需要"触发副作用"（查数据库、发邮件、执行代码），必须用 Tool Calling。工具调用还解决了输出 parser 一个关键问题——模型可以选"不做"（不调用工具），而 parser 强制模型总是输出结构。生产环境中两种经常配合：先通过 Tool Calling 获取数据，再通过 Output Parser 格式化最终回复。
* **Q: Prompt Template 和写字符串拼接的区别？**
  A: Prompt Template 提供了变量注入、模板继承、部分格式化、类型校验和输出端适配。核心区别在于：一是内置的输入变量校验（缺字段或多余字段报错）；二是支持从 Runnable chain 中自动提取变量，不需要手动拼接字符串；三是和 LangSmith 集成时变量值自动 trace，调试时能清晰看到每次渲染结果；四是支持部分格式化（先预填一部分变量，运行时再填剩余）。但简单的场景（一两句话的 prompt）用 f-string 确实够用。推荐边界：变量超过 2 个或模板行数超过 5 行时用 PromptTemplate，否则字符串拼接更轻量。LangChain 还支持 ChatPromptTemplate（多消息模板）和 FewShotPromptTemplate，这些手写拼接非常痛苦。
* **Q: LangChain 全部 Splitter，挑哪个用？**
  A: LangChain 提供 RecursiveCharacterTextSplitter、TokenTextSplitter、MarkdownHeaderTextSplitter、SemanticChunker 等。选型建议：通用场景用 RecursiveCharacterTextSplitter（按 `["\n\n", "\n", " ", ""]` 层级切分，兼顾语义和 chunk 大小控制）；代码场景用 Language（Recursive 的语言变体，按语法节点切分）；Markdown 文档用 MarkdownHeaderTextSplitter（按标题层级保留文档结构）；需要语义边界时用 SemanticChunker（通过 embedding 余弦相似度检测断点，质量最高但速度慢）。生产标准做法是 Recursive + overlap（10-20% chunk size）作为 baseline，然后用 Chunk 的检索效果评估来调参数。关键参数：chunk_size（500-1000 tokens 是常见起点）、overlap（100-200 tokens）。
* **Q: 怎么把 LangChain 的链接到 Nest / Next API？**
  A: LangChain 的 Python 链路不适合直接在 Node 后端运行。推荐架构：Python 侧起 FastAPI 服务封装 LangChain chain 或 LangGraph agent，暴露 REST/gRPC 端点；Nest/Next 通过 HTTP 或 SSE 调用。Python 服务层可以用 `astream_events` 或 `astream_log` 实现流式响应。如果团队全栈 Node，Vercel AI SDK 是更好的选择。关键实践：在 FastAPI 端实现 streaming 响应（`StreamingResponse` + `EventSource`），Nest 用 `@Sse()` 或 fetch + ReadableStream 消费。需要处理超时和重试时，在 Python 侧设置 chain 的 timeout，Nest 侧用 AbortController 控制前端取消。
* **Q: LangSmith 是什么？为什么所有 LangChain 项目都建议接？**
  A: LangSmith 是 LangChain 的 LLM 可观测性平台，提供 trace、评估、数据集管理、Prompt 调优等功能。建议接的原因：LangChain 的抽象层厚，不接 LangSmith 就是黑盒——看不到每个组件的输入输出、延迟和 token 消耗。LangSmith 可以做到：单次 trace 展示完整的 chain/agent 执行路径（每个 LLM 调用、工具调用、检索的耗时和 token）；离线评估（用数据集批量测试 chain 效果）；在线监控（生产环境异常检测和回放）。替代方案有 Langfuse、Helicone、Arize Phoenix，但 LangSmith 和 LangChain 的集成最深（自动 trace 无需配置）。缺点是 SaaS 收费高，数据送到 LangChain 服务器有合规风险。
* **Q: LangGraph 的 Checkpoint 怎么用？**
  A: Checkpoint 是 LangGraph 实现状态持久化和断点恢复的核心机制。在 `graph.compile(checkpointer=MemorySaver())` 时传入 Checkpointer，图每执行一个节点就自动保存一次 state snapshot。用法：通过 thread_id 恢复指定会话状态——`app.invoke(inputs, config={"configurable": {"thread_id": "user-123"}})`。Checkpoint 支持 MemorySaver（内存）、SqliteSaver（持久化）、PostgresSaver（生产级）。关键场景：Human-in-the-loop（打断后恢复）、错误恢复（节点失败后从上一个 checkpoint 重试）、多轮对话（在同一个 thread_id 上持续 invoke）。检查点保存的内容由 State 定义决定，设计 State 时只放"需要持久化"的数据可以减少存储开销。
* **Q: LangChain vs LlamaIndex 怎么选？**
  A: LangChain 和 LlamaIndex 的重叠区域在 RAG，但设计哲学不同。LangChain 是通用 LLM 编排框架，擅长 Agent、工具链、复杂流程；LlamaIndex 专注数据索引和检索，对文档解析、索引策略、检索策略（如 RouterQueryEngine、SubQuestionQueryEngine）的支持更深。选型建议：核心场景是 RAG/数据管道时选 LlamaIndex（数据连接器丰富、检索策略多）；需要 Agent、工具调用、多步骤推理时选 LangChain；也可以混用——LlamaIndex 做索引和检索，LangChain 做 Agent 编排。LlamaIndex 也有自己的 Agent 框架（如 ReActAgent），但生态和灵活性不如 LangChain。企业级 RAG 常用组合：LlamaIndex 处理文档 -> 向量数据库（pgvector/Qdrant）-> LangChain Agent 做查询路由和工具编排。
* **Q: LangChain 内置的 Agent 类型有哪些？怎么选？**
  A: LangChain 内置的 Agent 类型包括：OpenAI Tools Agent（推荐，用 tool calling 能力最强）、ReAct Agent（传统 text-completion 模式）、Structured Chat Agent（函数调用支持）、XML Agent（适合 Claude，用 XML 格式描述工具）、SQL Agent（数据库查询专用）、JSON Agent（操作 JSON）。选型建议：优先用 OpenAI Tools Agent（模型原生支持 tool calling，稳定性最好）；如果使用 Claude，用 XML Agent 效果好（Anthropic 的训练数据包含大量 XML）；自定义需求强烈时用 LangGraph 完全自己控制。2025 年的趋势是弃用 text-completion agent（ReAct），全面转向 tool-calling-based agent。
* **Q: LangGraph 怎么做 Human-in-the-loop？**
  A: LangGraph 通过 Checkpoint + interrupt 实现 HIL。在 `graph.compile()` 时传入 `interrupt_before=["node_name"]`，图在执行到该节点前暂停，等待人工输入。同时设置 `checkpointer` 保存状态，用户查看后可以继续或修改。关键是 `Command(resume=value)` - 用户提供输入后调用 `app.invoke(None, config)` 恢复执行。HIL 适用于：高风险操作确认（大额支付、删除数据）、工具调用前审批、生成内容审核。实践建议：尽量只在"审批节点"中断，不要让每一步都中断，否则用户体验差。还可以用 `interrupt_after` 在节点执行后中断，适合"先看看结果再决定"的场景。
* **Q: LangGraph 的多 Agent 模式有哪些？**
  A: LangGraph 支持三种多 Agent 模式。Supervisor 模式：一个 supervisor agent 协调多个 worker agent，supervisor 决定任务分配和结果汇总，适合"一个 PM 带多个工程师"的场景。Hierarchical 模式：多层级 Agent，每层有不同粒度，适合复杂企业流程。Network 模式：Agent 之间直接通信，没有中心协调者，适合需要自由讨论的场景。实现方式：每个 Agent 是一个 Node，加上路由 Edge 决定消息传递方向。State 是全局共享的，每个 Agent 可以读写。生产推荐 Supervisor 模式——可控性好、调试方便。多 Agent 的关键设计问题是通信协议（消息格式）、冲突解决（两个 Agent 给出矛盾结论时谁说了算）和 termination condition（什么情况下多 Agent 讨论结束）。
* **Q: LangChain 的 Memory 类型对比？**
  A: ConversationBufferMemory（保存全部消息，适合短对话，token 消耗大）、ConversationSummaryMemory（用 LLM 生成摘要压缩历史，适合长对话但可能丢细节）、ConversationBufferWindowMemory（只保留最近 K 轮，token 可控但丢失早期信息）、VectorStoreRetrieverMemory（用 embedding 检索相关历史，适合长期记忆，需向量数据库）、ConversationSummaryBufferMemory（摘要 + 缓冲窗口混合，摘要历史+保留最近窗口，综合较优）。选型建议：短对话用 BufferWindow（K=10-20）；长对话用 SummaryBuffer（buffer 窗口 10 轮 + 实时摘要）；需要跨会话记忆用 VectorStoreRetriever。注意 LangChain Memory 类在新版中逐步弃用，LangGraph 推荐直接在 State 里管理消息列表。
* **Q: Vercel AI SDK 和 LangChain 是什么关系？**
  A: Vercel AI SDK 和 LangChain 在功能上有重叠但定位不同。Vercel AI SDK 专注前端和后端（Edge/Node）的 AI 集成，核心是 `useChat`、`useCompletion`、`StreamData` 等 React/Vue/Svelte hooks 和 Edge Runtime 流式传输。LangChain 是 Python 为主的全栈编排框架。关系上：Vercel AI SDK 可以单独使用（直接调模型 API），也可以通过 `LangChainAdapter` 把 LangChain 的 chain/agent 暴露给 Vercel AI SDK 的前端。实践中，全栈 Node/TypeScript 团队常选 Vercel AI SDK（更轻量、Edge 友好、前端集成深度好）；Python 后端团队选 LangChain。Vercel AI SDK 的 RAG 和 Agent 能力不如 LangChain 完备，但 2025 年起正在快速补齐（如 `ai.tool`、`ai.generateText`）。
* **Q: LCEL Streaming 怎么实现？**
  A: LCEL 默认支持 streaming，只要所有组件都实现了 `stream` 方法。`model.stream()` 本身就是 streaming；`prompt | model | outputParser` 会自动传播 stream。关键机制是 `astream_events`（LangChain 0.1+），它能 stream 中间步骤的 token 和 events。实现方式：`chain.astream_events(input, version="v1")` 返回一个 AsyncGenerator，yield 不同类型的事件（`on_chat_model_stream`、`on_retriever_end` 等）。如果你需要自定义 stream 行为，实现 `RunnableGenerator` 或 `RunnableLambda(stream_output=True)`。流式输出是"chain + Agent"场景的刚需——用户可以边看推理过程边决定是否继续等待。生产环境建议用 `astream_events` 的 `v2` API（更稳定）配合 LangSmith 监控流式延迟。
* **Q: LangChain 怎么写一个完整 RAG chain？**
  A: 标准 RAG chain 代码骨架：`from langchain.chains import create_retrieval_chain` `from langchain.chains.combine_documents import create_stuff_documents_chain`。先用 `create_stuff_documents_chain(llm, prompt)` 创建文档组合链（把检索到的文档塞进 prompt context），再用 `create_retrieval_chain(retriever, combine_docs_chain)` 组合。完整实现：`retriever = vectorstore.as_retriever(search_kwargs={"k": 4}); combine_chain = create_stuff_documents_chain(llm, prompt); rag_chain = create_retrieval_chain(retriever, combine_chain); rag_chain.invoke({"input": "user question"})`。进阶：加 HistoryAwareRetriever 处理多轮对话；加 Re-rank 步骤过滤低相关文档；加 query transformation（LLM 重写问题再检索）；用 `create_history_aware_retriever` 把聊天历史转成独立查询。生产级 RAG chain 还要加 guardrails（输入输出检测）、fallback（检索为空时模型直接回答）、和 trace 集成。
### 工程化与部署

* **Q: 大模型在 ToB 业务里落地有哪些核心难点？**
  A: 核心难点有五。一是幻觉不可消除，金融/医疗等严肃场景需要严格的 Human-in-the-loop 和事实核查层。二是成本不可控——API 调用按 token 计费，ToB 高频调用下成本线性增长，需要缓存、Prompt 压缩、模型蒸馏等降本策略。三是数据安全与合规——客户数据不能出 VPC，要私有化部署或至少做到数据脱敏和审计日志。四是个性化与垂直领域适配——通用模型对行业术语理解差，需要 RAG 注入企业知识库或微调。五是评估困难——ToB 场景的"回答质量"是主观的，需要建立 LLM-as-Judge + 人工抽检的双层评估体系。成功案例的共同点是：限定域（Restricted Domain）+ Human-in-the-loop + 渐进式替换（先辅助后自动化）。
* **Q: 模型幻觉的深层原因（再追问版）？**
  A: 从根源上说，LLM 是一个"在 token 空间中做条件概率预测"的系统，不是"从事实数据库中查询"的系统。幻觉的深层原因包括：一是训练数据本身包含错误/矛盾信息，模型学到的是"统计规律"而非"事实正确"。二是 Decoder-only 架构的生成特性——它别无选择必须输出 token，不知道答案时也会"编造"。三是 Softmax 归一化导致概率分布被迫分配给所有 token（包括错误答案）。四是 RLHF 偏好"讨好用户"的回复——模型学会语气自信地给出看似合理但错误的信息。五是指令跟随的副作用——用户问题本身隐含了错误假设时，模型倾向于配合而非纠正。缓解方向：推理时通过搜索（如 Self-RAG、Verify-and-Edit）引入事实校验层，训练时用对抗数据、DPO 优化事实性偏好。
* **Q: 微调（Fine-tuning）核心是什么？什么时候才该用？**
  A: 微调的核心是让预训练模型在特定领域/任务上的表现更优，通过小规模高质量数据调整模型权重。本质是"教模型新的行为模式"而非"灌新知识"。该用微调的时机：模型需要学会特定的输出格式或风格（如客服语气、法律文书结构）；Prompt 工程 和 RAG 无法满足要求（模型始终在关键模式上出错）；你需要持续降低特定场景的推理成本（微调后的模型可以用更小的模型或更短的 prompt 达到同样效果）。不该用微调的时机：只是想给模型加新知识（RAG 更合适、成本更低）；只是偶尔出错（调 Prompt 或 Few-shot 即可）；没有足够的高质量数据（少于 500 条通常不值得）。核心原则：RAG 优先，微调最后。
* **Q: 全参微调 vs PEFT（LoRA / QLoRA）区别？**
  A: 全参微调（Full Fine-tuning）更新模型所有权重，效果好但显存需求极高（7B 模型约需 4x A100 80G），训练慢，存储成本高（每个微调版本存完整权重）。PEFT（LoRA/QLoRA）冻结原始权重，插入低秩适配矩阵训练。LoRA 只训练原权重 0.1%-1% 的参数，显存降低 3-4 倍；QLoRA 进一步把原始权重量化到 4-bit 再加 LoRA，7B 模型可以在单张 RTX 4090(24G) 上微调。效果上：LoRA 在有足够数据时能达到全参微调的 90-95% 效果，但极端复杂任务差距明显。生产建议：先用 LoRA 快速验证可行性，效果不够再上全参微调。全参微调更易过拟合，需要更多数据和正则化。
* **Q: LoRA 为什么能省显存？**
  A: LoRA 的核心思想：预训练权重所在的矩阵往往是"低秩"的，即在任务适配时只需要在原始矩阵旁加一个低秩分解矩阵。具体来说，对权重矩阵 W（d x k），插入 A（d x r）和 B（r x k），其中 r << min(d,k)，训练时只更新 A 和 B。这样需要梯度和优化器状态的参数从 d*k 减少到 r*(d+k)，通常 r=8-64，参数量减少 1000-10000 倍。显存节省来自三方面：参数量少（反向传播的梯度更小）、不需要存全量优化器状态（Adam 的 momentum 和 variance 小得多）、原始权重被冻结不需要梯度。QLoRA 进一步用 4-bit NormalFloat 量化原始权重，把权重存储从 16GB 降到 2GB（7B 模型），加上 LoRA 的适配器后可以在消费级显卡上训练。
* **Q: 微调要准备什么数据？格式怎么定？**
  A: 数据是微调效果的瓶颈。格式一般用对话模板：ChatML 格式（`<|im_start|>system\n...<|im_end|>\n<|im_start|>user\n...<|im_end|>\n<|im_start|>assistant\n...<|im_end|>`）或 ShareGPT 格式（json 数组，每条包含 conversations 列表）。质量要求：每条数据代表"一个理想的模型行为示例"；覆盖边缘情况（如拒答、承认不知道、多轮依赖）；至少 500-1000 条高质量数据，不是越多越好而是越精越好。数据来源：生产日志采样+人工修正、人工编写、用更强模型（GPT-4/Claude）生成后人工审核。关键步骤：去重、去噪声（低质量回答）、平衡分布（不要全是某一类请求）。工具：用 LLaMA-Factory 或 Axolotl 做数据格式转换和训练。
* **Q: 私有化部署有哪些选项？**
  A: 分三层选型。硬件层：显存决定模型上限——7B 模型需要 16-24G（RTX 4090），13B 需要 48G（A6000），70B 需要 4x A100 80G 或 Mac Studio 统一内存。也可租用 GPU（Lambda Labs、Vast.ai、AutoDL）。推理框架层：vLLM（吞吐最高，支持 PagedAttention、Continuous Batching）、Ollama（本地开发最方便）、llama.cpp（CPU/边缘部署）、TGI（HuggingFace 官方，生态好）、TensorRT-LLM（NVIDIA 优化，延迟最低）。部署架构层：单机单卡（开发/小规模）、单机多卡（中等规模）、多机多卡（生产/高并发）。生产推荐：vLLM + Docker + Kubernetes 部署，Kuberay 做 GPU 调度，配合 Prometheus 监控吞吐和延迟。
* **Q: Dify / Coze / FastGPT 这类平台怎么选？**
  A: Dify、Coze、FastGPT 都是 LLM 应用开发平台，选型看场景。Dify（开源）：适合 ToB 私有化部署，支持自定义 Agent、RAG、工作流、API 集成，开发者友好（GitHub 39k+ stars），可以本地部署完全控制数据和逻辑。Coze（字节跳动）：功能最全，插件生态丰富（飞书、抖音等），Bot 商店，适合快速搭建 C 端对话机器人，但私有化版本有限。FastGPT（开源）：专注知识库 RAG，文档解析和检索效果好，适合做内部知识库问答。选型建议：ToB/私有化用 Dify；快速 C 端验证用 Coze；纯知识库问答用 FastGPT。国内选型还需注意数据合规——Dify 和 FastGPT 可本地部署，Coze 的数据经过字节服务器。
* **Q: 自己搭 LLM 应用平台 vs 用 Dify？**
  A: 选择取决于团队能力和项目复杂度。用 Dify 的优势：快速搭建（几天出原型）、内置 RAG/Agent/工作流引擎和可观测性、社区插件多、团队不需要重复造轮子。自建的优势：完全控制技术栈（想用什么模型/数据库/框架都行）、深度定制（Dify 的工作流编辑器难以应对极端复杂逻辑）、性能优化空间大（Dify 的 chain 执行有额外开销）、数据完全不出 VPC。推荐策略：原型验证期用 Dify 快速试错；产品需求明确后评估是否需要自建。如果核心逻辑是"标准 RAG + 简单 Agent"，Dify 够用；如果涉及多步骤复杂业务流、特殊性能要求、深度模型定制，考虑自建。很多团队的做法是 Dify + 自定义 API 插件结合。
* **Q: Function Calling 的优缺点？为什么很多团队转 MCP？**
  A: Function Calling 的优势是模型原生支持、延迟低、实现简单。但缺点是：工具定义耦合在 Model API 调用中，不同模型的工具格式不兼容（OpenAI 的 JSON schema vs Anthropic 的 XML tools）；没有标准的工具注册、发现和调用协议；权限控制需要自己实现；工具描述一多质量下降，模型选错工具概率上升。MCP 解决了这些问题：标准化了工具发现（Server 自描述）、调用方式和传输协议；工具可以动态增删而不改 API 调用代码；权限在 MCP 层统一控制；Tool 和 Resource 的区分解耦了"数据提供"和"动作执行"。大厂转为 MCP 的核心驱动是"标准化"——不用再为每个模型适配不同的工具调用实现。MCP 当前还在早期（2024 年底发布，2025 快速迭代），但已被 Anthropic、LangChain 等广泛采用。
* **Q: Agent Loop 在工程里有哪些坑？**
  A: Agent Loop 的最大五个坑。一是无限循环——Agent 在"调用工具->返回结果->再调用"中停不下来，必须设最大迭代次数（通常 10-25）和 timeout。二是 Token 爆炸——每轮循环把完整工具结果塞回上下文，几轮后上下文就满了，需要用滑动窗口或摘要压缩。三是工具选择错误——工具超过 10 个时模型选错概率上升，需要优化工具描述（动词开头、明确输入输出）或动态工具路由。四是错误恢复——工具调用失败默认行为是"重试或不报错"，应该用结构化错误（fast/fatal 区分）让 agent 知道该重试还是放弃。五是状态管理——Agent 多轮交互的状态（已完成步骤、已获取的数据）需要持久化，否则崩溃后无法恢复。生产级方案：LangGraph 的 State 管理 + Checkpoint + 迭代上限 + token 预算控制。

* **Q: ElasticSearch / 倒排索引在 AI 场景的作用？**
  A: ES 在 AI 场景的核心价值是 Hybrid Search——向量检索不能完全取代关键词检索。ES 的 BM25 算法在术语匹配（产品名、编号、代码片段）上远优于 embedding 检索，且可以结合向量检索（kNN）做加权融合。典型用法：ES 做一级检索（同时跑 BM25 和向量检索），再用 RRF（Reciprocal Rank Fusion）合并结果。ES 也适合做 RAG 的 Filter——先通过结构化字段（时间、类别、权限）过滤再检索。此外，ES 的倒排索引天然适合做 Prompt 缓存检索（命中已缓存的相似问题直接返回），以及日志分析（LLM 调用日志的搜索和聚合）。选型建议：小团队用 ES 自带的稀疏检索（无需额外部署向量数据库）；大规模场景用 ES + 独立向量数据库（Qdrant/Milvus）的方案。
* **Q: Neo4j / 知识图谱在 AI 场景的作用？**
  A: 知识图谱和 Neo4j 在 AI 场景提供的是结构化关系的检索能力。向量检索适合"similar to X"，图谱检索适合"related to X"——实体之间的多跳关系（公司的 CEO 投资的创业公司 的 产品）是向量检索无法直接表达的。典型场景：企业知识库中实体关系的 QA（"A 产品依赖哪个团队维护的中间件？"）；GraphRAG（微软方案）——先用 LLM 从文档中提取实体关系构建图谱，再基于子图检索增强生成，对跨文档推理效果远优于平面 RAG。Neo4j 提供 Cypher 查询语言，可以通过 NL2Cypher（LLM 将自然语言转 Cypher）实现自然语言图谱查询。不足：构建图谱成本高（LLM 抽取实体关系有额外 token 开销和延迟），维护复杂。
* **Q: Docker Compose 在 AI 开发提效里能做什么？**
  A: Docker Compose 在 AI 开发中最实用的场景是一次启动完整的本地依赖环境。一个典型 AI 项目的 compose.yml 包含：Postgres（pgvector）、Redis（缓存/队列）、Qdrant/Weaviate（向量数据库）、MinIO（对象存储）、Ollama（本地模型推理）、Jupyter（开发环境）。好处是：新人加入 5 分钟就能跑通全栈 AI 环境（不用手动装 pgvector 插件/配向量数据库）；每次依赖升级通过 docker-compose pull 完成；CI 里用同样的 compose 配置跑集成测试。进阶用法：用 Docker Compose Profile 区分不同场景（dev/test/ollama-cpu/ollama-gpu），用 healthcheck 确保服务就绪顺序。缺点是 GPU 透传在某些环境（Windows/macOS）受限，生产部署还是用 Kubernetes。
* **Q: LangSmith / Helicone / Langfuse 选哪个？**
  A: 三者都是 LLM 可观测性平台。LangSmith（LangChain 官方）：和 LangChain/LangGraph 集成最紧密（自动 trace 无需手动插桩），提供数据集管理和在线评估，收费 SaaS，数据在 LangChain 侧。Langfuse（开源）：功能对标 LangSmith，可自托管（数据不出 VPC），有 Python/JS SDK，支持 trace/评估/提示管理，社区活跃。Helicone（开源）：轻量级，核心是代理层（OpenAI 兼容 API 代理），适合"只想监控 API 调用日志和成本"的场景，不支持 RAG/Agent 深度 trace。选型建议：用 LangChain 生态选 LangSmith（体验最好，但合规需确认）；需要自托管控制数据选 Langfuse（功能最全的开源选择）；只需 API 监控选 Helicone（最轻量）。
* **Q: vLLM 为什么吞吐高？**
  A: vLLM 的吞吐优势来自 PagedAttention 和 Continuous Batching 两大技术创新。PagedAttention 解决了 KV Cache 的内存碎片问题——传统推理中 KV Cache 是连续内存分配，每次请求预留最大长度，浪费严重。PagedAttention 把 KV Cache 分页管理（类似操作系统的虚拟内存），按需分配物理块，消除碎片，显存利用率从 20-40% 提升到 95%+，从而支持更大的 batch size。Continuous Batching（持续批处理）——传统批处理等整个 batch 完成才释放资源，vLLM 在每个 attention 步骤后动态调整 batch（完成请求立即退出，新请求随时加入）。这意味着即使是流式输出场景，vLLM 的 batch 也始终是满的。此外，vLLM 还支持多种量化（AWQ/GPTQ）、prefix caching（相同前缀复用 KV Cache）、和 tensor parallelism。
* **Q: 模型量化（INT8 / INT4 / AWQ / GPTQ）是什么？**
  A: 量化是把模型权重从 FP16（16-bit 浮点）压缩到更低精度，降低显存和加速推理的技术。INT8：权重用 8-bit 整数，显存减半、速度提升 1.5-2 倍，精度损失极小（<1%）。INT4：进一步减半显存，精度下降 1-3%，对小模型影响明显。GPTQ：后训练量化（PTQ）方法，基于 Hessian 矩阵做权重优化，一次性量化，适合 GPU 推理，支持 vLLM/TGI。AWQ：比 GPTQ 更先进的量化方法，通过观察"激活值"分布来保护重要权重通道，INT4 下的精度通常优于 GPTQ。量化选型建议：追求吞吐用 INT8（vLLM 原生支持）；追求极致显存压缩用 AWQ INT4（精度损失最小的高压缩方案）；边缘设备用 GGUF（llama.cpp 社区的标准量化格式，支持多种 bit）。
* **Q: 模型蒸馏（Distillation）是什么？**
  A: 模型蒸馏是用高能力大模型（Teacher）的输出训练小模型（Student），让小模型模仿大模型的行为。核心训练数据不是原始标注，而是 Teacher 对大量 prompt 的生成结果（logits 或 soft labels 或 text outputs）。蒸馏的核心价值：小模型在特定任务上可以达到大模型 80-95% 的效果，但推理成本降低 10-100 倍，延迟降至毫秒级。蒸馏的三种方式：黑盒蒸馏（用 Teacher 的生成文本做训练数据，最简单）、白盒蒸馏（用 Teacher 的输出 logits 分布，需要访问模型内部）、在线蒸馏（Student 和 Teacher 同时训练）。生产实践：先用 GPT-4/Claude 生成大规模高质量数据集，再用这些数据微调 LLaMA-7B，在特定领域（分类、摘要、客服）达到接近 GPT-4 的效果。
* **Q: 私有化部署 GPU 选什么？**
  A: 选型取决于模型规模和并发需求。推理场景：7-8B 模型（如 Qwen2.5-7B、DeepSeek-V2-Lite）推荐 1x RTX 4090 24G（显存够，性价比最高）或 L40S（企业级，48G 显存）。13-14B 模型需 1x A100-40G 或 1x A6000 48G。70B 模型需 4x A100-80G 或 2x H100（支持 TP/PP 流水线并行）。训练/微调场景：单卡 24G 可以做 QLoRA（7B）；4x A100 80G 可以做全参微调（7-13B）或 LoRA（70B）。预算排序：RTX 4090（性价比王，约 1.3 万）> A6000（48G 显存，约 3 万）> A100 80G（约 6-8 万）> H100（约 20 万+）。国内可选华为昇腾 910B（生态还在完善，适配 PyTorch 需要额外工作）。云端租赁更灵活：AutoDL/Vast.ai 按时租用 GPU，不需要一次性投入。
* **Q: 模型评测常见 benchmark？**
  A: 通用评测：MMLU（多领域知识）、HellaSwag（常识推理）、GSM8K（数学）、HumanEval（代码）、BBH（推理）。中文评测：C-Eval（多学科）、CMMLU、CLUE。AI Agent 评测：SWE-bench（真实 GitHub issue 修复）、GAIA（通用助手）、AgentBench（多任务环境）、WebArena（网页操作）。RAG 评测：RGB（RAG Benchmark）、RECALL（检索+RAG 质量）。选型建议：不要只看单一 benchmark 排名。重点关注你的业务场景对应的 benchmark——做代码助手看 HumanEval/SWE-bench，做客服看 MT-Bench/Chatbot Arena。Open LLM Leaderboard（HuggingFace）聚合了主流评测，方便横向对比。最重要的是建自己的业务评测集——从生产环境中采样 200-500 条数据做人工标注，定期跑分，比任何公开 benchmark 都更有价值。
* **Q: 私有化模型怎么更新？**
  A: 更新策略取决于部署场景。API 分发场景（调云端 API）：用模型版本号做 routing，发布新版本后逐步切流（5%->20%->50%->100%），每个阶段评估效果。私有化部署场景（本地推理）：需要蓝绿部署或滚动更新。蓝绿部署——保持旧模型运行，加载新模型到另一组 GPU，验证通过后切 DNS 或负载均衡器，失败立即回切。滚动更新——逐台 GPU 替换，适合多副本场景。关键实践：每个模型版本保留 2-3 天推理日志用于问题复盘；用 A/B 测试框架做效果对比（LLM-as-Judge + 人工抽样）；模型更新必须同步更新 System Prompt 和 Few-shot 模板（它们共同决定效果）；存储模型版本号和 prompt 版本的关联关系方便排查。
* **Q: ToB 项目灰度发布有什么特殊？**
  A: ToB 项目的灰度发布比 C 端更谨慎。核心特殊点：一是客户等级金丝雀——先灰度给"愿意尝鲜"的中小客户，稳定后才推给大客户。二是替换成本高——客户已经在用旧版本做业务流程，回滚需要客户配合，必须做向前兼容（旧格式输入输出不影响）。三是灰度策略——按客户维度（不是按流量），每个客户完整切换。常见模式：先对 Dev/Staging 环境客户开放，验证通过后推 Production 环境的新建客户（不影响存量），最后给存量客户窗口期迁移。四是回退方案——每个灰度版本必须准备数据回退脚本（降级到旧版本时不影响客户业务数据）。五是合同 SLA——灰度期间的 SLA 如何计算需要在合同中说明，通常灰度期只算"努力服务"而非保证 SLA。
* **Q: ToB 项目的成本怎么算给客户看？**
  A: ToB 场景的成本计算要区分"显性成本"和"隐性成本"两部分向客户展示。显性成本：模型 API 调用费（按 token 或按请求）、GPU 算力租赁费（私有化部署）、向量数据库等基础设施费。隐性成本：Prompt 工程和数据准备的人力投入、评估和标注成本、持续维护和模型更新成本。定价模式通常有三种：按调用量（类似 SaaS，每万次请求 x 元，适合调用量不确定的场景）；按席位（每人每月 x 元，适合内部工具类）；混合（基础订阅费 + 超量按调用收费）。向客户报价时建议给出"基准线"——基于 PoC 阶段的平均调用量预测月费用，并提供成本优化建议（缓存命中率、Prompt 压缩率），让客户感觉成本可控而非黑盒。大客户通常要求提供详细的成本分解表。
### 前端AI实战

* **Q: 前端调 LLM API 怎么做流式输出？**
  A: 前端做流式输出的标准做法是用 Fetch API 的 `ReadableStream` 或 `EventSource`。当后端返回 HTTP Streaming（Content-Type: text/event-stream）时，前端逐段读取：`const response = await fetch(url, options); const reader = response.body.getReader(); const decoder = new TextDecoder(); while(true) { const {done, value} = await reader.read(); if(done) break; const text = decoder.decode(value); appendToUI(text); }`。用 `EventSource` 更简单但只支持 GET 请求，不适合需要 POST 请求负载的场景。关键实践：遇到 `\n\n` 认为是完整的一条 SSE 消息再处理（避免切分中文字符）；用 AbortController 支持取消流式请求；设置合理的超时时间（通常 30-60s）；错误恢复——断流后自动重连（指数退避）。Vercel AI SDK 的 `useChat` hook 封装了上述所有逻辑，推荐直接使用。
* **Q: 为什么不能在前端直接调 OpenAI / Claude？**
  A: 直接在前端调用 AI API 是严重的安全风险。核心问题：API Key 暴露——前端 bundle 中放 Key 等于公开，任何人都可以从你的 JS 中提取 Key，然后滥用 API（造成巨额费用）。成本失控——没有后端控制，用户可以直接刷 API，每月账单可能到几十万。数据无法审计——所有请求都直接从浏览器到模型服务，公司无法记录和审计查询内容，合规风险高。模型控制缺失——无法统一管理使用的模型、System Prompt、安全策略。正确的做法是：前端通过自己的后端转发所有 AI API 调用，后端做鉴权、限流、审计、成本控制。后端可以添加自定义逻辑（RAG、缓存、内容过滤）。Vercel AI SDK 的思路是前端调用自己后端的 `/api/chat`，后端在 Edge Runtime 中安全调用 AI API。
* **Q: 流式输出在 React 里怎么处理？**
  A: React 中处理流式输出的标准方案：用 `useState` 维护累积文本，在流式回调中追加文本触发 re-render。性能要点：避免"每收到一个 chunk 就 setState"——chunk 通常很小（几个 token），频繁 re-render 会导致 Markdown 渲染卡顿。优化策略：用 `useRef` + `requestAnimationFrame` 做节流（每 50-100ms 批量更新一次 UI）；用 `useDeferredValue` 或 `startTransition` 让 UI 更新不阻塞交互；消息列表用虚拟滚动（react-virtuoso）避免全量渲染；Markdown 渲染用 `react-markdown` 配合 `remark-gfm`，但需要做增量渲染优化。Vercel AI SDK 的 `useChat` 内置了这些优化，包括按消息粒度管理状态和流式更新的批量处理。
* **Q: 大段文字流式渲染卡顿怎么办？**
  A: 卡顿的根因在于：流式收到的每个 chunk 都触发 Markdown 解析 + DOM 重排 + 虚拟滚动重计算。解决方案从轻到重：一是节流渲染——用 `requestAnimationFrame` 做缓冲，每帧只更新一次 DOM，累积的 token 批量插入（`useRef` 存缓冲，rAF 回调中 setState）。二是增量 Markdown 解析——不要每次全量解析整个消息的 Markdown，只解析新增部分。但 Markdown 是上下文相关的（`**` 可能跨 chunk 匹配），纯增量解析容易出错。稳妥做法是"全量解析 + 虚拟 DOM diff"（用 `react-markdown` 的 `rehypeReact` 做细粒度更新）。三是对超长回复（10000+ tokens）做按需渲染——默认折叠部分内容，用户展开才渲染。四是 Web Worker 渲染——把 Markdown 解析移到 Worker 线程，主线程只负责 DOM 更新。
* **Q: SSE 和 WebSocket 哪个适合 LLM 流式？**
  A: SSE（Server-Sent Events）是 LLM 流式的最佳选择。原因：LLM 流式是"单向"通信（服务端向客户端推送 token），SSE 正好解决这个场景，且基于标准 HTTP 协议（兼容所有负载均衡器、CDN、代理）。WebSocket 是双向全双工协议，对 LLM 流式来说大材小用——LLM 流式只需要服务端推送，SSE 更轻量、自动重连、和 EventSource API 原生集成。WebSocket 的优势在"双方频繁通信"场景（游戏、协作编辑），LLM 对话中用户发送一次请求然后持续接收响应，SSE 天然更合适。但 SSE 的局限：浏览器 EventSource API 仅支持 GET 请求，不能自定义 headers。解决方案是在后端做 SSE Proxy（前端 POST 到后端，后端转 SSE），或者用 Fetch API + ReadableStream 自己实现 SSE 客户端（Vercel AI SDK 的做法）。
* **Q: 怎么取消正在流式的请求？**
  A: 用 AbortController 实现。前端创建 `AbortController`，把 `controller.signal` 传给 fetch 请求。需要取消时调用 `controller.abort()`，fetch 请求会抛出 `AbortError`，在 catch 中处理。流式读取时也要检查 signal 状态：`while(!reader.closed && !signal.aborted) {...}`。后端需要响应前端的中断：当 HTTP 连接断开时（Node.js 的 `req.on('close', ...)` 或 Python FastAPI 的 `request.is_disconnected()`），后端应停止 LLM 生成并释放资源。实践中，后端是一个关键环节——如果前端取消了但后端还在继续调用 API，会产生浪费。在 Python 端可以用 `asyncio.Task` 取消或设置 `stop` 事件。Anthropic/OpenAI 的 SDK 都支持传递 `AbortSignal` 来自动响应客户端取消。
* **Q: Token 预算怎么在前端做提示？**
  A: Token 预算提示的核心是"不让用户发出必然超长的请求"。做法：前端实时计算输入文本的 token 数（用 `tiktoken` 或 `js-tiktoken` 库，取模型对应的 encoder），在用户输入时显示计数（如"128/4000 tokens"）。如果超过模型上下文窗口的 70% 显示警告，超过 90% 阻止发送并提示"消息过长"。关键要点：用模型实际的 tokenizer（不同模型编码不同，GPT-4 的 tiktoken 和 Claude 的 claude-tokenizer 不一样），不能按字符估算（中文 1 个 token ≈ 1.5 字，英文 ≈ 3.5 字符）。在输入框下方显示进度条（绿/黄/红三段），并给出建议（"摘要图片描述以节省空间"）。对于上传文件（图片/文档），预估文件编码后的 token 数一并计算。
* **Q: 错误怎么向用户展示？**
  A: AI 应用的错误展示核心原则：不要让用户看到原始错误堆栈或 API 错误码。错误分类展示：超时类——"响应时间过长，已中断。你可以重试或简化问题"；内容违规——"该请求包含受限内容，已拦截"；服务不可用——"AI 服务暂时不可用，请稍后再试"（配合自动重试）；token 超限——"对话太长，请开启新会话"；模型幻觉/低质量——不直接展示错误，而是委婉提示"结果可能不够准确，建议核实关键信息"。实践中建立错误码映射表：后端返回标准化 API 错误码（如 `AI_TIMEOUT`、`CONTENT_FILTERED`），前端统一渲染对应的用户友好文案。对于瞬时错误，前端自动重试 1-2 次再展示错误。错误展示时留"重试"和"反馈"按钮。
* **Q: ChatGPT 那种"消息列表"怎么实现？**
  A: 核心是消息数据结构的设计。每条消息包含：`id`（唯一标识）、`role`（user/assistant/system）、`content`（文本或多模态内容块）、`timestamp`、`status`（sending/streaming/done/error）、`metadata`（token 数、模型名、推理耗时）。消息列表用数组存储，通过 `id` 更新单条消息（流式追加 content）。UI 实现：用虚拟滚动（react-window/infinite-react）：只渲染可视区域的消息，保证千条消息不卡顿。每条消息组件分类型渲染——用户消息右对齐、AI 消息左对齐+头像+Markdown 渲染。流式消息特殊处理：用 `useRef` 持有当前 streaming 的消息对象，逐 token 更新其 content，避免全列表 re-render。消息发送时先添加"占位消息"（status: sending），收到完整响应后更新。关键注意：会话列表排序按最后一条消息时间降序，消息加载用无限滚动（向后端请求 older messages）。
* **Q: 怎么管理多个会话状态？**
  A: 前端：会话列表用本地存储（IndexedDB/LocalStorage）缓存最近 30-50 个会话的元数据（标题、最后消息预览、时间戳）。会话消息全文存后端，前端只缓存当前打开会话的消息。切会话时从后端拉取（API: `GET /conversations/:id/messages?before=<msg_id>&limit=50`）。后端：会话数据存数据库，表结构——`conversations(id, user_id, title, model, created_at, updated_at)` 和 `messages(id, conv_id, role, content, token_count, created_at)`。关键优化：对话标题自动生成（用户首条消息发送后，调用 LLM 生成 5-10 字标题）；消息分页加载（默认只拉最后 50 条，滚动到顶部加载更早消息）；删除/归档会话软删除。多设备场景需要考虑冲突问题（用户在手机和电脑同时使用同一会话），通常策略是 "last-write-wins"。
* **Q: AI 对话用 Edge Runtime 还是 Node？**
  A: Edge Runtime（Vercel Edge、Cloudflare Workers）和 Node Runtime 各有优劣。Edge 的优势：冷启动近乎 0、全球边缘部署延迟低、自动扩缩容。Node 的优势：完整的 Node.js API 支持（文件系统、Socket、子进程）、原生包兼容性好（很多 AI SDK 需要 Node-specific API）。AI 对话场景推荐 Node Runtime（或 Vercel 的 Node.js 函数），原因：AI 对话是长时间流式连接（可能持续 30s+），Edge Function 的超时限制（Vercel Edge 60s、Cloudflare 30s）对长对话不友好；LLM SDK 的 streaming 实现依赖 Node 的 Stream API；RAG 场景需要文件系统访问和数据库连接池。但 Edge 适合轻量级场景——Token 计数、输入校验、缓存查询。最佳实践：用 Node 做核心 AI API（流式转发），用 Edge 做静态资源和前端渲染。
* **Q: 怎么实现"图片 + 文字"混合输入？**
  A: 多模态输入的关键是前端消息结构的改造。消息 content 不再是纯字符串，而是 content block 数组：`[{type: "text", text: "描述这个"}, {type: "image_url", image_url: {url: "data:image/jpeg;base64,..."}}]`。前端实现：输入框支持拖拽/粘贴/上传图片，图片以压缩后的 base64 或缩略图展示在输入框上方，用 `contentEditable` 或定制的 `div` 实现"文字中穿插图片"的体验。上传后显示缩略图和删除按钮。技术难点：图片压缩（大图转 JPEG 80% quality 减少 token）、图片上传方式选择（base64 嵌入消息 vs 上传到 CDN 后传 URL——后者在私有化部署中需要处理文件存储权限）。OpenAI GPT-4o 和 Claude 3.5 都支持多模态输入。后端转发时保持 content block 结构不变。
* **Q: Markdown 增量渲染怎么处理？**
  A: Markdown 增量渲染的挑战在于语法块跨 token 边界。例如 `**bold**` 可能第一个 chunk 收到 `**bo`，第二个收到 `ld**`，分两次渲染会导致错误的中间状态。两种策略：一是"全量重渲染 + 虚拟 DOM diff"——每次更新用完整的 Markdown 文本重新解析，但依赖 React 的虚拟 DOM 做增量更新（react-markdown + rehype-react）。数据量大时（1000+ tokens），全量解析有性能压力。二是"按段落增量渲染"——识别 Markdown 的天然分块边界（空行 `\n\n`），按段落切分，已渲染的段落不变，只追加新段落。代码块特殊处理：等反引号闭合后再渲染（开始代码块时不渲染内容，收到结束反引号后一次性渲染整个代码块）。实践中用方案二 + 代码块延迟渲染，配合 requestAnimationFrame 做更新节流。
* **Q: AI 应用的埋点要监控什么？**
  A: AI 应用的埋点比传统应用多一个"模型行为"维度。核心技术指标：调用量（QPS、日活）、延迟（TTFT——首 token 时间、TPOT——每个输出 token 时间、总响应时间）、错误率（超时/限流/内容过滤/模型报错）、Token 消耗（输入/输出 token 数、按模型和用户维度聚合）。质量指标：用户满意度（点赞/踩、反馈率、重新生成次数——低质量回答的标志）、Context Usage（实际上下文填充率——对排查 token 浪费有用）、工具调用成功率（Agent 场景下工具调用的准确率和完成率）。业务指标：留存率、对话深度（平均每会话轮数）、功能使用分布（哪些 RAG 知识库被频繁查询）。工具选型：PostHog（开源产品分析 + 事件追踪）+ Langfuse（LLM trace 成本）是一个常见组合。
* **Q: AI 应用的"灰度发布"怎么做？**
  A: AI 应用灰度发布的维度不同于传统功能。核心灰度维度：模型版本（先用 GPT-4o-mini 验证，再决定是否上线 GPT-4o）、Prompt 版本（新 Prompt 模板在小流量上跑效果对比）、System Prompt 策略（不同类型的 system prompt 对不同用户的效果差异）。灰度流程：定义灰度指标（回答准确率 LLM-as-Judge + 用户满意度），设置灰度比例（5%->20%->50%->100%），每个阶段评估 24-48 小时，对比基线。关键工具：Feature Flag 系统（LaunchDarkly/Unleash）做用户分桶；A/B 测试框架评估效果差异。需要注意的是：LLM 生成的"质量"很难自动化评估，需要 LLM-as-Judge + 人工抽检结合。灰度期间保持"一键回退"能力——回退到旧模型版本 + 旧 Prompt 组合。
* **Q: AI 应用的成本怎么算和优化？**
  A: AI 应用成本 = API 调用费（输入 token + 输出 token）× 调用次数 + 基础设施（向量数据库、GPU 租赁）+ Prompt 工程和评估人力。优化策略从高到低：一是 Prompt 压缩——缩短 System Prompt（移除不必要指令、用更短的表述），减少 Few-shot 例子数量，每减少 1000 输入 token 在 GPT-4 上省约 $0.03/请求。二是缓存——相同请求走缓存不调模型（Semantic Cache，用 embedding 相似度匹配缓存结果），高重复场景可减少 30-50% 调用量。三是模型选择——简单任务用小模型（GPT-4o-mini/Claude Haiku），复杂任务才用大模型。四是 Batch API——非实时场景用 OpenAI Batch API（50% 折扣）。五是蒸馏——训练专用小模型替代通用大模型。六是 Prompt Caching（Anthropic/OpenAI 支持长 prompt 前缀缓存，可省 50%+ 输入 token 费用）。
* **Q: AI 应用的"国际化"（i18n）有什么特别？**
  A: AI 应用的国际化比传统应用多一层"模型的语言能力"。UI 文本的 i18n 和传统应用一样（用 react-i18next/next-intl 管理翻译文件）。特殊点在于：模型 System Prompt 需要多语言版本——中文、英文、日文等版本的指令措辞不能直接机器翻译，需要本地化适配（不同文化对"礼貌"的理解不同）。另外，模型输出语言需要控制——如果用户用中文问但模型用英文答是糟糕的体验，需要 System Prompt 明确"用用户输入的语言回答"。多语言模型的选型也需要考虑——Claude 的中文和英文都强，某些国产模型对东南亚语言支持更好。RAG 知识库的多语言也要注意——用户用中文问但知识库只有英文文档时，检索要支持跨语言 embedding（如 multilingual-e5-large）。
* **Q: AI 应用的"乐观更新"怎么做？**
  A: AI 应用的乐观更新指"用户发送消息后立即在 UI 中显示，不等后端响应"。做法：用户点发送后立即把消息插入列表（`status: 'pending'`），同时发起 API 调用。API 返回流式结果后更新该消息的 content（`status: 'streaming' -> 'done'`）。如果 API 失败，把消息状态改为 `error` 并显示重试按钮。好处是交互感觉零延迟。注意事项：乐观更新的消息 id 需要在客户端生成（`crypto.randomUUID()` 或 `nanoid`），和后端返回的 id 做映射。如果消息需要经过内容审核（敏感词检查），需要在乐观显示和审核通过之间做权衡——通常先乐观显示，后台异步做审核，发现违规时替换为"该内容已被拦截"。乐观更新 + 流式输出的组合是 ChatGPT 类产品的标准体验。
* **Q: AI 自动补全代码（类似 Copilot）怎么实现？**
  A: 核心原理：监听编辑器变化（Cursor 监听、或 contentEditable 的 input 事件），在光标位置计算出"上下文"（光标前 N 行 + 当前文件类型），发送给 LLM API 请求补全。实现关键：上下文构建——只包含光标前最近的代码（不需全文，200-300 tokens 足够），加上文件扩展名和相邻文件的导入。补全触发——可以是"每 200ms 无输入后自动触发"或"用户按 Tab 手动触发"。显示方式——补全内容以灰色文本插入在光标后，用户按 Tab 接受，继续输入自动忽略。技术栈：Monaco Editor 或 CodeMirror 提供了插件 API 来管理补全提示。前端需要处理：补全请求的防抖和取消（每次新输入取消上次补全请求），以及流式接收补全内容（逐 token 展示，类似打字效果）。生产级方案参考 Continue.dev（开源 AI 代码助手）的实现。
* **Q: AI 应用要不要 PWA / 离线支持？**
  A: AI 对话应用对 PWA/离线支持的需求较低，因为核心功能（对话）依赖网络。但可以做部分离线：本地缓存历史会话（IndexedDB 存最后 50 个会话的摘要），离线时只读浏览历史（不能发新消息）。PWA 主要价值在"安装到主屏幕"和"消息推送"。Service Worker 可以缓存应用 shell（HTML/CSS/JS），但 AI 对话的实时性使得离线使用场景很有限。值得做 PWA 的场景：笔记类 AI 助手（离线可看笔记）、文档编辑 + AI 辅助（离线可编辑文档，在线时 AI 自动处理）。如果目标市场是移动端低频网络环境（如地铁），可以考虑离线缓存最后一次会话的完整结果。总体建议：如果目标是桌面端用户，PWA 不是优先项；如果是移动端 Web，PWA 的安装体验值得做。
* **Q: Vercel AI SDK 的 useChat 怎么用？**
  A: Vercel AI SDK 的 `useChat` hook 封装了完整的对话管理。用法：`const { messages, input, handleInputChange, handleSubmit, isLoading, reload, stop } = useChat({ api: '/api/chat', initialMessages, body: { model: 'gpt-4' } })`。它在内部做了：消息列表管理（messages 数组）、流式接收（自动解析 SSE 流）、输入状态绑定（handleInputChange）、滚动锁定（新消息自动滚到底部）、错误处理、重新生成（reload 重新发送最后一条消息）。前端只需渲染 messages 数组。后端需要实现 `/api/chat` 路由：接收 `{ messages, ...body }`，调用 AI SDK 的 `streamText` 返回流式响应。Vercel AI SDK 还支持工具调用（`tools` 属性），`useChat` 自动处理工具调用的生命周期。生产扩展：持久化 messages 到数据库（在 onFinish 回调中保存），多会话管理（用 id 区分）。
* **Q: 消息编辑 / 重新生成怎么实现？**
  A: 消息编辑：用户编辑已发送的消息内容，触发重新生成。实现逻辑：将编辑后的消息及其之后的所有消息删除，用编辑后的消息作为新起点重新请求 AI。前端需要做：进入编辑模式（双击消息或点编辑图标），保存编辑后的内容，调用 reload API 发送新消息序列。注意：编辑用户消息时要同时删除后续的所有 AI 回复，否则上下文不一致。重新生成：不需要编辑直接让 AI 重新回答同一条消息。实现：调用 `reload()`（Vercel AI SDK 内置），删除当前 AI 回复，重新发送相同的消息列表给模型。由于模型生成的随机性（即使 temperature=0），新回复可能不同。用户可以在多个回复间切换（查看历史回复），UI 上显示"第 1/3 个回复"的切换控件。后端需要保存每次重新生成的回复（而非覆盖），最终用户选择一个满意的。
* **Q: 对话分支 / Fork 怎么做？**
  A: 对话分支是在某条消息处创建新的对话分支，保留原对话不变。数据模型：消息添加 `parent_id` 字段，原始会话是线性链表，分支产生"多叉树"结构。展示方式：ChatGPT 的做法——分支消息前显示"分支"标记，点击切换到该分支；或更直观的树形侧边栏。实现要点：分叉点是 `parent_id` 变化的位置——从消息 A 产生两个子消息 B1 和 B2，则是两个分支的起点。前端渲染需要从根消息开始，按用户选择的分支路径展开。后端 API 需要支持 `GET /conversations/:id/branches`（获取所有分支）和 `POST /conversations/:id/fork`（在指定消息处创建分支）。复杂度在于 UI 展示——线性对话用户习惯最强，分支会显著增加认知负荷。大多数产品只在 Pro 功能中提供分支（如 Claude），普通用户保持线性体验。
* **Q: 语音输入 / TTS 怎么集成？**
  A: 语音输入：浏览器 Web Speech API 的 `SpeechRecognition`（Chrome 支持好，Safari/Firefox 有限）。更稳定的方案是用云服务——Deepgram/Whisper（OpenAI）/Azure Speech，实时语音转文字。前端通过 `MediaRecorder` 采集音频流，发送到 ASR 服务获得识别文本。关键点：Web Speech API 在移动端 Chrome 可用但精度一般；生产环境推荐 Deepgram 或 Whisper API，支持实时流式识别（边说话边出文字）。TTS 输出：浏览器 Speech Synthesis API 最简单（音质一般，支持有限），ElevenLabs（音质最好，延迟较低），OpenAI TTS（性价比高，延迟低）。实现方式：AI 回复完成后（或流式完成时），把完整文本传给 TTS 播放。如果追求实时体验，可以逐句 TTS（按句号分句，每句独立 TTS，实现"边说边出"效果）。一般建议提供"文字优先，语音辅助"的交互，即默认只显示文字，用户点击"朗读"才触发 TTS。
* **Q: 文件上传 + 处理流怎么做？**
  A: 文件上传 + AI 处理的标准流程：前端上传文件到后端 -> 后端解析提取文本 -> 把文本注入上下文 -> 调用 LLM。前端：支持拖拽/点击上传，上传时显示进度条，文件类型和大小限制在前端先校验。上传方式：直接上传到后端（适合小文件，<10MB），或上传到对象存储（S3/MinIO）再传 URL（大文件，推荐）。后端处理流：接收文件流 -> 根据 MIME type 路由到不同的解析器（PDF 用 PyMuPDF/unstructured，Word 用 python-docx，图片用 OCR/多模态模型）-> 提取文本 -> Chunking（如果文本太长） -> 存入临时上下文或向量数据库。用户体验要点：文件上传过程要显示状态（上传中->解析中->完成），让用户知道进度；解析完成后立即发送给 LLM 处理，形成"上传-分析"的连续流。大文件（>30MB）建议后台异步处理，前端轮询或 WebSocket 获取状态。
* **Q: Markdown 渲染中的 XSS 安全？**
  A: AI 生成的 Markdown 内容可能包含恶意脚本标签（`<script>`、`<img onerror>`、`<a href="javascript:">`），必须处理。安全策略：使用专门的 Markdown 渲染库（react-markdown/remark）而非 `dangerouslySetInnerHTML`；配置 `rehype-sanitize` 或 DOMPurify 过滤危险标签和属性；使用 `allowElement` 和 `allowAttribute` 白名单（允许 `code`、`pre`、`a` 等安全标签，不允许 `script`、`iframe`、`on*` 事件属性）。额外注意：代码块中的文本应保留（不应转义），只有渲染时解析的 HTML 标签才需过滤。链接安全：对外链添加 `rel="noopener noreferrer"` 和 `target="_blank"`。还有一个 AI 特有的 XSS 风险——用户通过 Prompt 注入让 AI 生成恶意 Markdown，所以即使 AI 是"可信"的，渲染也必须做 sanitize。
* **Q: 移动端 AI 应用有什么特殊问题？**
  A: 移动端 AI 应用的核心特殊性：网络不稳定——移动网络可能频繁切换（WiFi->4G->弱信号），流式请求容易中断，需要实现断线自动重连（指数退避）和请求队列（网络恢复后重发）。内存限制——移动端浏览器内存有限（iOS Safari 通常 1-2GB），大量消息 + Markdown 渲染容易导致页面崩溃，需要更激进的虚拟滚动和消息缓存（只保留可视区域的消息，其余存到 IndexedDB）。交互差异——移动键盘的"发送"按键优先级低，更好的体验是输入框旁边的发送按钮或语音输入；流式输出时自动滚动到最新消息需要更精细的控制（用户手动回看历史时不能强行滚动）。性能——Markdown 全量渲染在手机上更卡，建议限制单条消息长度（超长消息折叠）。字号——移动端阅读长 AI 回复需要更大的行高和字体。
* **Q: 怎么实现"AI 自动补全代码"（Copilot 同款）？**
  A: 这是 Q202 的延伸。核心实现分三步。第一步——编辑器集成：Monaco Editor / CodeMirror 提供占位文本（ghost text）渲染 API，补全内容以半透明灰色显示在光标后。第二步——上下文构建：收集光标前的代码（包括缩进和上下文语言标识）、光标后的代码（用于检测补全是否合适）、当前文件类型和相邻文件名。上下文限制在 200-300 tokens，避免响应太慢。第三步——补全触发和渲染：用户停止输入 200ms 后触发补全请求（防抖），用 AbortController 取消上一条未完成的补全。流式接收补全内容（逐 token 渲染），用户按 Tab 接受（补全内容变为真实文本），继续输入自动忽略。Continue.dev 是开源的参考实现，支持多个 LLM 后端和 IDE。
* **Q: 怎么把 AI 集成到富文本编辑器（TipTap / Lexical / Slate）？**
  A: AI 编辑器集成通常提供三个功能：补全（suggestions）、改写、和对话。TipTap（基于 ProseMirror）的集成方式：用 `Extension` 注册 AI 命令——`/ai` 斜杠唤起 AI 菜单，选择"继续写"、"改写"、"总结"等操作。实现方式：选中的文本作为 prompt 的上下文，发送给 LLM API，流式接收结果替换选中内容。关键实践：编辑器需要支持"异步内容替换"——AI 正在生成时，选中区域显示加载动画，生成内容逐步流入。Lexical（Meta 开源）的做法类似，提供 `LexicalAI` 插件管理 AI 交互状态。Slate 最底层，需要自己实现事务管理。TipTap 是最推荐的——API 完善、Node/Mark 扩展机制成熟、社区已有 AI 插件（如 `@tiptap-pro/extension-ai`）。核心挑战：AI 生成的流式内容不能破坏编辑器的 Undo/Redo 栈，需要在 AI 输出完成后一次性提交事务。
### AI编程工具

* **Q: 你日常用哪些 AI 工具？典型的工作流是什么？**
  A: 日常工具组合：Claude Code（主要代码开发和重构）、Cursor（补全和文件级编辑）、Copilot（轻量补全）、Claude.ai/ChatGPT（复杂设计和技术调研）、Perplexity（查文档和学习新框架）。典型工作流：早上先让 Claude Code 过一遍前一天的 PR 评论和未完成任务；开发时 Cursor 实时补全；遇到复杂功能用 Claude Code 的 Agent 模式做多文件重构；写完后让 Claude Code 生成测试和文档；PR 前用 AI 做 Code Review。技术调研时用 Perplexity 查资料 + Claude 分析对比，把结论用 Claude 整理成文档。一个提效关键点是"Prompt 模板化管理"——把常用的指令（code review、commit message、测试生成）保存为模板，减少重复输入。
* **Q: Cursor / Claude Code / Copilot 这些 AI 编程工具的本质区别？**
  A: Copilot（GitHub/OpenAI）：最早普及的 AI 编程助手，核心是"行内补全"——在光标位置预测下一段代码，适合简单重复的编码。基于 GPT-4o 的 Copilot Chat 支持对话但功能有限。Cursor：基于 VS Code 的 AI IDE，核心是"编辑器深度集成"——选中的代码可以触发 AI 操作（重构、解释、修改），支持多文件编辑、Agent 模式、Claude/GPT-4 等多模型。Cursor Tab 的补全质量优于 Copilot（能理解更大上下文）。Claude Code（Anthropic）：终端工具，核心是"Agent 式编程"——给它一个任务描述，它自主读代码、改代码、跑测试、提交 PR。本质差异：Copilot 是"补全"，Cursor 是"辅助编辑"，Claude Code 是"自主 Agent"。三者不冲突：Copilot 做轻量补全，Cursor 做文件级编辑，Claude Code 做复杂任务。实际工作中三件套配合使用效率最高。
* **Q: AI 写代码最容易翻车的几种情况？**
  A: 一是创建"看起来对的假代码"——函数签名正确但内部逻辑有微妙错误（边界条件未处理、并发问题），单元测试不一定能发现。二是幻觉 API——编造不存在的库函数或方法名（把不同框架的 API 混在一起），在 TypeScript 里常表现为 import 了不存在的类型。三是上下文迷失——处理跨多文件的修改时，忘记同步更新相关类型定义和接口签名，导致类型错误。四是过度复杂——AI 倾向于加新抽象层（HOC、装饰器、工厂函数），把简单逻辑过度工程设计。五是"回滚陷阱"——AI 有时会删除已有的正确代码，引入新实现但不兼容旧接口。应对策略：始终对 AI 生成的代码手动审查边界条件；让 AI 先读相关文件再改（提供完整上下文）；指定"最小改动原则"限制它的发挥空间；复杂重构时要求 AI 先生成测试用例再改代码。
* **Q: 怎么写一个高质量的 AI 编程指令？**
  A: 高质量 AI 编程指令的四个要素。一是明确角色和约束——"你是一个资深 React 工程师，遵循 TypeScript 严格模式，代码不需要注释因为类型已经自文档化"。二是给反例——"不要使用 any 类型，不要引入新的依赖，如果现有代码中有类似功能请复用而非新建"。三是提供充分上下文——把相关文件的内容（或文件路径）作为指令的一部分，"修改 src/services/user.ts 中的 fetchUser 函数，它的返回类型在 src/types/user.ts 中定义"。四是要求输出格式——"请输出完整的文件内容（不要 diff），包含所有 import 语句"。核心原则：指令越具体，AI 翻车概率越低。"重构这段代码"是坏指令，"把这段代码的 for 循环改成 map/filter 链式调用，并提取出独立的验证函数"是好指令。
* **Q: AI 写完代码你怎么 review？**
  A: AI 生成代码的 review 重点不同于人类代码。第一看"逻辑是否正确"——AI 写的条件判断、边界处理、错误处理是否正确？很多时候 AI 写出"看起来对的假逻辑"。第二看"是否引入了幻觉"——调用的函数/API 是否真实存在？import 路径是否正确？第三看"是否过度设计"——AI 是否引入了不必要的抽象？第四看"安全性"——AI 是否把敏感信息硬编码了？是否有注入风险？第五看"是否符合现有代码风格"——命名规范、错误处理模式是否与项目一致。工具层面：用 Claude Code / Cursor 的 diff 视图清晰展示 AI 的改动（不要接受"全文件替换"式的改动，容易隐藏问题）。最佳实践：让 AI 先生成变更的测试代码，再生成实现代码——测试通过验证的实现通常更可靠。最终准则是：AI 代码和人类代码一样需要 review，不能因为是 AI 生成的就不审查。
* **Q: AI 帮调 bug 应该怎么用？**
  A: 有效做法：把完整错误信息（包括 stack trace、相关代码行、输入数据）贴给 AI，告诉它"你期望的行为"和"实际得到的行为"。AI 擅长根据 stack trace 定位错误根源。具体工作流：第一步——复制完整错误信息和出错的代码段发给 AI，让 AI 分析可能原因。第二步——AI 给出修复建议后，不要直接接受，而是让它解释为什么原代码出错了（验证它真正理解了问题）。第三步——要求 AI 写出修复代码并解释改了什么。第四步——如果修复涉及多文件，让 AI 列出所有需要改动的文件。注意：AI 在调试时容易提出"绕开问题"而非"解决问题"的方案（用 try-catch 吞掉错误而不是修复根因），需要在 prompt 中强调"请修复根本原因而非掩盖错误"。同时要检查 AI 建议的修复是否引入了新的安全问题。
* **Q: AI 帮写单元测试该怎么用？**
  A: AI 写单元测试是最实用的场景之一。工作流：把源文件 + 测试框架的配置（Vitest/Jest） + 测试风格偏好发给 AI，要求生成完整的测试文件。关键指令——"测试所有公开函数，覆盖正常路径、边界条件（空数组、负数、null）和错误路径；使用 describe/it 组织测试；不要 mock 外部依赖除非必要"。AI 擅长"给定输入输出生成测试"——给函数的签名和注释就能生成全面的测试用例。但 AI 不擅长"测试函数的副作用"——需要人补充对数据库写入、文件系统操作等副作用的测试。提效技巧：一次让 AI 生成多个测试文件；用 AI 生成的测试作为"活的文档"——测试用例本身展示了 API 的使用方式（对新人 onboarding 有用）。检查测试质量的指标：AI 是否测试了错误路径？测试是否真正验证了结果（有 assert）？测试是否独立？（一个测试失败不应该导致其他测试也失败。）
* **Q: AI 帮 code review 怎么用？**
  A: AI Code Review 可以覆盖人类容易遗漏的维度。标准工作流：在 CI 中接入 AI Code Review（如 Claude Code review、CodeRabbit、Copilot Code Review），每次 PR 自动触发。AI review 检查的重点：类型安全——是否有隐式的 any、类型断言是否安全；代码规范——是否遵循项目约定（命名、文件结构、错误处理模式）；性能——是否有不必要的 re-render、大对象深拷贝、O(n^2) 循环；安全性——是否有 SQL 注入/XSS/敏感信息泄露风险；测试覆盖——新代码是否有对应测试。AI review 的弱项：理解业务逻辑是否正确（AI 不知道业务需求是什么）、判断设计决策是否合理（用 A 方案还是 B 方案）。最佳实践：AI 做初步 check（阻塞性的问题），人工 review 做 final sign-off（业务逻辑和设计决策）。不要让 AI review 替代人工 review，它应该作为人工 review 的前置过滤。
* **Q: AI 帮写文档 / commit message / PR 描述？**
  A: AI 最适合的是"根据代码差异生成摘要"。commit message：`git diff --cached` 的输出发给 AI，要求"用 conventional commit 格式生成 1-2 句描述，解释为什么做这个改动而非只描述做了什么"。Claude Code 和 Copilot 都有内置的 commit message 生成功能。PR 描述：把 diff + 相关 Issue 链接发给 AI，让 AI 生成包含"改动概览、关键决策、测试说明、截图（如有）"的 PR 描述。文档：AI 擅长从代码生成 API 文档（JSDoc/Swagger），但不擅长写"设计文档"（需要理解业务背景和权衡）。最佳实践：AI 写初稿，人类补充"为什么"部分的解释和上下文。效率和质量的平衡点：AI 做 80% 的"机械性"写作，人类补充 20% 的关键洞察。
* **Q: AI 帮助设计 API / 数据结构靠谱吗？**
  A: 部分靠谱。AI 对"已有成熟模式的 API 设计"表现很好——RESTful CRUD、GraphQL Schema、TypeScript 类型定义、Prisma Schema 等，因为这些模式在训练数据中大量出现。给出业务描述后 AI 能生成合理的 API 接口和数据结构定义。不靠谱的地方：需要深度理解业务领域和业务规则的 API 设计——比如复杂的计费系统、权限模型、工作流引擎，AI 不理解业务约束和隐含的规则。使用方式：用 AI 生成初版设计方案作为"讨论起点"（快速得到 60 分的设计），人工 review 和修改来补齐业务理解。不要期待 AI 一次给出生产级 API 设计。推荐工作流：先让 AI 根据需求生成 OpenAPI/Swagger 规范的 API 设计 → 人工 review 修改 → 用 spec 生成 mock server → 前后端并行开发。
* **Q: AI 改造遗留代码（legacy code）的正确姿势？**
  A: 遗留代码改造是最容易被 AI 搞砸的场景。正确姿势：第一步"只读不改"——让 AI 先阅读并解释代码的功能（生成文档），确保你理解了现有逻辑。第二步"写测试再改"——要求 AI 先为现有代码生成"特性测试"（characterization tests），锁定当前行为。第三步"小步重构"——让 AI 一次只做一个小改动（提取函数、重命名变量、拆分模块），每步都跑测试验证。严禁的做法：让 AI 一次重写整个遗留模块——在大幅重构中 AI 很容易丢失隐含的业务逻辑（特殊 case、边界条件、性能优化）。正确做法是"Stangler Fig 模式"——AI 辅助在新系统中增量实现功能，逐步替换旧系统。AI 最适合遗留代码的：生成文档、添加类型注解、写测试、提取重复代码为公共函数。不适合的：大规模架构重构、替换核心业务逻辑。
* **Q: AI 帮选技术栈 / 框架对比靠谱吗？**
  A: 让 AI 做技术选型对比需要谨慎。AI 的优势：提供主流选项的客观对比（特性表、性能数据、社区活跃度）、生成 demo 代码验证可行性。AI 的局限：训练数据的时效性（新版本/新框架的信息可能不准确）、对团队背景不了解（AI 不知道你的团队擅长什么、运维能力如何）、对隐藏成本不敏感（某个框架看似完美但部署复杂）。正确用法：把选型问题分解——"列出 3 个可选方案，对比它们的性能、学习曲线、社区支持、部署要求，各给一个最小 demo 代码"，而不是"帮我选一个"。AI 提供信息让你做决策，而不是让 AI 替你决策。最终的选型决策永远是人的责任——AI 不知道你的组织架构、团队技能、长期规划。
* **Q: 怎么避免对 AI 过度依赖？**
  A: 过度依赖 AI 的表现：不加审查直接使用 AI 代码、被 AI 生成的错误结论引导方向、失去独立解决问题的能力。避免方法：一是保持"review 习惯"——所有 AI 输出都视为"初稿"，必须经过审查才能使用。二是隔一段时间不用 AI"纯手写"——保持编码手感，检查自己是否还有不靠 AI 编码的能力。三是理解 AI 输出的每一行代码——不要"复制粘贴然后相信它"，面试时 AI 帮不了你。四是用 AI 做"学习加速器"而非"替代思考"——让 AI 解释为什么这么做，而不是只拿结果。五是在团队中设立"AI 使用规范"——明确哪些可以用 AI（测试、文档、模板代码），哪些不能（核心业务逻辑、安全关键代码）。六是定期做无 AI 日——"每周半天不碰 AI 工具"，独立思考和解决问题。
* **Q: AI 帮做需求分析 / PRD 解析？**
  A: AI 擅长从 PRD 中提取结构化的信息。工作流：把 PRD 文档（可能是飞书/Notion/Word）粘贴给 AI，要求提取：功能列表、用户角色、关键约束、数据的输入输出、验收标准（AC）。AI 可以输出结构化格式（markdown table 或 JSON schema）。进阶做法：让 AI 根据 PRD 输出"用户故事地图"、"数据流图"、"API 接口定义"，作为开发前的设计文档。AI 也能做需求冲突检测——如果 PRD 中 A 部分和 B 部分矛盾（"支持匿名访问" vs "所有接口需鉴权"），AI 可以标注出来。局限：AI 无法理解"没说出来的需求"（业务方默认的常识），也不能判断需求优先级。所以 AI 解析的 PRD 是"粗糙的初稿"，需要产品经理和开发 review 和补充。
* **Q: 怎么让 AI 帮你"读代码 / 接手老项目"？**
  A: 核心方法：让 AI 逐层解析代码库。第一步——项目总览：让 AI 读 README、package.json、项目目录结构，输出"这个项目是做什么的，用了什么技术栈，主要模块有哪些"。第二步——核心流程解析：让 AI 追踪一条"用户请求"经过的代码路径（从入口文件到数据库），画数据流图或时序图。第三步——依赖关系分析：用 AI 生成模块依赖图（哪些文件依赖哪些文件），识别核心模块和耦合度。第四步——生成文档：让 AI 为关键模块和函数生成注释和文档。工具支持：Claude Code 的 `/init` 命令会自动生成项目概要；Cursor 的 "Codebase Index" 可以跨文件搜索和理解代码。关键注意：分批喂给 AI（不要一次把几万行代码全塞进上下文），按模块或按功能逐块分析。AI 读代码的结论需要用"验证问题"来检查（例如"这个函数的返回值是什么类型"）。
* **Q: AI 帮写脚本（一次性 ops 脚本）的正确姿势？**
  A: AI 写一次性脚本的准确率很高，因为这是它的训练数据中最常见的模式。正确姿势：提供明确的需求描述——输入是什么（文件格式、数据源）、输出是什么（期望的结果）、约束条件（运行环境、执行时间、安全要求）。然后分两步：先让 AI 生成脚本并审查逻辑，再让 AI 生成对应的测试数据或测试命令。关键注意：脚本需要处理错误和边界条件——AI 经常忘记处理文件不存在、网络超时、空数据等情况，需要在 prompt 中明确要求。安全方面——AI 写的脚本可能包含危险命令（`rm -rf`、`DROP TABLE`），务必逐行审查。建议：让 AI 先打印"dry-run"模式（只输出将会做什么而不真正执行），确认无误后再运行。一次性脚本不需要最优性能，但需要可读性和错误处理。
* **Q: 让 AI 帮"写英文 / 改邮件 / 翻译" 的注意点？**
  A: AI 做文字润色和翻译非常成熟。核心注意点：一是"保持原意不篡改"——AI 倾向于润色时"发挥"（加内容/改语气），需要明确"不要新增信息，只改善表达"。二是"区分事实核查——AI 翻译英文时要小心它把组织名、产品名、人名也"翻译"了（如把 "OpenAI" 翻成"开放 AI"）。三是对文化差异敏感——AI 可能不了解特定文化语境中的表达，尤其是涉及跨文化沟通的邮件。四是指定目标受众——"这个邮件是写给美国客户 CEO 的，请使用正式但友好的语气"。五是"长文本切分"——超长文本分段处理，避免 AI 遗漏后半部分的内容。推荐工作流：先让 AI 做直译/初稿，人工调整关键术语和语气，再让 AI 做二轮润色。用 AI 做英文写作用工具：DeepL Write（英语润色专业）、Claude/GPT（通用翻译 + 润色）。
* **Q: AI 帮"画架构图 / 时序图" 怎么用？**
  A: AI 生成架构图的最佳路径是"文本描述 -> 图代码 -> 自动渲染"。标准做法：让 AI 输出 Mermaid.js 或 PlantUML 格式的图描述，然后粘贴到 Mermaid Live Editor 或集成工具（如 Notion/飞书都支持 Mermaid）中渲染。例如给 AI 描述"用户请求经过 Nginx 到 API Gateway 再到微服务 A 和 B，A 调用 Redis 缓存和 Postgres 数据库"，AI 输出 Mermaid 的 `flowchart LR` 或 `sequenceDiagram`。关键技巧：要求 AI 把节点关系写清楚（包括数据流方向和协议）、注出关键技术组件（消息队列、缓存、数据库）。时序图适合 AI 描述复杂交互流程——"用户注册的完整流程，包括邮件验证和欢迎通知"。Claude Code 可以直接生成 Mermaid 并预览。局限：AI 画的图可能出现"拓扑正确但布局难看"的问题，需要手动调整布局参数。
* **Q: AI 帮"查文档 / 学新框架" 怎么用？**
  A: 最佳实践是"AI 做学习和概念理解的加速器"。学习新框架的典型工作流：先让 AI 生成框架的"核心概念地图"（"用 200 字解释 React Server Components 是什么，和 Client Components 的区别"）。再让 AI 提供"最小可用示例"（"给我一个 Next.js App Router 的完整项目骨架，包含布局、路由、API handler"）。然后需要深入时，让 AI 解释关键机制（"Next.js 的 fetch 缓存是怎么工作的？什么时候用 force-dynamic？"）。关键技巧：给 AI 指定"角色"——"你是一个有 10 年经验的 React 导师，用通俗的比喻解释 Suspense"。不要只问"给我代码"，要追问"为什么这样设计"——AI 可以解释框架的设计权衡，这是官方文档欠缺的。注意时效性——AI 的知识有截止时间，新版本的变化可能不知道，需要加上"基于 v14 或 v15"的限定。
* **Q: AI 帮"看性能 profile / 看 source map" 靠谱吗？**
  A: 看 Source Map（错误堆栈）：AI 很擅长——给它 Source Map 和压缩后的错误堆栈，它能还原出原始代码位置和导致错误的上下文。这是 AI 的"模式匹配"能力的典型应用。看性能 Profile：有限可靠——AI 可以解释火焰图/CPU Profile 中的热点（"这个函数占用了 40% 的 CPU，因为它在循环中做了 DOM 操作"），但对复杂性能问题的根因分析（内存泄漏、渲染抖动、并发竞争）效果有限。原因：性能问题需要运行时上下文和框架底层知识，AI 缺乏对代码实际运行的观察。推荐做法：把 profile 的关键数据（耗时 Top 10 函数、内存增长曲线）贴给 AI 做初步分析，然后人工验证和深度排查。AI 的结论可以是"假设"，需要人工确认。
* **Q: AI 工具的 cost 怎么控制？**
  A: AI 开发工具（Claude Code/Cursor/Copilot）的费用是按席位订阅的，控制成本的关键是"让每个席位的价值最大化"。策略一：按需分配席位——不是每个开发都需要 Pro 版，轻度用户用免费版即可。策略二：选择模型——Cline/Continue 等开源工具可以接入自有模型（通过 Ollama/vLLM），本地模型推理成本固定（电费 + GPU 折旧），高频场景（补全）用本地小模型划算。策略三：控制 API 调用量——如果使用 Claude Code 等按 token 付费的工具，合理规划 prompt 长度（默认带所有相关文件上下文可能很浪费），限制 Agent 迭代次数。策略四：团队级订阅 vs 个人买单——企业订阅通常有折扣和统一管理。注意隐形成本：AI 生成代码的 review 时间和后续维护成本（低质量 AI 代码比不写更贵）。
* **Q: AI 工具的"安全 / 数据合规"风险？**
  A: 安全风险分三层。一是代码泄露——Copilot/Claude Code 将代码片段发送到云端推理，可能包含敏感逻辑和密钥。缓解方案：开启企业版的"数据不用于训练"选项；使用本地模型方案；在 prompt 中去除敏感信息。二是 Prompt 注入——攻击者通过在代码注释或第三方库中植入恶意 Prompt 来操控 AI 工具的行为。缓解方案：限制 AI 工具的执行权限（不要给文件系统的写权限）；敏感操作需要人类确认。三是供应链安全——AI 生成的代码可能建议使用存在安全漏洞的依赖版本或包含不安全的代码模式。缓解方案：AI 生成的依赖推荐需要人工审查版本号和安全记录。合规方面：核心问题是训练数据中是否包含受版权保护的代码（GitHub Copilot 的版权诉讼是典型案例）。企业需要制定 AI 使用政策——哪些数据可以发送给 AI 服务，哪些不可以（如客户个人信息、商业机密）。
* **Q: AI 工具帮做技术调研 / 写技术分享的工作流？**
  A: 一个高效的技术调研工作流。第一步——收集信息：把调研主题和相关线索发给 AI + Perplexity 搜索（"搜索 + 总结"模式），获得多个来源的概述。第二步——深度对比：让 AI 对比不同方案的优缺点（"对比 WebSocket 和 SSE 在实时推送场景下的优劣"），要求给出使用案例和 benchmark。第三步——生成 demo：让 AI 为每个方案写最小 demo 代码，你在本地验证，这是检验 AI 结论是否可靠的最直接方式。第四步——整理成文：把调研过程和结论发给 AI，要求生成技术文档/博客的初稿，包括背景、方案对比、选型理由、Demo 链接。关键原则：AI 给出结论后必须验证（查官方文档、跑 demo），不要盲信 AI 的调研结论。AI 可能遗漏重要信息源或给出过时的结论。
* **Q: 怎么用 AI 帮你"晋升 / 写自评"？**
  A: AI 在写自评/绩效材料上的作用主要是"组织和润色"。做法：把一年的工作成果以"流水账"的形式发给 AI（时间线 + 做了什么 + 结果），让 AI 把这些提炼成"STAR 格式"的结构化自评（情境、任务、行动、结果）。AI 擅长：把零散的工作记录变成有逻辑的叙述（"从碎片到连贯"）；提炼关键数据（"你参与了 5 个项目，其中 X 项目的性能优化使页面加载时间降低 40%"）；适配公司职级要求（"针对 P6 晋升 P7 的标准，突出你在技术方案设计和跨团队协作方面的贡献"）。注意事项：不要过度夸大事实（AI 倾向于把小事说大）；AI 生成的"成就"必须你自己确认每一条真实可信；最终文案必须符合公司文化和你的个人风格。建议先让 AI 做"挖掘"——"根据我提供的材料，列出我今年最有价值的 5 个贡献"。
* **Q: 长期看，AI 对前端工程师意味着什么？**
  A: AI 不会取代前端工程师，但会重塑这个角色。方向一：从"写代码"转向"设计和审查"——AI 负责实现（写组件、写样式、写 API 调用），前端工程师负责架构设计、交互设计、代码 review、质量把关。AI 把"写代码"的门槛降低，但"设计好系统"的能力更重要。方向二：前端工程师的边界扩展——借助 AI，前端可以做更多"原来属于后端/全栈"的工作（编写 API、数据建模、运维脚本），需要学会 AI 辅助下的全栈开发。方向三：AI 原生交互设计——前端的新战场是"AI 交互设计"（流式渲染、状态管理、AI UI 组件），这些是传统后端无法替代的。最终结论：适应 AI 工具的前端会存活并更有价值（一人能做的事变多了），拒绝 AI 的前端会被淘汰。核心竞争力从"编码速度"转变为"系统设计 + AI 协作 + 产品思维"。
* **Q: 怎么用 AI 复盘一周 / 一月的 commit？**
  A: 用 AI 复盘 commit 日志做工作总结。做法：`git log --since="1 week ago" --format="%h %s"` 获取一周的 commit 列表，发给 AI 要求"根据这些 commit message 生成周报，按功能模块分类，标注每个模块的工作量和影响"。AI 还能做更深入的复盘：分析 commit 分布（哪几天提交多、什么时间段效率高）；识别代码改动模式（重构多还是新功能多）；发现潜在问题（同一个文件被反复修改可能意味着设计不合理）。进阶做法：把 commit diff（`git diff --stat`）也发给 AI，让 AI 评估每个改动的规模和性质（"这个 commit 修改了 300 行，主要是重构了 XX 模块的 API 调用方式"）。注意：commit message 写得越清晰，AI 的复盘质量越高。如果团队 commit message 质量差，先让 AI 把 raw diff 总结成描述再复盘。
* **Q: AI 帮处理 Excel / CSV / JSON 数据怎么用？**
  A: AI 非常擅长"非结构化到结构化"的数据处理。典型场景：给 AI 一段 CSV 文本，让它做数据清洗（去重、格式标准化、缺失值处理）并输出规范结果；给一段非结构化的日志文本，让它提取关键字段输出为 JSON。做法：直接把数据样本（前 20 行）发给 AI，让它理解格式和内容，然后要求它写一个 Python/Node.js 脚本做完整处理。对于大数据量（>10000 行），不要让 AI 直接在对话中处理，让它生成处理脚本。进阶用法：让 AI 做数据分析和可视化——"这个 CSV 包含用户行为数据，分析用户留存率并生成 Matplotlib 代码"。安全性注意：Excel/CSV 可能包含敏感数据（PII），在使用 AI 处理前要脱敏或确认工具的数据安全策略。本地优先用 Ollama 做数据处理更安全。
* **Q: AI 帮做产品 / 设计 brainstorm？**
  A: AI 在产品 brainstorm 中的角色是"激发灵感的协作者"，不是决策者。有效方法：给 AI 一个"设计约束空间"——"我们做一个 AI 编程助手，目标用户是初级前端工程师，他们最痛的点是什么？列出 10 个可能的 feature，每个用一两句话说明"。AI 可以生成大量 idea（质量参差不齐，但数量能激发思考），然后人的工作是筛选、合并、判断可行性。进阶用法：让 AI 扮演不同的"persona"来评估你的 idea——"以一个 5 年经验的前端工程师角度评价这个功能"、"以一个产品经理角度分析这个功能的市场价值"。注意：AI 的 brainstorm 结果总有"平庸的倾向"（提出主流但无创新的方案），需要人类补充"打破常规"的思考。最好的方式是"AI 做发散 -> 人类做聚焦 -> AI 做细化 -> 人类做决策"的循环。
* **Q: AI 帮写周报 / 月报 / 述职报告？**
  A: AI 写汇报材料的核心价值是把零散的信息整理成结构化的叙述。做法：把一周的工作内容以"流水账"形式发给 AI（时间、做了什么、遇到的问题、结果），让它按照"目标 -> 进展 -> 结果 -> 下一步"的结构组织成周报。对于月报/述职，需要更多上下文——项目目标、与其他团队的关系、业务影响数据。AI 擅长：提炼关键数据（"本周完成了 3 个需求，修复了 5 个 bug，代码 Review 8 次"）；优化表达（"让进展描述更突出价值和成果而非苦劳"）；适配不同的受众（给主管看的 vs 给团队看的 vs 给跨部门看的）。注意事项：不要直接把 AI 生成的报告原封不动提交——加入个人的反思和判断（"我认为这个项目的风险在于..."），AI 无法替代人的思考和观点。AI 生成的是"草稿"，你添加的是"灵魂"。
* **Q: AI 提效的"反模式"有哪些？**
  A: 常见 AI 提效反模式：一是"不加 prompt 直接开干"——给 AI 模糊的指令然后反复修改，比直接写还慢。正确做法是第一次 prompt 就给出清晰的上下文和输出要求。二是"AI 写的每段代码都不审查"——导致 bug 累积，debug 时间远超重写。三是"让 AI 做它不擅长的事"——让 AI 做复杂的数学计算、最新框架的精确语法、需要深度业务理解的设计决策。四是"一味追求用最强的模型"——简单任务（如补全、分类）用 GPT-4o 完全是浪费，GPT-4o-mini/Claude Haiku 又快又便宜。五是"一次给 AI 超长上下文"——提示越长，AI 注意力越分散，效果反而下降。六是"过度依赖 AI 补全"——写几行就等 AI 补全，打断自己的思路和编码流。最好的方式是"人写逻辑框架，AI 填充实现细节"。
* **Q: AI 帮你"学新框架 / 新工具"的最快路径？**
  A: 最快学习路径是"AI 引导 + 动手实践"的循环。步骤一——概念地图：让 AI 用"对比和类比"解释新框架的核心概念（"React Server Components 可以理解为'只在服务端运行的 React 组件'，和传统的 CSR 组件的核心区别是..."）。步骤二——最小项目：让 AI 生成一个完整的最小项目模板，你亲自运行起来，这是学框架最关键的一步。步骤三——边改边学：在项目中遇到具体问题时，让 AI 解释（"这个 useEffect 为什么会有无限循环？"），而不是直接让 AI 修复。步骤四——输出倒逼输入：用 AI 帮你设计一个"用新框架做 XX 项目"的学习计划，然后自己实施。关键：不要让 AI 代你写所有代码——你写的代码才是学会的代码。AI 的最佳角色是"随时可问的导师"而非"代写工具"。推荐结合 Perplexity 查官方文档 + Claude/ChatGPT 做概念解释 + 自己动手写代码。
* **Q: AI 帮你做技术博客 / 知识沉淀？**
  A: AI 写技术博客的正确姿势：AI 做"草稿"和"结构化"，人类补充"深度"和"个性"。工作流：第一步——提供核心观点和素材："我最近做的一个性能优化项目，把页面加载时间从 3s 降到了 0.8s，主要用了代码分割、图片优化、CDN 预热，帮我整理成一篇技术博客"。第二步——让 AI 生成大纲和初稿，包含背景、问题分析、方案对比、实施细节、效果数据。第三步——人类 review：补充只有你知道的"细节和坑"（AI 写不到的具体实现细节、遇到的独特问题和解决方案）。第四步——AI 润色：优化表达、补充代码块的注释、统一术语。知识沉淀的另一个场景是"团队文档生成"——把会议录音/笔记发给 AI，让它生成会议纪要和行动项。注意：AI 生成的博客缺少"个人风格"，需要在二稿中加入你自己说话的语调。AI 适合做 70% 的骨架工作，30% 的灵魂部分必须你自己写。
* **Q: AI 帮你做 OKR / 目标拆解？**
  A: AI 在 OKR（目标与关键结果）制定中作为"结构化思考助手"。做法：给 AI 描述你的年度目标（"我想在 Q3 提升前端团队的工程效率"），AI 可以生成 OKR 建议——Objective 草案（"建立高效的前端工程化体系"）+ 多个 KR 建议（"CI 构建时间降低 40%"，"AI 工具使用率提升到 80%"等）。AI 的能力：确保 KR 是可量化的（它知道"提升效率"不可测量但"构建时间降低 40%"可测量）；对标行业标准（知道合理的 benchmark）；将大目标拆解成季度/月度可执行的 increment。注意事项：AI 不知道你的组织战略和资源约束，它生成的 OKR 是"理论上合理的 OKR"，实际可行性需要人来判断。最终 OKR 必须经过团队讨论和上级对齐。AI 的角色是"秘书"——帮你写出初稿提高效率，而不是"战略官"——决定目标方向。
* **Q: 怎么用 AI 提升英文 / 跨国协作？**
  A: AI 在英文能力提升上有三个实用场景。一是"写作助手"——写英文邮件/Slack/文档时，先用你的英文写初稿，让 AI 优化语法、用词和语气。核心 prompt："这是一个写给美国客户 CTO 的邮件，请保持正式但友好的语气，优化表达但不改变原意"。二是"阅读加速器"——让 AI 总结长篇英文文章、技术文档、RFC，"用中文总结这篇英文文章的核心观点，列出关键数据"。三是"口语练习"——用语音输入 + AI 对话练习英文。ChatGPT App 的语音对话模式适合这个场景。跨国协作中，AI 可以解决的问题：跨时区会议纪要自动生成和翻译（把英文会议录音转中文摘要）、英文 PR 描述优化、非英文母语成员的代码 review 评论润色。注意：AI 翻译的英文可能过于"完美"而显得不自然（母语者不会这样表达），需要调整到"专业但自然"的尺度。最终目标是"AI 辅助你提升英文"而非"AI 替代你使用英文"。
* **Q: 用 AI 学竞品 / 做技术调研的工作流？**
  A: 竞品分析的工作流分四步。第一步——信息爬取：用 AI（Perplexity/Google AI Overview）搜索竞品的公开信息（产品功能、定价、技术博客、客户评价）。第二步——功能矩阵：把收集的信息发给 Claude/ChatGPT，要求"生成一个竞品对比表，按功能维度（API 能力、定价、部署方式、安全性）横向对比"。第三步——深度分析：让 AI 分析竞品的技术方案（"根据竞品的公开文档，推测它的 RAG 方案是怎么实现的"），注意这里 AI 的推测不一定准确。第四步——差异化定位：基于对比结果，让 AI 建议你产品的差异化方向（"竞品在 X 方面很强，但我们可以在 Y 方面做差异化"）。效率关键是：提供具体的竞品信息源链接而非让 AI "自己搜索"（AI 的搜索能力不如 Perplexity 专注）。推荐组合：Perplexity + Claude/ChatGPT 分析 + 自己验证关键结论。最终结论要回答"别人做了什么，我们怎么做才能更好"。
* **Q: Claude Code 的架构是什么样的？**
  A: Claude Code 的核心架构是 Agent loop 驱动的 CLI 工具，运行在用户的终端中。架构分层：感知层——读取文件系统（文件内容、目录结构、git 状态、lint 错误）、用户指令（自然语言命令或 slash 命令）；推理层——通过 Anthropic API 调用 Claude 模型，核心是 Agent loop（Observe-Think-Act），模型决定下一步行动（读文件、改代码、执行命令）；执行层——工具调用（文件读写、bash 执行、git 操作、搜索替换），每个工具都有安全沙箱和权限控制。治理层——规则系统（CLAUDE.md 中定义项目规范）、权限配置、日志审计。Claude Code 的 Agent 循环实现了 ReAct 模式：模型观察当前状态 -> 思考需要做什么 -> 调用工具 -> 观察工具结果 -> 继续直到任务完成。关键特点：感知层包含"完整的项目上下文"（文件树、git diff、lint 错误），使 Agent 能做出上下文感知的决策。
* **Q: Claude Code 的"治理"具体怎么做？**
  A: Claude Code 的治理体系通过多层级规则约束 Agent 行为。第一层——CLAUDE.md 项目规则：项目根目录的 CLAUDE.md 定义了核心约束（技术栈、代码风格、安全规则、测试要求），Agent 每次启动时加载。第二层——工具权限控制：Claude Code 区分"推荐操作"和"危险操作"，危险操作（删除文件、修改 git 历史、安装依赖）需要用户确认。权限级别：自动执行（读文件、搜索）、推荐确认（写文件、git commit）、强制确认（删除文件、运行高危命令）。第三层——对话级别的 Approval：用户可以在关键操作点（写入文件、运行命令）设置"是否需要人类确认"。第四层——审计日志：每步操作记录到 ~/.claude/logs，可回溯排查。治理的平衡点：规则太松容易出事故，太严频繁打断用户导致体验差。推荐的设置是"读操作全自动，写操作需审批，危险操作双重确认"。
* **Q: 什么是 Spec-Driven Development（SDD）？为什么 AI 时代需要它？**
  A: Spec-Driven Development 是"先写规范再写代码"的开发方法论。传统做法：先做架构设计/API 设计/接口定义，再写实现。AI 时代 SDD 重新重要，核心原因：AI 生成代码的速度极快，但方向容易偏。没有明确的 spec，AI 可能在"实现一个和需求相似但不完全正确的东西"上浪费大量 token 和时间。SDD 给 AI 提供了"什么是正确的"的明确标准——AI 先理解 spec，再生成与之匹配的实现。流程：Human 写 spec（定义输入输出、约束条件、接口签名）-> AI 根据 spec 生成实现 -> AI 根据 spec 生成测试 -> 测试验证实现是否符合 spec。SDD 在 AI 时代的优势：大幅减少"AI 方向走偏"的迭代次数；spec 可以作为 prompt context 让 AI 理解全局；测试自动验证 AI 输出的正确性。OpenSpec 是这个方法论的一个具体工具实现。
* **Q: OpenSpec 是什么？解决了什么问题？**
  A: OpenSpec 是一个开源规范框架，为 AI 编程提供结构化的"需求 -> 设计 -> 任务"转化工具。解决的问题：AI 编程中最大的成本不是"写代码"而是"方向错了重写"。OpenSpec 通过分层规范管理来降低这个成本。核心解决的问题有三个：一是"需求理解偏差"——proposal 阶段让人类和 AI 对齐需求理解；二是"设计决策缺失"——design 阶段明确技术方案和权衡，不给 AI 自由发挥的空间；三是"任务拆解模糊"——tasks 阶段把设计拆成可执行的、AI 可以独立完成的子任务。OpenSpec 还通过 specs/changes 双文件夹模型实现了"规范即文档"——规范本身就是项目的活文档，不再需要额外的 wiki 或 Notion。OpenSpec 不是锁死流程的教条，而是一组可裁剪的实践，团队可以根据项目复杂度选择使用完整三件套或仅使用 spec 中的某一部分。
* **Q: OpenSpec 的核心三件套：proposal / design / tasks 各写什么？**
  A: Proposal（提议）：回答"为什么要做"和"做什么"。包含背景、目标、范围、非功能性需求、验收标准。Proposal 是需求文档的简洁版本，由产品或业务方主导，确保 AI 理解需求背景。Design（设计）：回答"怎么做"。包含技术方案、架构图（Mermaid）、数据模型、接口定义、实现策略、关键决策（ADR）。Design 是技术设计文档，由技术负责人主导，确保 AI 在正确的约束下实现。Tasks（任务）：回答"按什么顺序做"。把 Design 拆成可执行的任务列表，每个任务有明确的输入条件、输出产物、测试要求。Tasks 是 AI 的"执行清单"，AI Agent 可以按顺序独立完成每个任务。三件套形成"需求 -> 设计 -> 执行"的转化链，确保每一层的信息传递不失真。Proposal 没对齐 -> Design 就会偏 -> Tasks 就会错 -> AI 写出的代码就不对。
* **Q: OpenSpec 的双文件夹模型（specs vs changes）是什么意思？**
  A: specs 和 changes 是 OpenSpec 的双层规范存储结构。specs/：存放"已完成的设计决策"——稳定的、被团队共识确认过的规范。一旦一个 spec 被合并到 specs/，它就成了项目的"宪法"，AI 和开发者都应遵循。changes/：存放"正在进行的提案"——还在讨论中的修改提议，可能被接受也可能被拒绝。changes/ 中的每个 change 就是一次完整的 proposal + design + tasks 变更。工作流：开发者在 changes/ 中创建 change -> 讨论和迭代 -> 对齐后合并到 specs/ -> AI 根据 specs/ 中的规范生成代码。这种分离解决了"文档过时"的问题：specs/ 始终是当前项目的权威文档，changes/ 是正在进行的工作。AI Agent 在编码时参考 specs/ 确保方向正确。变化点：merge 到 specs/ 时不仅仅是文件操作，而是"设计决策的固化"——表示团队正式接受了这个设计。
* **Q: Superpowers 是什么？提供了哪些核心能力？**
  A: Superpowers 是一个 Claude Code 的规则集/提示集合（可在 GitHub 上获取），目标是显著提升 Claude Code 在复杂软件开发任务中的能力。它本质上是一组精心设计的 CLAUDE.md 配置和自动化规则，不是独立的工具。核心能力包括：角色定义——让 Claude Code 以"资深架构师"的角色思考；结构化输出——规范代码生成的格式和质量标准；安全护栏——防止 AI 做出危险操作（随意修改配置、删除文件）；工作流自动化——自动化的代码 review、测试生成和文档更新。Superpowers 的哲学是"给 AI 装上脚手架"——不在限制 AI 的能力，而是引导它的能力走向正确的方向。它和其他开源 Claude Code 规则集的本质区别：更系统的结构化设计，覆盖了从需求理解到代码审查的完整开发周期。使用 Superpowers 需要和 OpenSpec 配合——Superpowers 提供"怎么做"的方法论，OpenSpec 提供"做什么"的规范。
* **Q: Claude Code + OpenSpec + Superpowers 三件套是过度工程吗？**
  A: 取决于团队规模和项目复杂度。对于个人项目或 2-3 人的小团队，三件套可能是"过度工程"——OpenSpec 的 proposal-design-tasks 流程增加了前期文档工作，小项目直接让 Claude Code 开干更快。对于中型团队（5-15 人）或企业项目，三件套的价值很明显：减少了 AI 方向错误导致的返工成本；specs/ 作为团队共识的"单一事实源"减少了沟通成本；Superpowers 的规则集确保了 AI 输出的可预测性。选型建议：个人项目只用 Claude Code；2-5 人加 Superpowers 规则集；5 人以上再加 OpenSpec。核心判断标准是"AI 方向错误的代价"——如果一次错误的代码生成导致后续多个依赖方需要返工，那么三件套的投资是值得的。从实践来看，"渐进式采用"是合理路径——先从 Superpowers 开始，用到 OpenSpec。
* **Q: OpenSpec 的常见踩坑有哪些？**
  A: 实践中最常见的五个坑。一是"spec 写得太粗"——proposal 只有一两句话，AI 无法理解真实需求。spec 应该足够详细到 AI 生成的代码能直接通过 review。二是"spec 写完不更新"——代码实现过程中发现设计不合理，但 spec 不更新，导致 spec 和代码脱节（spec 变成了死文档）。三是"每个人都按自己的方式写 spec"——没有统一的 spec 模板，导致风格各异、质量不可控。四是"把 OpenSpec 当成项目管理工具"——OpenSpec 是"设计决策记录"而非"任务跟踪系统"，不要用它替代 Jira/Linear。五是"AI 生成的代码不符合 spec 时责怪 OpenSpec"——实际的根因通常是 spec 不够清晰或 tasks 拆解得不够细。好的 OpenSpec 实践来自迭代——第一次的 spec 可能只有 60 分，通过 review 和使用经验逐步优化到 90 分，而不是追求一次完美。
* **Q: "你日常怎么用 AI 提效"被问到，怎么答得让人记住？**
  A: 不要只回答"我用 AI 写代码"，而要展示你系统性的 AI 提效方法论。让人记住的答案结构：先说"我的核心理念"——"AI 提效的核心不是让 AI 代替我工作，而是让 AI 处理重复劳动，让我集中精力做更有创造性的决策"。然后按场景分三类：第一类"机械化工作全自动"——测试生成、文档编写、commit message、翻译，AI 完成度 90%+。第二类"创造性工作人机协作"——架构设计、代码实现、Bug 修复，AI 做初稿和方案探索，我做决策和审查。第三类"学习加速"——用 AI 做"即时导师"学新框架、读源码。最后给一个具体的效率数据——"自从系统化使用 AI 提效后，我的编码效率提升了约 2-3 倍，但代码质量 review 时间增加了 30%，总体交付速度提升约 60%"。这个回答展示了思考深度和量化意识。
### 场景设计题

* **Q: 场景题：公司想做一个"内部知识库问答机器人"，让你设计技术方案。**
  A: 技术方案分数据层、检索层、生成层、交互层。数据层——知识库文档统一存储在文档平台（飞书/Confluence/Notion），通过 API 或定时同步拉到系统。文档解析：PDF/Word/Markdown 分别用对应的解析器（Unstructured/PyMuPDF），按语义切片（500-1000 tokens，overlap 15%）。向量化：用 text-embedding-3-small 或 multilingual-e5-large 生成 embedding 存入 Qdrant（自托管）或 pgvector。检索层——Hybrid Search：BM25（关键词匹配）+ 向量检索（语义匹配），RRF 融合排序。加 Reranker（Cohere rerank 或 BGE-reranker）提升 Top-K 精度。权限过滤：用户只能检索自己有权限的文档（在检索阶段加 filter，document_id IN user_perm_docs）。生成层——LLM 根据检索结果 + 用户问题生成回答。关键：System Prompt 要求"严格基于提供的内容回答，不要添加知识库外的信息"，如果检索结果不相关（reranker 分数低于阈值）则回答"未找到相关信息"并建议提问方式。交互层——Web 界面，支持流式输出、追问、反馈按钮。数据隔离——每个公司/团队的数据不能互相访问。扩展性——未来支持多轮对话的 History-Aware 检索，以及 Agent 化的复杂问题分解（多步检索）。
* **Q: 场景题：让你做一个"代码评审 Agent"，怎么设计？**
  A: 核心设计：PR 触发 -> 并行评审 -> 结果汇总 -> 评论提交。触发阶段：监听 GitHub/GitLab Webhook（PR opened/synchronized），拉取 diff 和变更文件列表。评审阶段：并行运行多个评审 Agent，每个 Agent 负责一个维度——安全 Agent（检查密钥泄露、SQL 注入、XSS、权限漏洞）、质量 Agent（代码规范、类型安全、错误处理、测试覆盖）、性能 Agent（不必要的 re-render、大对象、O(n^2) 循环、内存泄漏风险）、架构 Agent（耦合度、过度设计、模式一致性）。每个 Agent 接收 diff + 相关文件的上下文（import 的函数/类型定义），输出评审意见（严重级别 + 问题描述 + 修复建议）。汇总阶段：主 Agent 汇总所有评审意见，去重（多个维度可能报同样问题），按严重级别排序（blocker/critical/warning/suggestion），生成结构化的 PR Review 评论。最佳实践：AI Review 作为"第一道关卡"——自动标记潜在的 blocker 问题，人工 reviewer 关注 AI 标记的 critical 问题和业务逻辑正确性。CI 集成：设置"AI Review Pass"作为合并的 check 之一。
* **Q: 场景题：公司 ToB 客户要私有化 LLM，从硬件到部署你怎么选？**
  A: 选型四步法。第一步——需求评估：客户需要什么模型能力？是简单分类对话（7B 够用）还是复杂推理（70B+ 必需）？并发量多少？延迟要求？数据是否需要隔离？第二步——硬件选型：推理场景 7B 模型推荐 1x RTX 4090 24G（性价比最高）或 L40S 48G；70B 模型最少 4x A100 80G 或 2x H100。训练/微调场景单卡 24G 可做 QLoRA（7B），多卡 A100 可做全参。国产可选昇腾 910B。第三步——推理框架：vLLM（吞吐高，连续批处理，支持量化，推荐优先考虑）或 Ollama（部署简单，但吞吐差）。框架选型后考虑量化——INT8 显存减半精度微损，AWQ INT4 压缩更大。第四步——部署架构：单机 Docker Compose（小规模原型）、Kubernetes + KubeRay（生产级，支持自动扩缩容 GPU）、裸金属（极致性能）。客户现场部署要满足网络隔离和数据不出域的要求，通常通过反向代理（Nginx）暴露 API。运维需要监控 GPU 利用率、OOM、推理延迟和错误率。
* **Q: 场景题：让你优化一个"AI 回答平均要 30 秒"的产品，怎么排查？**
  A: 系统化排查链路。第一步——拆解延迟构成（Trace）：TTFT（首 token 时间）+ TPOT（每个 token 生成时间）* token 数 + 前后处理时间。30 秒中，可能是模型推理慢（TTFT 5s + TPOT 100ms * 200 tokens = 25s），也可能是前后处理（RAG 检索、Tool Calling）耗时。第二步——分析 TTFT 过高：如果是 Prompt 太长（超长 System Prompt + 大量历史消息），检查是否有不必要的上下文内容，实施 Prompt 压缩和缩短。如果是 GPU 推理慢，检查是否 batch size 太小、量化级别不够、或模型太大（70B 用单卡推理本来就慢）。第三步——分析 TPOT 过高：检查是否使用流式输出（显著改善首屏体验），检查 vLLM 的 continuous batching 是否充分利用 GPU，检查 KV Cache 是否命中。第四步——端到端优化：前端做乐观更新（立即显示消息）；RAG 检索做异步并行（相关文档向量检索和关键词检索并行）；Tool Calling 做超时控制；模型切换（简单场景用小模型 1-3s，复杂场景才用大模型）。目标：TTFT < 1s，总响应 < 5s。
* **Q: 场景题：做一个"AI 客服"，怎么保证不乱说话？**
  A: 多层防御策略。第一层——知识库约束：AI 客服必须是检索增强的，不能依赖模型内部知识。System Prompt 明确"只基于提供的知识库回答问题，知识库里没有的信息回答'抱歉我不了解这个问题'"。RAG 的 reranker 设低阈值——检索结果相关性低时直接拒答。第二层——输入过滤：敏感词检测（用户试图诱导 AI 说违规内容），Prompt 注入检测（识别"忽略之前的指令"类攻击）。第三层——输出过滤：生成的内容经过内容安全检测（NSFW、政治敏感、PII 泄露），使用 LLM-as-Judge 或专门的分类模型做实时审核。第四层——行为限制：配置 Tool Calling 的白名单（只能调用知识库查询工具，不能调用写操作工具）；限制 Agent Loop 的最大步数。第五层——人工兜底：识别到模型置信度低或用户情绪激动时转人工；人工客服可以查看 AI 的完整推理日志。第六层——灰度 + 监控：新版本的 System Prompt 先在 5% 流量上验证；监控异常回复率和用户投诉率。客服场景中"过度拒答"比"乱说"更安全——宁可说不知道，不能乱承诺。
* **Q: 场景题：把 ChatGPT 类的对话产品迁移到你们的国产替代方案，应该注意什么？**
  A: 迁移到国产模型（DeepSeek、通义千问、Kimi、GLM）的核心注意点。一是能力差异评估——国产模型在复杂推理（数学、代码）上与 GPT-4/Claude 仍有差距，需要在迁移前用你的业务数据集做 benchmark 测试。关键看：语义理解准确率、指令跟随能力、输出格式一致性（JSON 输出是否稳定）。二是 Token 化差异——不同模型 tokenizer 不同，中文字符的 token 消耗差异大（有些国产模型的中文 token 效率高），影响成本估算。三是 Tool Calling / Function Calling 兼容性——国产模型的工具调用能力参差不齐，JSON Mode 稳定性不如 GPT，需要增加 retry 和后处理逻辑。四是流式输出格式——迁移 SSE 协议兼容层（OpenAI 格式 vs 国产模型自定义格式）。五是 Prompt 迁移——同一个 Prompt 在 GPT 上效果好但在国产模型上可能差，需要重新调优（国产模型通常需要更明确的格式约束和中英文术语对齐）。六是数据合规——国产模型的部署和数据存储是否满足行业监管要求。建议策略：从非关键功能开始迁移，用 AI Gateway 做统一 API 适配层，实现灰度切换。
* **Q: 场景题：用户对 AI 输出不满意怎么办？**
  A: 这是一个"体验闭环"设计问题。解决方案分四层。第一层——反馈收集：每条 AI 回复后展示赞/踩按钮，引导用户反馈。踩的时候让用户选择原因（"答案不准确"、"太啰嗦"、"没有帮助"、"有其他问题"），这为后续优化提供方向。第二层——实时修正：用户不满意时提供"重新生成"和"修改问题"选项。重新生成用新的随机 seed 获得不同的回复。第三层——降级策略：如果用户连续 2 次点踩，自动切换到更保守的模式（降低 temperature、减少创造性、更严格的 RAG 约束），或提示"是否需要转人工"。第四层——离线优化：收集用户不满意的样本（用户反馈 + 具体的 AI 回复），定期做评估和优化。建立"不满意数据集"，用 LLM-as-Judge 批量评估新 Prompt 版本的效果。关键点：向用户展示"AI 正在改进"的信号——"感谢反馈，这条回复已标记给团队优化"。好的反馈机制本身就能提升用户满意度（即使 AI 回复不够好，用户感受到被倾听）。
* **Q: 场景题：模型出现"复读机"现象怎么处理？**
  A: "复读机"现象（模型不断重复相同的短语或句子）的根因：一是概率陷阱——模型在生成的 token 序列中陷入局部概率循环，当前 token 的最优预测导致重复。二是上下文污染——历史消息中重复的模式诱导模型继续重复。三是温度太低（temperature=0 时贪心采样容易陷入循环）。处理方案：即时层面——调整 generation 参数：适当提高 temperature（0.3-0.7）、设置 frequency_penalty（0.3-0.5）和 presence_penalty（0.3-0.5）减少重复。加 stop sequences——在 prompt 中设置"如果检测到重复超过 3 次就停止"。代码层面——前端检测重复模式（连续 3 个相同句子时自动中断并提示"回复异常，请重试"）。长期预防——检查 System Prompt 是否包含可能导致重复的指令（如"请详细解释"在无边界时可能导致无限展开）；检查 RAG context 是否有重复的文档片段。模型层面——如果特定模型频繁复读，考虑换模型或升级版本。严重情况下，设置最大生成长度并监测"重复率"指标。
* **Q: 场景题：怎么做"AI 应用的灾备 / 降级"？**
  A: AI 应用的灾备策略分模型层、业务层、体验层。模型层——多模型兜底：主模型不可用时自动切换到备用模型（GPT-4o -> GPT-4o-mini -> Claude Haiku -> 国产模型）。模型 API 做 health check，连续 3 次失败触发切换。降级模式：主模型超时回退到次模型（弱但快）。业务层——缓存优先：高频问题提前准备缓存（相同的 embedding 检索结果在 TTL 内复用），缓存命中时完全不需要模型调用。异步处理：非实时场景（报告生成、批量处理）走消息队列，主模型恢复后轮询完成。体验层——优雅降级：AI 不可用时展示"AI 暂时离线，以下是人工整理的常见问题"或者"AI 正在升级，预计 10 分钟后恢复，您可以先..."。不要展示技术错误信息。离线模式：PWA 缓存常见问题的回复离线可用。灾备方案需要在架构层面设计而不是等出事了再想——建立"降级矩阵"：每个功能模块在"主模型不可用/次模型可用/完全离线"三种状态下的行为预案。
* **Q: 自我介绍：怎么把"我做过 AI 项目"讲得让面试官眼前一亮？**
  A: 结构化的"STAR + 数据 + 思考"模式。框架：做了什么（角色和场景）-> 核心挑战（技术难点）-> 你的贡献（具体做了什么）-> 结果和数据（量化收益）-> 反思（你学到了什么）。示例——"我在 XX 公司负责 AI 客服系统的前端架构。核心挑战是流式输出在低端移动设备上的渲染性能——3000 tokens 的回复在千元机上卡顿严重。我的方案是'增量渲染 + Web Worker's Markdown 解析'，把首 token 显示时间从 2.5s 降到 0.8s，帧率从 15fps 提升到 55fps。最终该项目上线后用户满意度提升 30%，日活提升 15%。这个项目让我深刻理解了 AI 应用的性能瓶颈分析方法和流式渲染的工程实践。"让人记住的关键：数据说话（不是"提升了性能"而是"从 2.5s 降到 0.8s"）、具体的技术细节（增量渲染 + Web Worker）、业务影响（日活提升 15%）。
* **Q: 场景题：让你设计一个 Cursor 同款 AI 编辑器，怎么做？**
  A: 核心架构分四层。编辑器层——基于 VS Code（开源）或 VS Code Server 做白标定制，提供编辑器核心能力（语法高亮、多语言支持、LSP 集成、Git 集成）。AI 补全层——监听编辑器变化（onDidChangeTextDocument），取光标前的上下文（200-300 tokens）+ 光标后内容 + 当前文件类型，发送给 LLM API 请求补全。补全以 ghost text 形式渲染在光标后，用户按 Tab 接受，继续输入自动取消。多模型支持（GPT-4o-mini 做快速补全，Claude 做复杂补全）。AI 对话层——侧边栏对话面板，支持"Ask"（选中代码直接提问）和"Edit"（选中代码并给出修改指令）。核心：对话上下文中包含当前文件的完整内容和选中区。Agent 模式——文件级操作（Refactor、Fix、Generate），用户给出自然语言指令，Agent 读取多个相关文件、修改代码、创建新文件。差异对比面板展示修改。补全性能关键：补全延迟必须 <500ms（超过 1s 用户就会感觉卡顿），通过流式输出 + 逐 token 渲染实现"打字机效果"，另外实现请求防抖（用户继续输入时取消上次未完成的补全请求）。
* **Q: 场景题：AI 监控告警归并系统怎么做？**
  A: 传统告警归并基于规则（相同错误类型、相同主机），LLM 可以做到"语义级别"的归并。架构设计：数据采集层——接收 Prometheus/Grafana/Sentry/ELK 等源的告警事件，统一格式化为标准告警结构（title、message、severity、source、timestamp、labels）。语义分析层——用 LLM 对每条告警做分类：根因告警 vs 衍生告警、已知问题 vs 新问题、紧急 vs 可延迟。核心是"告警指纹提取"——LLM 把告警消息提炼为"指纹"（关键特征向量），相同指纹的告警归并到同一 incident。归并策略：时间窗口归并（相同服务 5 分钟内的告警合并）+ 因果归并（A 服务的错误可能是 B 服务故障导致的，B 的是根因）+ 语义归并（"连接超时"和"连接拒绝"是同一类问题）。Agent 辅助——总结归并后的告警组的根因和影响范围，给出推荐处理步骤。LLM 归并的挑战：延迟（在线归并要求秒级，LLM 调用可能慢于阈值）、准确率（误归并比不归并更糟糕——会导致关键告警被隐藏）。生产方案：规则归并做第一层（快速、确定），LLM 归并做第二层（深度分析，异步做）。
* **Q: 场景题：智能客服路由（什么时候转人工）？**
  A: 智能客服的转人工决策点设计。必须转人工的场景：用户明确要求（"转人工"、"找人工客服"）；情绪检测异常（检测到愤怒、沮丧的关键词或重复投诉）；涉及敏感操作（退款、投诉、法律相关、账号安全）；AI 连续 2 次回答未解决用户问题（用户继续追问且问题未闭环）；高风险场景（医疗建议、法律建议、金融交易）。选择性转人工的场景：AI 置信度低于阈值（RAG 检索结果相关性分数低）；对话轮次超过 N 轮（通常 10-15 轮以上说明问题复杂）；用户连续输入短句/语气词（"不行"、"还是不对"）。路由实现：AI 客服的每个回复附带一个"转人工分数"（0-1），结合规则引擎（必须转的条件走硬路由 + 分数超阈值走软路由）。工程注意：转人工要携带完整对话上下文（用户信息、问题描述、AI 已尝试的解决方案），让人工客服无缝接手。设计上"宁可早转不可晚转"——用户被长时间困在 AI 里是最糟糕的体验。
* **Q: 场景题：让 AI 把设计稿自动转代码？**
  A: 设计稿转代码是典型的多模态 AI 应用，目前准确率有限但有实用价值。技术方案：设计稿解析层——输入 Figma 设计稿（通过 Figma API 获取节点树 + 组件属性 + 样式信息）或截图（多模态模型直接识别）。关键：Figma API 的方式更可靠（能获取精确的图层层级、自动布局属性、颜色字体），截图方式适合快速原型。布局还原层——AI 识别设计稿的布局结构（Flex/Grid、间距、对齐、响应式断点），生成对应的 HTML/CSS 结构。关键难点：AI 在"设计稿中的分组"和"合理的 DOM 结构"之间映射经常出错（设计稿的分组是视觉的，不是语义的）。组件映射层——把设计稿中的 UI 组件映射到实际代码组件库（如 Ant Design、shadcn/ui）。需要维护"设计组件 -> 代码组件"的映射配置。生成层——输出完整的组件代码（TSX + CSS Modules/Tailwind），支持流式预览。局限：生成代码的可维护性较差（AI 生成的 CSS 选择器命名、组件拆分粒度不如人工设计的合理），通常定位为"从 0 到 80% 的加速器"，人工需要重构和优化。最佳场景是"设计 -> 骨架代码 -> 人工精细化"的工作流。
* **Q: 场景题：AI 应用的 SLA 怎么保证？**
  A: AI 应用的 SLA 比传统应用复杂，因为依赖的外部模型 API 本身不保证 SLA。分层保证策略：第一层——模型 API 的冗余：同时接入多家模型供应商（OpenAI + Anthropic + 国产模型），通过 AI Gateway 做故障切换。可用性目标：99.9%（主模型不可用时 3s 内切换到备用模型）。第二层——延迟 SLA：设置"降级时间线"——预测生成时间如果超过 N 秒（如 10s），自动切换到更快的模型或缓存方案。目标是 P95 响应时间 < 5s。关键工具：使用流式输出让用户感受到进度而非白屏等待。第三层——质量 SLA：LLM-as-Judge 在线评估回复质量，低于阈值触发重新生成或降级。离线用数据集跑回归测试。第四层——容量规划：预估 QPS 高峰（业务活动期），预置足够的推理单元（自部署场景）或配置 API 的 rate limit 和配额告警。可量化的 SLA 指标：可用性（API 成功率 > 99.5%）、延迟（TTFT P95 < 2s，总响应 P95 < 10s）、质量（用户满意度 > 85%）。SLA 违约需要有补偿机制（如免费调用额度）。
* **Q: 场景题：多端 AI 助手（Web + iOS + Android + 桌面）怎么统一？**
  A: 多端统一的核心是"一套 API 后端，多个客户端 SDK"。架构：统一 API 层——所有端调同一个后端 API（/api/chat），参数和消息格式统一（OpenAI 格式或标准消息协议）。后端处理完所有 AI 逻辑（RAG、Agent、工具调用），客户端只负责展示。客户端 SDK 层——每个端实现独立的 SDK，封装连接管理、流式接收、状态同步。Web 用 Vercel AI SDK / fetch SSE，iOS 用 URLSession + streaming，Android 用 OkHttp + SSE，桌面用 Tauri/Electron 的 HTTP 客户端。状态同步——关键问题是"多端同时使用同一会话时的冲突"。一般策略：最后写入者胜出（LWW），同步器设计——消息 ID 基于时间戳 + 客户端 ID 前缀，服务端按消息顺序合并。推送机制——一个端收到 AI 回复后，通过 WebSocket 推送给其他端。UI 适配——Web 端功能最全，移动端精简（语音输入优先、减少复杂操作），桌面端介于两者之间。核心原则：后端是"唯一的事实源"，客户端是"无状态的渲染层"。
* **Q: 场景题：AI 应用全链路可观测性怎么做？**
  A: 全链路可观测性覆盖"用户端 -> 后端 -> AI 模型"的完整请求路径。分层设计：用户端——收集性能指标（TTFT、总响应时间、FCP 流式首次渲染时间）、异常（流式中断、渲染错误）、行为（点赞/踩、重新生成、放弃等待）。工具：Web Vitals + 自定义埋点（PostHog/Sentry）。后端——传统可观测（API 延迟、错误率、QPS + RAG 检索延迟、向量数据库查询时间）+ AI 专用指标（上下文窗口填充率、Tool Calling 执行时间、Agent Loop 迭代次数）。工具：Langfuse/LangSmith + OpenTelemetry。模型端——模型推理指标（TTFT、TPOT、GPU 利用率、KV Cache 命中率）、模型质量指标（LLM-as-Judge 打分、一致性评估）。工具：vLLM metrics（Prometheus）+ 自定义评估服务。全链路 trace——最主要的挑战是"关联"：用户的 Web 请求 -> 后端 API -> RAG 检索 -> 向量 DB 查询 -> Tool Calling -> 模型推理 -> 流式响应返回，需要统一的 trace ID 贯穿所有环节。OpenTelemetry + Langfuse 的组合可以实现端到端 trace。关键告警项：错误率突增、TTFT 超过阈值、Agent 循环超限、GPU OOM。
* **Q: 场景题：AI 应用合规风险有哪些？怎么处理？**
  A: AI 应用合规风险分四大类。数据隐私与保护——用户对话数据含 PII（姓名、电话、地址），存储需要加密且限制访问，训练数据需要脱敏。模型使用前做数据保护影响评估（DPIA）。内容合规——生成内容需符合法规（中国《生成式 AI 服务管理暂行办法》要求生成内容不违法、不传播虚假信息、标注 AI 生成）。对策：输出端加内容安全审核（百度/阿里云的内容安全 API），敏感词过滤，生成内容加"AI 生成"标识。知识产权——模型输出的版权归属存在法律灰色地带，训练数据中是否包含受版权保护的内容。对策：使用有明确版权授权的内容训练模型；生成内容的版权通过用户协议约定。跨境数据——使用国外模型 API（OpenAI/Claude）时数据可能出境，需要遵守《数据安全法》《个人信息保护法》。对策：数据不出境使用国产模型（DeepSeek/通义千问/GLM），或签订标准合同条款（SCC）。合规处理框架：建立 AI 合规检查清单，每个 AI 功能上线前过合规评审，持续监控法规变化。
* **Q: 场景题：把团队"AI First"推进开发流程，怎么做？**
  A: AI First 不是"所有人用 AI 写代码"，而是系统性地把 AI 嵌入开发流程的每个环节。推进路线：第一步——工具层普及（1-2 周）：团队统一部署 AI 编程工具（Cursor + Claude Code + Copilot），制定使用规范（哪些场景可以用、数据安全注意事项）。第二步——流程层嵌入（1-2 月）：Code Review 中 AI 自动检查；CI 流程中接入 AI 测试生成；PR 描述和 commit message 由 AI 生成。第三步——文化层建设（3-6 月）：建立"AI 最佳实践"文档库；每周的 AI 提效分享会；把 AI 使用效果纳入 OKR（"AI 辅助后测试覆盖率提升 X%"）。关键推动手段："自上而下"（技术负责人带头示范）+"自下而上"（开发者自发分享提效经验）。避免的坑：强制所有人用统一的工具（开发者应该选自己顺手的工具）；把 AI 当"银弹"（AI 不能解决糟糕的需求和混乱的架构）；忽视安全合规（敏感代码段不能发给外部 AI）。衡量指标：开发者满意度、平均交付周期、Code Review 效率、Bug 率变化。

### 综合开放题

* **Q: 终极开放题：如果让你三年内深耕一个 AI 方向，你会选哪个？**
  A: 我会选择"AI 原生应用架构与体验设计"这个方向。原因：2024-2025 年 AI 基础设施已趋于成熟（模型能力足够了、工具链基本完善、MCP/Agent 标准逐渐形成），但"如何构建好的 AI 原生应用"这个上层问题远未解决。具体深耕点：AI 交互范式——流式 UI 的最佳实践、多模态输入输出在前端的无缝集成、AI 状态管理（loading/streaming/error 的用户体验设计）。AI 工程化——AI 应用的性能调优（TTFT 优化、流式渲染性能、移动端适配）、可靠性（降级、灾备、可观测性）。AI 产品设计——如何把 AI 能力嵌入现有产品而不破坏用户体验、Agent 的"可预测性"设计（用户知道 AI 在做什么以及为什么）。我的优势是前端全栈背景+AI 工程经验，这让我能同时理解"用户体验"和"模型能力"两个层面，做出既有技术深度又有产品感觉的 AI 应用。简单说：不做"调 API 的 AI 应用"，而做"重新定义交互的 AI 原生应用"。




