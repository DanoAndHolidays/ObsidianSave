# Button 与 Button Group

相关文档：[Button](https://ocn10zycuxwg.feishu.cn/wiki/LZ9kwfE7Ai5Ww2kEsidcB8wnnNg) [Button Group](https://ocn10zycuxwg.feishu.cn/wiki/TW6GwSzrCiG8vDk3FgGcYvw9ntf)

---
## Button
最基础且最高频使用的交互组件。飞书文档[Button](https://ocn10zycuxwg.feishu.cn/wiki/LZ9kwfE7Ai5Ww2kEsidcB8wnnNg)已经建立了完整的能力模型（核心/表现/扩展/工程四层）和 6 条设计原则

由于此组件的实现较为简单，这里直接附上源码：
```TypeScript
import { type ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

const variants = {
  default: "bg-gray-900 text-white hover:bg-gray-800",
  outline: "border border-gray-200 bg-white hover:bg-gray-50",
  ghost: "hover:bg-gray-100",
  destructive: "bg-red-600 text-white hover:bg-red-700",
};

const sizes = {
  sm: "h-8 px-3 text-xs",
  default: "h-9 px-4 text-sm",
  lg: "h-10 px-6 text-base",
};

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof variants;
  size?: keyof typeof sizes;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center rounded-md font-semibold transition-colors focus:outline-none focus:ring-1 focus:ring-offset-1 disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    />
  ),
);
Button.displayName = "Button";
```

### 模型能力

| 层级 | 职责 | 包含要素 |
|------|------|---------|
| **核心能力** | Button "做什么" | 行为触发（click/submit/reset）、原生 button 行为、disabled 状态控制 |
| **表现能力** | Button "长什么样" | variant（6 种视觉变体）、size（8 级尺寸）、内容表达（Icon/With Icon/Rounded/Spinner） |
| **扩展能力** | 不改变核心语义的使用方式扩展 | Link（asChild）、Button Group（组合能力） |
| **工程能力** | 可维护性与可扩展性 | API 命名规范（camelCase + 双单词）、原生属性兼容、组件边界控制 |

### 设计原则

| # | 原则 | 核心要求 | 可判定性 |
|---|------|---------|---------|
| 1 | 原生语义优先 | 保留 `<button>` 的 type/disabled/onClick 语义 | 脚本化 |
| 2 | 行为与表现分离 | variant/size 只影响视觉，不影响行为 | LLM 评估 |
| 3 | variant 驱动 | 所有视觉变体通过统一 `variant` prop 表达 | 脚本化 |
| 4 | API 与原生属性边界 | 自定义属性不得与 HTML 原生属性冲突 | 脚本化+LLM |
| 5 | 属性命名规范 | camelCase + 双单词语义 | 脚本化 |
| 6 | 组件边界与职责控制 | Button 只负责单一交互触发，组合能力独立拆分 | LLM 评估 |

### Crate 定义
> metadata仅作参考
#### Crate A: `button-core`

| 字段 | 值 |
|------|-----|
| **name** | `button-core` |
| **type** | `library` |
| **responsibility** | 封装 Button 组件核心实现：variant/size 系统、原生 button 属性转发（type/disabled/onClick）、ref 转发、无障碍基础支持（aria-label、role）、asChild 模式（与 Next.js Link 集成） |
| **metadata** | `{"package": "shadcn/ui", "component": "Button", "principles": ["native-semantics-first", "behavior-presentation-separation", "variant-driven"]}` |

**包含内容**：
- `Button` 组件（默认导出 + 命名导出）
- `buttonVariants()` — cva 驱动的 variant/size 工厂函数
- `ButtonProps` 类型（继承 `ButtonHTMLAttributes`，扩展 variant/size/asChild）
- `forwardRef` → 底层 `<button>` 元素
- `asChild` 通过 Slot 实现（Radix）
- 纯图标按钮的 `aria-label` 强制检测

**受约束的 Archetype**：`button-best-practice`、`component-design-best-practice`

#### Crate B: `button-styles`

| 字段 | 值 |
|------|-----|
| **name** | `button-styles` |
| **type** | `utility` |
| **responsibility** | Button 视觉 token 系统：variant 6 种变体的 Tailwind 类映射、size 8 级尺寸的 padding/font-size 配置、rounded/icon 特殊样式的类组合、与全局主题变量的集成（CSS 自定义属性） |
| **metadata** | `{"package": "class-variance-authority", "variants": ["default", "destructive", "secondary", "outline", "ghost", "link"], "sizes": ["xs", "sm", "default", "lg", "icon-xs", "icon-sm", "icon", "icon-lg"]}` |

**包含内容**：
- `cva` 配置对象（base + variants + compoundVariants）
- 颜色 token 引用（`bg-primary`, `text-primary-foreground` 等）
- 尺寸 token 映射表
- `icon-*` 尺寸的宽高平方约束（`size-6`, `size-8`, `size-9`, `size-10`）
- hover/focus-visible/disabled 状态样式

**受约束的 Archetype**：`button-best-practice`

### Archetype 契约定义
**Name**: `button-best-practice`
**Scope**: `crate`
**Concept**: 确保 Button 组件遵循原生语义优先、表现与行为分离、variant 驱动、API 边界清晰的设计原则

##### C-1: 原生 button 语义保留
- **ID**: `c-btn-native-semantics`
- **类型**: `text`
- **排序**: 1
- **条件内容**:
  ```
  Button 组件必须保留原生 <button> 元素的语义。type 属性默认为 "button"（禁止默认 "submit"
  以避免表单中误触提交）。支持 type="submit" 和 type="reset" 的显式声明。
  禁止用 <div> 或 <span> 模拟按钮行为（除非通过 asChild 继承 Slot 的语义传递）。

  ❌ 违规: <div onClick={handler} role="button" tabIndex={0}>Click</div>
  ✅ 正确: <Button type="button" onClick={handler}>Click</Button>
  ```

##### C-2: disabled 状态原生支持
- **ID**: `c-btn-disabled-native`
- **类型**: `text`
- **排序**: 2
- **条件内容**:
  ```
  Button 的禁用状态必须通过原生 disabled 属性实现，禁止仅通过 CSS 视觉模拟
  （如 pointer-events-none + opacity-50 而不设置 disabled）。

  ❌ 违规: <Button className="pointer-events-none opacity-50">Disabled</Button>
  ✅ 正确: <Button disabled>Disabled</Button>

  原因：仅靠 CSS 模拟会导致键盘导航和屏幕阅读器仍将按钮视为可操作。
  ```

##### C-3: forwardRef 转发
- **ID**: `c-btn-forward-ref`
- **类型**: `text`
- **排序**: 3
- **条件内容**:
  ```
  Button 组件必须使用 React.forwardRef 将 ref 转发到底层 <button> 元素。
  这确保父组件可以通过 ref 访问原生 DOM 节点（如焦点管理、动画触发）。

  ❌ 违规: function Button(props: ButtonProps) { return <button {...props} /> }
           // 无 ref 转发，外部无法通过 ref 操作 DOM
  ✅ 正确:
    const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
      ({ variant, size, ...props }, ref) => (
        <button ref={ref} {...props} />
      )
    );
  ```

##### C-4: variant 驱动视觉
- **ID**: `c-btn-variant-driven`
- **类型**: `text`
- **排序**: 4
- **条件内容**:
  ```
  Button 的所有视觉变体必须通过 `variant` prop 表达。禁止通过直接 className
  覆盖背景色、文字色等核心视觉属性来绕过 variant 系统。

  ❌ 违规:
    <Button className="bg-red-500 text-white hover:bg-red-600">
      Delete
    </Button>
    // 应使用 variant="destructive"

  ✅ 正确:
    <Button variant="destructive">Delete</Button>

  注：className 可用于 margin、flex、width 等布局属性，但不得覆盖 variant 已定义的
  颜色、边框、hover/focus 状态。
  ```

##### C-5: 六种 variant 完整性
- **ID**: `c-btn-variant-completeness`
- **类型**: `text`
- **排序**: 5
- **条件内容**:
  ```
  Button 组件必须支持全部六种 variant：default、destructive、secondary、
  outline、ghost、link。每种 variant 必须覆盖 default/hover/focus-visible/
  disabled 四个状态。

  ❌ 违规: 只实现了 default 和 outline 两种 variant
  ✅ 正确: cva variants 中完整定义六种变体及各自的状态样式
  ```

##### C-6: size 八级尺寸
- **ID**: `c-btn-size-scale`
- **类型**: `text`
- **排序**: 6
- **条件内容**:
  ```
  Button 组件必须支持完整的八级尺寸系统：
  - 文本按钮：xs, sm, default, lg
  - 图标按钮：icon-xs, icon-sm, icon, icon-lg

  图标专属尺寸必须确保宽高相等（正方形），使用 Tailwind 的 size-N 工具类
  或显式设置相同的 width/height。

  ❌ 违规: 图标按钮使用 sm 而非 icon-sm，导致宽高不相等
  ✅ 正确: size="icon-sm" → size-8（32px × 32px）
  ```

##### C-7: 纯图标按钮 aria-label 强制
- **ID**: `c-btn-icon-aria-label`
- **类型**: `text`
- **排序**: 7
- **条件内容**:
  ```
  纯图标按钮（无文字内容）必须设置 aria-label 属性，为屏幕阅读器提供可读的功能描述。
  禁止仅依赖图标语义（如 aria-hidden="true" 的图标）而不提供替代文本。

  ❌ 违规:
    <Button size="icon">
      <SearchIcon />  {/* 无 aria-label */}
    </Button>

  ✅ 正确:
    <Button size="icon" aria-label="Search">
      <SearchIcon />
    </Button>
  ```

##### C-8: 带图标按钮 data-icon 间距
- **ID**: `c-btn-with-icon-spacing`
- **类型**: `text`
- **排序**: 8
- **条件内容**:
  ```
  图标 + 文字组合按钮必须使用 data-icon 属性控制图标与文字的间距。
  图标在左（inline-start）或图标在右（inline-end）各需不同的间距策略。

  ❌ 违规: 图标与文字之间无间距，视觉粘连
  ✅ 正确:
    <Button>
      <GitBranchIcon data-icon="inline-start" />
      New Branch
    </Button>
    或使用 gap-2 统一间距
  ```

##### C-9: Spinner 加载态
- **ID**: `c-btn-spinner-loading`
- **类型**: `text`
- **排序**: 9
- **条件内容**:
  ```
  加载状态按钮必须同时满足：
  1. 设置 disabled 属性（阻止重复点击）
  2. 集成 Spinner 组件（视觉反馈）
  3. 保留按钮文字（让用户知道正在处理什么）
  4. Spinner 使用 data-icon 控制与文字的间距

  ❌ 违规: 加载时仅显示 Spinner 不保留文字
  ❌ 违规: 加载时不设置 disabled，用户可重复点击
  ✅ 正确:
    <Button disabled>
      <Spinner data-icon="inline-start" />
      Generating
    </Button>
  ```

##### C-10: asChild 用于路由跳转
- **ID**: `c-btn-aschild-link`
- **类型**: `text`
- **排序**: 10
- **条件内容**:
  ```
  Button 用作链接跳转时，必须通过 asChild + Next.js Link 实现，禁止添加自定义
  href/to 属性。这确保路由行为完全由 Next.js 控制，Button 只负责视觉样式。

  ❌ 违规: <Button href="/login">Login</Button>  // 自定义 href
  ❌ 违规: <button onClick={() => router.push('/login')}>Login</button>
           // 失去 Button 的样式体系
  ✅ 正确:
    <Button asChild>
      <Link href="/login">Login</Link>
    </Button>
  ```

##### C-11: camelCase + 双单词属性命名
- **ID**: `c-btn-prop-naming`
- **类型**: `text`
- **排序**: 11
- **条件内容**:
  ```
  Button 的自定义属性必须使用 camelCase 命名，语义复杂时使用双单词或多单词组合。
  属性名称必须自解释（self-documenting），禁止缩写或单字母命名。

  ❌ 违规: <Button vis="outline" sz="sm" />  // 缩写
  ❌ 违规: <Button v="outline" />  // 单字母
  ✅ 正确: variant, size, ariaLabel, dataIcon
  ```

##### C-12: 不覆盖原生属性
- **ID**: `c-btn-no-native-override`
- **类型**: `text`
- **排序**: 12
- **条件内容**:
  ```
  Button 组件的自定义属性不得与 HTMLButtonElement 原生属性冲突或覆盖。
  自定义属性仅用于表达原生属性无法覆盖的组件语义（如 variant、size）。
  原生属性（type、disabled、onClick、form 等）必须直接透传到 <button> 元素。

  ❌ 违规: 组件的 type prop 控制的是 visual type 而非 HTML type
  ✅ 正确: type 直接对应 <button type="...">，视觉变体用 variant
  ```

##### C-13: 命名导出 + 一文件一组件
- **ID**: `c-btn-named-export`
- **类型**: `text`
- **排序**: 13
- **条件内容**:
  ```
  Button 组件必须使用命名导出（named export），禁止默认导出。
  每个文件只包含一个组件（Button.tsx 只导出 Button，不导出其他组件）。

  ❌ 违规: export default function Button() {}
  ❌ 违规: 在 Button.tsx 中同时导出 Button 和 ButtonGroup
  ✅ 正确: export { Button } 或 export const Button = ...
  ```

---
## Button Group
### 能力模型

| 层级 | 职责 | 包含要素 |
|------|------|---------|
| **核心能力** | 结构容器 | 聚合多个 Button、布局管理、`role="group"` 语义化、保持 Button 行为独立 |
| **表现能力** | 视觉与布局表达 | orientation（方向）、size inheritance（尺寸继承）、separator（分隔）、split/nested/input/dropdown/select/popover 组合形态 |
| **扩展能力** | 与其他组件组合 | Input/InputGroup、DropdownMenu、Select、Popover、Tooltip |
| **工程能力** | 可维护性 | API 设计规范、与 Button 依赖关系、无障碍规范、可组合性 |

### 设计原则

| # | 原则 | 核心要求 |
|---|------|---------|
| 1 | Button 语义优先 | Button Group 不得改变 Button 原生语义，只负责组织 |
| 2 | 组合与行为分离 | Button 负责行为，Button Group 负责组合 |
| 3 | 结构优先 | Button Group 的核心价值是结构，而非样式 |
| 4 | API 边界 | Button Group 属性不得与 Button 属性冲突 |
| 5 | 职责单一 | 只负责"组合"，不承担业务/状态逻辑 |

### 组合形态

| 形态 | 描述 | 典型场景 |
|------|------|---------|
| **Orientation** | 水平（默认）/ 垂直布局 | 工具栏 vs 侧边操作栏 |
| **Size** | 尺寸协同（sm/default/lg + icon-*） | 全组统一尺寸 |
| **Separator** | 按钮间视觉分隔 | 复制/粘贴、保存/取消 |
| **Split** | 主操作 + 附属下拉图标 | Follow + 下拉选项 |
| **Nested** | 双层 ButtonGroup 嵌套 | 消息输入框（加号按钮 + 输入区 + 语音按钮） |
| **Input** | 输入框 + 操作按钮一体化 | 搜索栏 |
| **Dropdown Menu** | 主按钮 + 下拉菜单 | Follow 按钮 + 更多操作 |
| **Select** | 选择器 + 输入框 + 操作按钮 | 货币选择 + 金额输入 + 发送 |
| **Popover** | 功能按钮 + 弹出层 | Copilot + 任务输入弹层 |

### Crate 定义
#### Crate A: `button-group`

| 字段 | 值 |
|------|-----|
| **name** | `button-group` |
| **type** | `module` |
| **responsibility** | ButtonGroup 结构容器：orientation 布局控制、size 尺寸继承传递、ButtonGroupSeparator 分隔组件、split 拆分模式、nested 嵌套支持、`role="group"` 语义 + aria-label/labelledby 无障碍 |
| **metadata** | `{"components": ["ButtonGroup", "ButtonGroupSeparator", "ButtonGroupText"], "patterns": ["orientation", "separator", "split", "nested"]}` |

**包含内容**：
- `ButtonGroup` 容器（接收 orientation、size、aria-label/labelledby）
- `ButtonGroupSeparator` — 视觉分隔线
- `ButtonGroupText` — 文本标签（配合 aria-labelledby 使用）
- 通过 React Context 传递 size 给子 Button
- `cn()` + `cva` 布局样式（flex、gap、rounded 裁剪）

**受约束的 Archetype**：`button-group-best-practice`（全部 Condition）、`component-design-best-practice`

#### Crate B: `button-compositions`

| 字段 | 值 |
|------|-----|
| **name** | `button-compositions` |
| **type** | `module` |
| **responsibility** | Button Group 与外部组件的高阶组合模式：Input/InputGroup 搜索栏、DropdownMenu 下拉菜单按钮、Select 选择器联动、Popover 弹出层按钮、Tooltip 提示按钮。提供组合模板和类型安全的 props 接口，供页面直接使用 |
| **metadata** | `{"integrations": ["Input", "InputGroup", "DropdownMenu", "Select", "Popover", "Tooltip"], "patterns": ["search-bar", "split-dropdown", "select-action", "popover-form", "tooltip-icon"]}` |

**包含内容**：
- `SearchButtonGroup` — Input + Button 一体化搜索模板
- `SplitDropdownButton` — 主按钮 + 下拉菜单模板
- `SelectActionGroup` — Select + Input + Button 联动模板
- `PopoverButton` — 弹出层表单模板
- 各模板的 TypeScript 泛型 props 类型

**受约束的 Archetype**：`button-group-best-practice`（§D 扩展能力 Condition）、`component-composition-best-practice`

### Archetype 契约定义
**Name**: `button-group-best-practice`
**Scope**: `crate`
**Concept**: 确保 ButtonGroup 作为纯粹的结构容器，不引入新的行为语义，保持 Button 的独立性和可组合性

##### C-1: role="group" + 无障碍标注
- **ID**: `c-btg-role-group`
- **类型**: `text`
- **排序**: 1
- **条件内容**:
  ```
  ButtonGroup 必须设置 role="group"（默认值，显式声明更佳），并且必须提供
  aria-label（直接描述）或 aria-labelledby（关联外部标签），向辅助技术
  说明按钮组的用途。

  ❌ 违规: <ButtonGroup><Button>A</Button><Button>B</Button></ButtonGroup>
           // 无 aria-label，屏幕阅读器无法解释分组用途
  ✅ 正确:
    <ButtonGroup aria-label="Text formatting">
      <Button variant="outline" size="sm">Bold</Button>
      <Button variant="outline" size="sm">Italic</Button>
    </ButtonGroup>
  ```

##### C-2: 不引入行为逻辑
- **ID**: `c-btg-no-behavior`
- **类型**: `text`
- **排序**: 2
- **条件内容**:
  ```
  ButtonGroup 禁止定义任何业务行为逻辑。不得包含 onClick、onChange、状态管理
  等行为相关代码。所有行为必须由子 Button 独自处理。

  ❌ 违规: <ButtonGroup onClick={handleGroupClick}>
  ❌ 违规: ButtonGroup 内部使用 useState 管理选中状态
  ✅ 正确: ButtonGroup 仅提供 className/orientation/aria-label + children
  ```

##### C-3: 不覆盖子 Button 属性
- **ID**: `c-btg-no-prop-override`
- **类型**: `text`
- **排序**: 3
- **条件内容**:
  ```
  ButtonGroup 不得覆盖或修改子 Button 的 variant、size、disabled 等核心属性。
  ButtonGroup 的 size 属性仅作为子 Button 的默认值（如子 Button 未显式设置 size
  则继承），不得强制覆盖已显式声明的子 Button 属性。

  ❌ 违规: ButtonGroup 强制所有子 Button 使用同一 variant
  ✅ 正确: size 通过 React Context 传递，子 Button 可显式覆盖
  ```

##### C-4: orientation 方向控制
- **ID**: `c-btg-orientation`
- **类型**: `text`
- **排序**: 4
- **条件内容**:
  ```
  ButtonGroup 必须支持 orientation 属性，取值 "horizontal"（默认）和 "vertical"。
  horizontal 使用 flex-row，vertical 使用 flex-col。布局切换不得影响子 Button 的行为。

  Orientation 通过 Tailwind 的 flex 工具类实现，禁止使用绝对定位或 float。

  ✅ 正确:
    horizontal → flex gap-0（子元素紧贴）
    vertical → flex flex-col gap-0
  ```

##### C-5: 尺寸继承机制
- **ID**: `c-btg-size-inheritance`
- **类型**: `text`
- **排序**: 5
- **条件内容**:
  ```
  ButtonGroup 的 size 属性通过 React Context 向下传递，子 Button 若未显式设置
  size 则自动继承 ButtonGroup 的 size。图标按钮需要使用对应的 icon-* 尺寸。
  
  尺寸继承链：ButtonGroup size → Context → 子 Button（可显式覆盖）

  ✅ 正确:
    <ButtonGroup size="sm">
      <Button variant="outline">Small</Button>         {/* 继承 sm */}
      <Button variant="outline">Button</Button>         {/* 继承 sm */}
      <Button variant="outline" size="icon-sm">         {/* 显式覆盖为 icon-sm */}
        <PlusIcon />
      </Button>
    </ButtonGroup>
  ```

##### C-6: Separator 使用规范
- **ID**: `c-btg-separator`
- **类型**: `text`
- **排序**: 6
- **条件内容**:
  ```
  ButtonGroupSeparator 用于在按钮组内添加视觉分隔线。
  
  使用建议：
  - outline variant 的 Button 自带边框，通常无需分隔符
  - 其他 variant（default/secondary/ghost）建议添加分隔符
  - Separator 应是纯视觉元素（`<div>` 或 `<span>`），不带交互能力

  ❌ 违规: Separator 用 <button> 实现
  ✅ 正确: <ButtonGroupSeparator /> → <div role="separator" aria-hidden="true" />
  ```

##### C-7: Split 拆分模式
- **ID**: `c-btg-split-pattern`
- **类型**: `text`
- **排序**: 7
- **条件内容**:
  ```
  Split 模式（一个主操作 + 一个附属操作）通过 ButtonGroup + ButtonGroupSeparator
  实现。主按钮使用文本，附属按钮使用图标。两者共享相同的 variant 和 size。

  ❌ 违规: 主按钮和附属按钮使用不同的 variant，视觉不统一
  ✅ 正确:
    <ButtonGroup>
      <Button variant="secondary">Follow</Button>
      <ButtonGroupSeparator />
      <Button variant="secondary" size="icon">
        <ChevronDownIcon />
      </Button>
    </ButtonGroup>
  ```

##### C-8: 嵌套 ButtonGroup 规范
- **ID**: `c-btg-nested`
- **类型**: `text`
- **排序**: 8
- **条件内容**:
  ```
  ButtonGroup 支持嵌套（ButtonGroup 内嵌套另一个 ButtonGroup），用于模块化功能拆分。
  嵌套层级不超过 2 层。每个子 ButtonGroup 独立设置自己的无障碍标注。

  ✅ 正确:
    {/* 外层：整体消息输入布局 */}
    <ButtonGroup aria-label="Message input">
      {/* 内层子组 1：加号图标按钮 */}
      <ButtonGroup>
        <Button variant="outline" size="icon"><PlusIcon /></Button>
      </ButtonGroup>
      {/* 内层子组 2：输入框 + 语音按钮 */}
      <ButtonGroup>
        <InputGroup>...</InputGroup>
      </ButtonGroup>
    </ButtonGroup>
  ```

##### C-9: 外部组件组合接口
- **ID**: `c-btg-external-composition`
- **类型**: `text`
- **排序**: 9
- **条件内容**:
  ```
  ButtonGroup 与外部组件（DropdownMenu、Select、Popover、Tooltip、Input）
  组合时，必须保持各自组件的独立性和正确的层级关系：

  - DropdownMenu：DropdownMenuTrigger 通过 asChild 继承 Button 样式
  - Select：SelectTrigger 放在 ButtonGroup 内，保持视觉统一
  - Popover：PopoverTrigger 通过 asChild 继承 Button 样式
  - Tooltip：TooltipTrigger 包裹目标 Button，不包裹整个 ButtonGroup
  - Input：Input 直接作为 ButtonGroup 子元素，与 Button 共享布局

  ❌ 违规: Tooltip 包裹整个 ButtonGroup 而非单个 Button
  ❌ 违规: 组合时手动覆写了组件的核心样式
  ```

##### C-10: ButtonGroup vs ToggleGroup 区分
- **ID**: `c-btg-vs-togglegroup`
- **类型**: `text`
- **排序**: 10
- **条件内容**:
  ```
  当按钮之间存在状态关联（选中/未选中、互斥、多选）时，必须使用 ToggleGroup
  而非 ButtonGroup。ButtonGroup 仅用于无状态关联的独立操作分组。

  | 场景 | 使用 |
  |------|------|
  | 提交 + 取消 | ButtonGroup |
  | 加粗 + 斜体 + 下划线（格式切换） | ToggleGroup |
  | 复制 + 粘贴 | ButtonGroup |
  | 左对齐 + 居中 + 右对齐（单选） | ToggleGroup |

  ❌ 违规: 用 ButtonGroup + useState 管理选中状态来实现 ToggleGroup 的功能
  ✅ 正确: 有状态关联 → 使用专门的 ToggleGroup 组件
  ```

---
## 依赖关系

| Archetype                                     | Scope   | 约束 Crate                             | Condition 数 | 说明                |
| --------------------------------------------- | ------- | ------------------------------------ | ----------- | ----------------- |
| **`button-best-practice`**                    | `crate` | `button-core`、`button-styles`        | 13          | Button 组件设计契约     |
| **`button-group-best-practice`**              | `crate` | `button-group`、`button-compositions` | 10          | Button Group 结构契约 |
