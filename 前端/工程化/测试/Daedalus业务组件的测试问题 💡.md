# Daedalus业务组件的测试问题 💡
> Last Format Time：9/16/2026 19:24:53

---
## 目前Daedalus中的组件测试是几乎没作用的
比如：

去检查导出类型是不是function

```javascript
import { describe, expect, it } from "vitest";
import { AnatomiesCreateDialog } from "./AnatomiesCreateDialog";


describe("AnatomiesCreateDialog", () => {
  it("exports a named page-bound dialog component", () => {
    expect(AnatomiesCreateDialog).toBeTypeOf("function");
  });
});
```

读取组件的文件内容，转成字符串去验证。对无害、无意义重构非常敏感，每次都要改，对真正的 Bug 不敏感。

```javascript
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const source = readFileSync(new URL("ConditionTypeSelector.tsx", import.meta.url), "utf8");

describe("ConditionTypeSelector", () => {
  it("owns the text-versus-reference type choice", () => {
    expect(source).toContain('value: "text"');
    expect(source).toContain('value: "archetype_ref"');
    expect(source).toContain("handleTypeClick");
    expect(source).toContain("conditionType === option.value");
    expect(source).not.toContain("<Textarea");
    expect(source).not.toContain("<Select");
    expect(source).not.toContain("handleMove");
  });
});
```

代码里写了这些东西不能证明什么，Agent写这种无用测试，常出现于一个较大的任务中，不能一次性的尝试去解决太多的逻辑闭环

---
## 有效的测试
https://github.com/supabase/supabase/blob/master/apps/studio/components/interfaces/Workers/WorkersList.test.tsx

https://github.com/PostHog/posthog/blob/master/products/desktop/packages/ui/src/features/canvas/components/ChannelSidebar.test.tsx

我找了几个仓库中的测试来看
发现他们的测试会去验证给定状态下，用户执行某个操作后，组件产生了正确且可观察的结果：
```javascript
  // 测试点击
  it('refreshes the workers list on request', async () => {
    const onRefresh = vi.fn()
    renderList([worker('embed')], onRefresh)

    // 点击按钮，而不是去确认有没有 <button...
    await userEvent.click(screen.getByRole('button', { name: 'Refresh' }))

    // 验证事件处理函数被执行，而不是去确认有没有 onRefresh
    expect(onRefresh).toHaveBeenCalledOnce()
  })
```

```javascript
  // 测试翻页
  it('pages through the workers ten at a time', async () => {
    // 制造12条数据
    const workers = Array.from({ length: 12 }, (_, index) => worker(`worker-${index}`))
    renderList(workers)
    
    // 应该只有10个展示出来了，因为组件的PAGE_SIZE = 10，剩下的两条在下一页
    expect(rowNames()).toHaveLength(10)
    // 总共两页 当前第一页
    expect(screen.getByText('Page 1 of 2')).toBeVisible()
    // Previous 前一页按钮应该 disabled
    expect(screen.getByRole('button', { name: 'Previous page' })).toBeDisabled()
    // 点击下一页
    await userEvent.click(screen.getByRole('button', { name: 'Next page' }))
    // 展示剩下的两条
    expect(rowNames()).toEqual(['worker-10', 'worker-11'])
    // // Next 下一页按钮应该 disabled
    expect(screen.getByRole('button', { name: 'Next page' })).toBeDisabled()
  })
```

代价就是写一个200行的组件，可能要写400行测试

我们的分页器组件测试：
```javascript
describe("ListPagination", () => {
  it("renders the list summary and navigation controls", () => {
    const markup = renderToStaticMarkup(<ListPagination {...defaultProps} />);

    expect(markup).toContain("64");
    expect(markup).toContain("Page 2 of 4");
    expect(markup).toContain('aria-label="Previous"');
    expect(markup).toContain('aria-label="Next"');
  });

  it("disables navigation at the first and last pages", () => {
    const firstPage = renderToStaticMarkup(<ListPagination {...defaultProps} currentPage={1} />);
    const lastPage = renderToStaticMarkup(<ListPagination {...defaultProps} currentPage={4} />);

    expect(firstPage).toMatch(
      /<button[^>]*(?:aria-label="Previous"[^>]*disabled=""|disabled=""[^>]*aria-label="Previous")/,
    );
    expect(lastPage).toMatch(
      /<button[^>]*(?:aria-label="Next"[^>]*disabled=""|disabled=""[^>]*aria-label="Next")/,
    );
  });

  it("renders nothing when the list is empty", () => {
    const markup = renderToStaticMarkup(<ListPagination {...defaultProps} totalItems={0} />);

    expect(markup).toBe("");
  });
});
```