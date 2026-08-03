# ProjectFileTree题目

---
## code

你标记的疑问：
- `if (!current) continue`：`pop()` 的类型永远包含 `undefined`。虽然这里运行时几乎不会为空，但这行用于 TypeScript 类型收窄和防御性保护。
- `identity` 为什么会不同：切换 owner、repo 或 branch 时，新 props 会先 render，而旧 state 要等 `useEffect` 才更新，中间会短暂不一致。这个判断防止旧仓库的展开路径泄漏到新仓库。
- `DEFAULT_EXPANDED_PATHS` 是空集合，表示全部折叠，不是全部展开。
- `overscan` 就是虚拟列表缓冲区。它会在视口外额外渲染 12 行，减少快速滚动时的空白闪烁。
- 两次 `reverse()` 是为了配合栈的 `pop()`，在深度优先遍历时仍保持原始显示顺序。
- 第 4 题应写成 `reconcileExpandedPaths(currentState.paths, directoryPaths)`。你的反向调用所得成员碰巧相同，但数据流语义不准确。

```ts
import { useVirtualizer } from "@tanstack/react-virtual";
import type { GitHubFileNode } from "@repo/schemas";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  PROJECT_FILE_TREE_ROW_HEIGHT,
  ProjectFileTreeNode,
} from "./ProjectFileTreeNode";

const FILE_TREE_OVERSCAN = 12;
const DEFAULT_EXPANDED_PATHS = new Set<string>();

type VisibleProjectFileTreeNode = {
  // 相比于普通的node，多了一个深度的值，这个值是用来展示树状结构使用的
  depth: number;

  node: GitHubFileNode;
};

// (parameter) nodes: {
//   name: string;
//   path: string;
//   type: "file" | "dir";
//   sha: string;
//   size ?: number | undefined;
//   children ?: ...[] | undefined;
// } []

// 这种处理的方式还挺常见的，就是将具有父子关系的数组项进行处理
const collectDirectoryPaths = (nodes: GitHubFileNode[]): Set<string> => {
  const directoryPaths = new Set<string>();
  const pendingNodes = [...nodes];

  while (pendingNodes.length > 0) {

    // 不停的去取出dir节点
    const node = pendingNodes.pop();
    if (!node || node.type !== "dir") continue;


    // 然后将节点的path加入答案，再将其children加入待处理的数组中
    directoryPaths.add(node.path);
    if (node.children) pendingNodes.push(...node.children);
  }

  return directoryPaths;
};

/**
 * 简单来讲就是给每个可视节点加个depth
 * @param nodes 
 * @param expandedPaths 
 * @returns 
 */
const flattenVisibleProjectFileTree = (nodes: GitHubFileNode[], expandedPaths: ReadonlySet<string>): VisibleProjectFileTreeNode[] => {

  //   type VisibleProjectFileTreeNode = {
  //     depth: number;
  //     node: {
  //       name: string;
  //       path: string;
  //       type: "file" | "dir";
  //       sha: string;
  //       size?: number | undefined;
  //       children?: ...[] | undefined;
  //   };
  // }

  const visibleNodes: VisibleProjectFileTreeNode[] = [];

  // [...nodes]是浅拷贝了一个新的数组，反转了，然后为每个node添加一个depth的属性
  const pendingNodes = [...nodes].reverse().map((node) => ({ depth: 0, node }));

  while (pendingNodes.length > 0) {
    // 这里面的逻辑和上面的collectDirectoryPaths很像

    const current = pendingNodes.pop();

    // TODO这里是做什么的，有点诡异，还有不存在的情况吗
    if (!current) continue;

    visibleNodes.push(current);
    const { node, depth } = current;

    // 如果是file，或者不展开dir的节点，或者没有孩子的dir节点（不可能展开的），直接下一个节点
    if (node.type !== "dir" || !expandedPaths.has(node.path) || !node.children) continue;

    // 如果是可展开的dir，那么就钱拷贝其孩子，然后加入到待处理的数组中，但是其depth相对于父节点 + 1
    // 这里很巧妙，一个file节点，不是为0的depth就是在一个dir的children中存在，所以，你只要处理dir的孩子的深度+1就可以了。
    for (const child of [...node.children].reverse()) {
      pendingNodes.push({ depth: depth + 1, node: child });
    }

  }

  return visibleNodes;
};

const reconcileExpandedPaths = (
  expandedPaths: ReadonlySet<string>,
  directoryPaths: ReadonlySet<string>,
): Set<string> => {
  const nextExpandedPaths = new Set<string>();

  for (const path of expandedPaths) {
    if (directoryPaths.has(path)) nextExpandedPaths.add(path);
  }

  return nextExpandedPaths;
};

/**
 * 检测两个string set 的内容是不是一样的
 * @param firstPaths 
 * @param secondPaths 
 * @returns 
 */
const arePathSetsEqual = (
  firstPaths: ReadonlySet<string>,
  secondPaths: ReadonlySet<string>,
): boolean => {

  // 长度不一样，直接死刑
  if (firstPaths.size !== secondPaths.size) return false;

  // 长度一样，那就是其中有可能是不一样的项，而这种项，肯定是一个有一个没有的，这里太妙了：
  for (const path of firstPaths) {
    if (!secondPaths.has(path)) return false;
  }

  return true;
};

export type ProjectFileTreeProps = {
  branch: string;
  isFetching: boolean;
  nodes: GitHubFileNode[];
  onScan: (path: string, scope: "file" | "directory") => void;
  onSelectFile: (path: string) => void;
  owner: string;
  repo: string;
  selectedPath: string | null;
};

export const ProjectFileTree = function ({
  isFetching,
  nodes,
  onScan: handleScan,
  onSelectFile: handleSelectFile,
  owner,
  repo,
  branch,
  selectedPath,
}: ProjectFileTreeProps) {
  // ============================================================
  // 📝 第1题：建立文件树的基础运行上下文
  // ============================================================
  // 获取翻译函数，创建滚动容器 ref，并根据 owner、repo、branch 生成稳定的
  // treeIdentity；同时从 nodes 派生当前仍然存在的全部目录路径。
  // （提示：useTranslation、useRef<HTMLDivElement>、useMemo、
  // JSON.stringify、collectDirectoryPaths；两个 useMemo 的依赖要精确）
  console.log("nodes", nodes)
  console.log("owner, repo, branch", owner, repo, branch)
  console.log("selectedPath", selectedPath)
  console.log("isFetching", isFetching)

  // ✏️ 你的代码：
  const { t } = useTranslation();
  const scrollRef = useRef<HTMLDivElement>(null)

  // 一棵树的唯一身份
  const treeIdentity = useMemo(() => JSON.stringify([owner, repo, branch]), [owner, repo, branch]);

  // 从nodes中收集路径
  const directoryPaths = useMemo(() => collectDirectoryPaths(nodes), [nodes]);

  // ============================================================
  // 📝 第2题：设计可跨仓库切换的展开状态
  // ============================================================
  // expansionState 同时保存 identity 和 Set<string>。只有状态的 identity 与
  // treeIdentity 一致时才使用其中的 paths，否则立即派生为空的默认展开集合；
  // 不要通过渲染期间 setState 来完成切换。
  // （提示：useState<{ identity: string; paths: Set<string> }>、
  // DEFAULT_EXPANDED_PATHS；expandedPaths 是派生值）

  // ✏️ 你的代码：

  // 这里维护着树的id与其展开的路径
  const [expansionState, setExpansionState] = useState<{ identity: string, paths: Set<string> }>({ identity: treeIdentity, paths: DEFAULT_EXPANDED_PATHS })

  // 只有当前的树id与我的展开状态中的id一致的时候才去尝试使用其中的值，也就是说，在最开始的时候，所有的的dir节点都是展开的状态呢
  // TODO 这里怎么会有不同的，不应该是一样的吗
  const expandedPaths = expansionState.identity === treeIdentity
    ? expansionState.paths
    : DEFAULT_EXPANDED_PATHS;

  // ============================================================
  // 📝 第3题：扁平化可见节点并配置虚拟列表
  // ============================================================
  // 根据 nodes 与 expandedPaths 计算带 depth 的可见节点，再创建 virtualizer。
  // 行数取可见节点数，行高使用 PROJECT_FILE_TREE_ROW_HEIGHT，滚动元素来自
  // scrollRef；key 优先使用节点 path，并配置项目给出的 overscan 与 flushSync。
  // （提示：useMemo、flattenVisibleProjectFileTree、useVirtualizer、
  // FILE_TREE_OVERSCAN；getItemKey 需要处理越界索引）

  // ✏️ 你的代码：
  const visibleNodes = useMemo(() => flattenVisibleProjectFileTree(nodes, expandedPaths), [nodes, expandedPaths])

  const virtualizer = useVirtualizer({
    count: visibleNodes.length,
    estimateSize: () => PROJECT_FILE_TREE_ROW_HEIGHT,

    // 使用一个节点的路径作为其key
    getItemKey: (index) => visibleNodes[index]?.node.path ?? index,
    getScrollElement: () => scrollRef.current,
    //TODO 这里难道是缓冲区吗
    overscan: FILE_TREE_OVERSCAN,
    useFlushSync: false,
  })

  // ============================================================
  // 📝 第4题：协调异步刷新后的展开路径
  // ============================================================
  // 当目录集合或文件树身份变化时更新 expansionState：身份变化则清空旧仓库的
  // 展开路径；身份不变则移除已经不存在的目录。若路径集合实际未变化，必须返回
  // 原 state，避免无意义渲染。
  // （提示：useEffect、setExpansionState 函数式更新、
  // reconcileExpandedPaths、arePathSetsEqual；依赖 directoryPaths、treeIdentity）

  // ✏️ 你的代码：

  useEffect(() => {
    setExpansionState((currentState) => {
      // 
      if (currentState.identity !== treeIdentity) return { identity: treeIdentity, paths: new Set(DEFAULT_EXPANDED_PATHS) }

      const nextPaths = reconcileExpandedPaths(directoryPaths, currentState.paths)

      return arePathSetsEqual(currentState.paths, nextPaths)
        ? currentState
        : { identity: treeIdentity, paths: nextPaths };
    }
    )
  }, [treeIdentity, directoryPaths])



  // ============================================================
  // 📝 第5题：切换文件树时复位滚动位置
  // ============================================================
  // treeIdentity 变化后，把滚动容器恢复到顶部；容器尚未挂载时不得报错。
  // （提示：useEffect、scrollRef.current、scrollTo、可选链）

  // ✏️ 你的代码：
  /**
   * 这里是我字节写出来的，哈哈哈
   */
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: 0 })
  }, [treeIdentity])

  // ============================================================
  // 📝 第6题：以不可变方式切换目录展开状态
  // ============================================================
  // 创建 handleToggleDirectory(path)：使用函数式 setState，并复制 Set 后再
  // add/delete。若旧状态属于另一棵树，应从默认集合开始，返回值必须绑定当前
  // treeIdentity，避免快速切换仓库时把旧路径带入新仓库。
  // （提示：useCallback、new Set、Set.has/add/delete；依赖 treeIdentity）

  // ✏️ 你的代码：

  const handleToggleDirectory = useCallback((path: string) => {
    setExpansionState((currentState) => {
      const curPaths = currentState.identity !== treeIdentity ? DEFAULT_EXPANDED_PATHS : currentState.paths

      const nextPaths = new Set(curPaths)
      
      if (nextPaths.has(path)) nextPaths.delete(path);
      else nextPaths.add(path);

      return { identity: treeIdentity, paths: nextPaths }
      
    })
  }, [treeIdentity])

  // ============================================================
  // 📝 第7题：渲染具备语义和定位信息的虚拟文件树
  // ============================================================
  // 返回滚动容器与 role="tree" 的内部画布。画布高度来自虚拟列表总高度；
  // 遍历虚拟行，通过 index 找到 visibleNode，越界时返回 null。每一行使用绝对
  // 定位的 size/start，并将业务 Props、depth、expanded 与三个事件回调完整传给
  // ProjectFileTreeNode。滚动容器还需用 aria-busy 表达刷新状态。
  // （提示：virtualizer.getTotalSize/getVirtualItems、virtualRow.size/start；
  // key 使用 node.path，aria-label 使用 repositoryDetail.selectFileDesc）

  // ✏️ 你的代码：
  return (
    <div ref={scrollRef} aria-busy={isFetching} className="flex-1 overflow-auto p-2">
      <div
        className="relative w-full"
        role="tree"
        style={{height: virtualizer.getTotalSize() }}
      >
        {
          virtualizer.getVirtualItems().map((item) => {
            const node = visibleNodes[item.index];

            if (!node) return null
            
            return (
              <div key={node.node.path} className="absolute left-0 top-0 w-80"
                style={{
                  height: item.size,
                  top: item.start
                  , backgroundColor: "green"
                  ,
                }}
              > 
                <div className="border-red-100" style={{
                  
                }}>
                  <ProjectFileTreeNode
                    branch={branch}
                    depth={node.depth}
                    expanded={expandedPaths.has(node.node.path)}
                    node={node.node}
                    owner={owner}
                    repo={repo}
                    selectedPath={selectedPath}
                    onScan={handleScan}
                    onSelectFile={handleSelectFile}
                    onToggleDirectory={handleToggleDirectory}
                  />
                </div>
              </div>
            )
          })
        }

      </div>
    </div>
  );
};

```