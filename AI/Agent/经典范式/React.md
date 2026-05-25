# React
## 代码实现
```js
import dotenv from 'dotenv'
import path from 'path'

// 直接使用原生提供的 dirname，效果和之前完全一样
const __dirname = import.meta.dirname

dotenv.config({ path: path.resolve(__dirname, '../../.env') })

import { LLMClient } from 'src/core/client'
import { Agent } from '../core/agent'
import {
    LLMConfig,
    LLMMessage,
    LLMRequestOptions,
    LLMResponse,
    AgentConfig,
    ToolDefinition,
} from '../core/types'

const MOCK_TOOLS: Record<string, { description: string; fn: (args: string) => string }> = {
    get_weather: {
        description: '获取指定城市的天气信息，输入城市名，返回天气状况和温度',
        fn: (city: string) => {
            const weatherMap: Record<string, string> = {
                北京: '晴，15-28°C',
                上海: '多云，20-26°C',
                广州: '雨，24-30°C',
                深圳: '晴，25-31°C',
            }
            return weatherMap[city] || '暂无该城市天气数据'
        },
    },
    search_attractions: {
        description: '搜索旅游景点，输入城市名，返回热门景点列表',
        fn: (city: string) => {
            const attractionsMap: Record<string, string> = {
                北京: '故宫、天安门、长城、颐和园、天坛',
                上海: '外滩、东方明珠、豫园、田子坊',
                广州: '广州塔、珠江新城、北京路、沙面',
            }
            return attractionsMap[city] || '暂无该城市景点数据'
        },
    },
    calculate: {
        description: '数学计算器，输入数学表达式，返回计算结果',
        fn: (expr: string) => {
            try {
                const result = eval(expr)
                return String(result)
            } catch {
                return '计算表达式有误'
            }
        },
    },
}

function formatTools(toolRegistry: Record<string, any>): string {
    const toolList = Object.entries(toolRegistry)
        .map(([name, tool]) => `- ${name}: ${tool.description}`)
        .join('\n')
    return toolList || '没有可用的工具'
}

function buildPrompt(tools: string, question: string, history: string[]): string {
    return `你是一个具备推理和行动能力的AI助手。你可以通过思考分析问题，然后调用合适的工具来获取信息，最终给出准确的答案。

## 可用工具
${tools}

## 工作流程
请严格按照以下格式进行回应，每次只能执行一个步骤:

Thought: 分析当前问题，思考需要什么信息或采取什么行动。
Action: 选择一个行动，格式必须是以下之一:
- 'tool_name[tool_input]' - 调用指定工具
- 'Finish[最终答案]' - 当你有足够信息给出最终答案时

## 重要提醒
1. 每次回应必须包含Thought和Action两部分
2. 工具调用的格式必须严格遵循:工具名[参数]
3. 只有当你确信有足够信息回答问题时，才使用Finish
4. 如果工具返回的信息不够，继续使用其他工具或相同工具的不同参数

## 当前任务
**Question:** ${question}

## 执行历史
${history.length > 0 ? history.join('\n') : '(无)'}

现在开始你的推理和行动:
`
}

// a simple react agent
export class ReactAgent extends Agent {
    toolRegistry: any
    enableToolCalling: boolean
    maxStep: number
    currentHistory: string[]
    customPrompt: string
    constructor(
        llm: LLMClient,
        name: string,
        config: AgentConfig,
        systemPropmt: string,
        toolRegistry: any,
        enableToolCalling: boolean = true,
        maxStep: number,
        customPrompt: string,
    ) {
        super(llm, name, config, systemPropmt)
        this.toolRegistry = toolRegistry
        this.enableToolCalling = enableToolCalling && toolRegistry
        this.maxStep = maxStep
        this.currentHistory = []
        this.customPrompt = customPrompt

        console.log('基础信息: ', this.getInfo())

        console.log(`ReactAgent ${name} 构建成功，最大步数${maxStep}`)
    }

    buildPrompt(toolsDesc: string, question: string, history: string[]): string {
        return buildPrompt(toolsDesc, question, history)
    }

    parseOutput(responseWithThoughtAndAction: string) {
        let thought = ''
        let action = ''

        const thoughtMatch = responseWithThoughtAndAction.match(
            /Thought:\s*([\s\S]*?)(?=\s*Action:)/,
        )
        if (thoughtMatch && thoughtMatch[1]) {
            thought = thoughtMatch[1].trim()
        }

        const actionMatch = responseWithThoughtAndAction.match(/Action:\s*([\s\S]*)/)
        if (actionMatch && actionMatch[1]) {
            action = actionMatch[1].trim()
        }

        return { thought, action }
    }

    executeTool(action: string, toolRegistry: Record<string, any>): string {
        // 匹配格式: tool_name[args]
        const match = action.match(/^(\w+)\[(.+)\]$/)
        if (!match) {
            return `无法解析工具调用: ${action}`
        }

        const toolName = match[1]
        const toolArgs = match[2]
        const tool = toolRegistry[toolName]

        if (!tool) {
            return `工具不存在: ${toolName}`
        }

        try {
            return tool.fn(toolArgs)
        } catch (e) {
            return `工具执行错误: ${e}`
        }
    }

    async run(inputText: string): Promise<string> {
        
        let currentStep = 0
        while (currentStep < this.maxStep) {
            console.log(`\n当前第${currentStep + 1}步`)

            const toolsDesc = formatTools(MOCK_TOOLS)
            const stepHistory = [...this.currentHistory]
            // console.log(stepHistory)

            const prompt = buildPrompt(toolsDesc, inputText, stepHistory)
            // console.log(prompt)

            const messages: LLMMessage[] = [{ role: 'user', content: prompt }]

            if (!this.enableToolCalling) {
                const response = await this.llm.chat({ messages })
                // console.log(response);

                const content = response.choices[0]?.message?.content || ''
                const { thought, action } = this.parseOutput(content)

                console.log(`\nThought: ${thought}`)
                console.log(`\nAction: ${action}`)

                // 处理 Action
                if (action.startsWith('Finish[')) {
                    console.log(`\n最终答案: ${action.slice(7, -1)}`)
                    console.log('\n最后一轮Prompt: ',prompt);
                    
                    return action.slice(7, -1)
                    // TODO
                    // 这里要将对话的历史添加到this._history中去，而详细的React的步骤就不用去添加了
                }

                // 执行工具
                const toolResult = this.executeTool(action, MOCK_TOOLS)
                console.log(`工具执行结果: ${toolResult}`)

                // 添加到历史
                this.currentHistory.push(
                    `\n步骤${currentStep + 1}:\nAction: ${action} \nObservation: ${toolResult}`,
                )
            }

            currentStep++
        }

        return '达到最大步数限制'
    }
}

const llm = new LLMClient({
    provider: 'deepseek',
    apiKey: process.env.DEEPSEEK_API_KEY || '',
    baseURL: 'https://api.deepseek.com',
    model: 'deepseek-chat',
})

// // console.log(process.env);

const reactAgent = new ReactAgent(
    llm,
    'ReactAgent',
    { shit: 'test' },
    '你是一个友好的AI助手，用中文回答。',
    undefined,
    false,
    5,
    '',
)

reactAgent.run('给我安排去北京上海的旅行').then(console.log)

```
## 执行结果
```text
➜  server git:(feat-agent-llm ~1) ✗ pnpm tsx src/agents/react_agent.ts
◇ injected env (7) from .env // tip: ⌘ enable debugging { debug: true }
基础信息:  
            Agent Name: ReactAgent
            Provider: deepseek

ReactAgent ReactAgent 构建成功，最大步数5
ReactAgent 正在处理: 给我安排去北京上海的旅行

当前第1步

Thought: 用户让我安排去北京上海的旅行。这需要我分别获取北京和上海的天气信息以及旅游景点信息，以 便提供合理的旅行建议。我先从查询北京的天气和景点开始。

Action: get_weather[北京]
工具执行结果: 晴，15-28°C

当前第2步

Thought: 用户希望安排去北京和上海的旅行。我需要先获取这两个城市的天气和景点信息，以便提供旅行建 议。我已经有了北京的天气（晴，15-28°C），现在需要获取上海的天气，以及两个城市的景点信息。       

Action: get_weather[上海]
工具执行结果: 多云，20-26°C

当前第3步

Thought: 我已经获取了北京和上海的天气信息。现在需要获取两地的热门景点，以便规划旅行安排。       

Action: search_attractions[北京]
工具执行结果: 故宫、天安门、长城、颐和园、天坛

当前第4步

Thought: 我已有北京和上海的天气信息，以及北京的景点信息。还需要上海的景点信息才能给出完整的旅行 安排建议。因此，我接下来需要获取上海的景点信息。

Action: search_attractions[上海]
工具执行结果: 外滩、东方明珠、豫园、田子坊

当前第5步

Thought: 我已经获取了北京和上海的天气信息以及热门景点列表。根据这些信息，我可以为用户安排一个简 单的一周旅行计划，涵盖北京和上海两个城市。北京天气晴朗，适宜户外游览；上海多云，也比较舒适。北京景点有故宫、天安门、长城等，上海有外滩、东方明珠等。我将推荐一个行程安排。

Action: Finish[### 北京-上海旅行建议

根据当前天气和景点信息，为您规划了一个7天的旅行计划：

#### 📅 行程安排

**Day 1-4：北京**
- **天气**：晴，15-28°C（适宜出行，建议带薄外套）
- **推荐景点**：
  - 故宫（历史文化）
  - 天安门广场（地标）
  - 长城（一日游，建议选八达岭）
  - 颐和园（皇家园林）
  - 天坛（祈福圣地）

**Day 5-7：上海**
- **天气**：多云，20-26°C（舒适，偶有阴天）
- **推荐景点**：
  - 外滩（夜景必看）
  - 东方明珠（登高观景）
  - 豫园（江南古典园林）
  - 田子坊（文艺小巷，适合闲逛）

#### 💡 小贴士
- 北京景点分散，建议包车或地铁+打车结合
- 长城建议早出发，避开人流
- 上海外滩晚上灯光更美
- 两地温差不大，夏装+一件薄外套即可

祝您旅途愉快！]

最终答案: ### 北京-上海旅行建议

根据当前天气和景点信息，为您规划了一个7天的旅行计划：

#### 📅 行程安排

**Day 1-4：北京**
- **天气**：晴，15-28°C（适宜出行，建议带薄外套）
- **推荐景点**：
  - 故宫（历史文化）
  - 天安门广场（地标）
  - 长城（一日游，建议选八达岭）
  - 颐和园（皇家园林）
  - 天坛（祈福圣地）

**Day 5-7：上海**
- **天气**：多云，20-26°C（舒适，偶有阴天）
- **推荐景点**：
  - 外滩（夜景必看）
  - 东方明珠（登高观景）
  - 豫园（江南古典园林）
  - 田子坊（文艺小巷，适合闲逛）

#### 💡 小贴士
- 北京景点分散，建议包车或地铁+打车结合
- 长城建议早出发，避开人流
- 上海外滩晚上灯光更美
- 两地温差不大，夏装+一件薄外套即可

祝您旅途愉快！

最后一轮Prompt:  你是一个具备推理和行动能力的AI助手。你可以通过思考分析问题，然后调用合适的工具 来获取信息，最终给出准确的答案。

## 可用工具
- get_weather: 获取指定城市的天气信息，输入城市名，返回天气状况和温度
- search_attractions: 搜索旅游景点，输入城市名，返回热门景点列表
- calculate: 数学计算器，输入数学表达式，返回计算结果

## 工作流程
请严格按照以下格式进行回应，每次只能执行一个步骤:

Thought: 分析当前问题，思考需要什么信息或采取什么行动。
Action: 选择一个行动，格式必须是以下之一:
- 'tool_name[tool_input]' - 调用指定工具
- 'Finish[最终答案]' - 当你有足够信息给出最终答案时

## 重要提醒
1. 每次回应必须包含Thought和Action两部分
2. 工具调用的格式必须严格遵循:工具名[参数]
3. 只有当你确信有足够信息回答问题时，才使用Finish
4. 如果工具返回的信息不够，继续使用其他工具或相同工具的不同参数

## 当前任务
**Question:** 给我安排去北京上海的旅行

## 执行历史

步骤1:
Action: get_weather[北京]
Observation: 晴，15-28°C

步骤2:
Action: get_weather[上海]
Observation: 多云，20-26°C

步骤3:
Action: search_attractions[北京]
Observation: 故宫、天安门、长城、颐和园、天坛

步骤4:
Action: search_attractions[上海]
Observation: 外滩、东方明珠、豫园、田子坊

现在开始你的推理和行动:

### 北京-上海旅行建议

根据当前天气和景点信息，为您规划了一个7天的旅行计划：

#### 📅 行程安排

**Day 1-4：北京**
- **天气**：晴，15-28°C（适宜出行，建议带薄外套）
- **推荐景点**：
  - 故宫（历史文化）
  - 天安门广场（地标）
  - 长城（一日游，建议选八达岭）
  - 颐和园（皇家园林）
  - 天坛（祈福圣地）

**Day 5-7：上海**
- **天气**：多云，20-26°C（舒适，偶有阴天）
- **推荐景点**：
  - 外滩（夜景必看）
  - 东方明珠（登高观景）
  - 豫园（江南古典园林）
  - 田子坊（文艺小巷，适合闲逛）

#### 💡 小贴士
- 北京景点分散，建议包车或地铁+打车结合
- 长城建议早出发，避开人流
- 上海外滩晚上灯光更美
- 两地温差不大，夏装+一件薄外套即可

祝您旅途愉快！
```