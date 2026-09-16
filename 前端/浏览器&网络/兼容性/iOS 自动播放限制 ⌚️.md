# iOS 自动播放限制 ⌚️
> Last Format Time：9/16/2026 19:24:53

---
## 核心结论
iOS Safari 对媒体自动播放限制比较严格。

### 静音视频
通常允许自动播放：

```tsx
<video
  src="/demo.mp4"
  autoPlay
  muted
  playsInline
  loop
/>
```

关键属性：

- `autoPlay`：尝试自动播放。
    
- `muted`：静音，**iOS 允许自动播放的关键条件**。
    
- `playsInline`：在页面内播放，避免进入全屏。
    
- `loop`：循环播放，可选。
    

可以记成：

```text
autoplay + muted + playsInline
            ↓
      iOS 通常允许自动播放
```

---
## 带声音的媒体不能直接自动播放
例如：

```js
const audio = new Audio('/music.mp3')

audio.play()
```

如果页面加载后直接执行，iOS Safari 很可能拒绝：

```text
NotAllowedError
```

原因是浏览器要求：

> 带声音的媒体播放通常必须由用户操作触发。

所以不能通过单纯调用：

```js
audio.play()
```

绕过 autoplay 限制。

---
## 正确做法：用户交互后播放
把 `play()` 放到点击事件中：

```tsx
const handleStart = async () => {
  const audio = new Audio('/music.mp3')

  try {
    await audio.play()
  } catch (err) {
    console.error(err)
  }
}

<button onClick={handleStart}>
  开始播放
</button>
```

流程：

```text
用户点击
   ↓
click / touch
   ↓
audio.play()
   ↓
浏览器认可为 user activation
   ↓
允许播放
```

这里的 `user activation` 可以理解为：

> 浏览器确认这次播放是用户主动触发的，而不是网页偷偷播放。

---
## 注意异步操作导致用户激活丢失
不推荐：

```js
button.onclick = () => {
  setTimeout(() => {
    audio.play()
  }, 1000)
}
```

也尽量避免：

```js
button.onclick = async () => {
  await fetchSomething()

  audio.play()
}
```

因为 `play()` 和用户点击之间隔了异步任务后，浏览器可能认为：

```text
这次 play()
已经不再属于刚才的用户操作
```

从而继续阻止播放。

最稳妥的是：

```js
button.onclick = () => {
  audio.play()
}
```

即：

> 尽量在用户事件回调中直接调用 `play()`。


# 常见实际方案

---
## 视频自动播放 + 默认静音
```tsx
<video
  src="/demo.mp4"
  autoPlay
  muted
  playsInline
/>
```

这是移动端 Web 最常用的方案。

---
## 用户点击后开启声音
```tsx
function Video() {
  const videoRef = useRef<HTMLVideoElement>(null)

  const enableSound = async () => {
    const video = videoRef.current
    if (!video) return

    video.muted = false

    try {
      await video.play()
    } catch {
      // 播放失败时显示播放按钮等降级 UI
    }
  }

  return (
    <>
      <video
        ref={videoRef}
        src="/demo.mp4"
        autoPlay
        muted
        playsInline
        loop
      />

      <button onClick={enableSound}>
        开启声音
      </button>
    </>
  )
}
```

不要在没有用户操作的情况下直接：

```js
video.muted = false
```

因为 iOS Safari 可能在视频从静音切换为有声时暂停播放。


# 最终心智模型

```text
iOS 媒体自动播放

                    媒体
                     │
          ┌──────────┴──────────┐
          │                     │
        静音                  有声音
          │                     │
autoplay + muted           无用户操作
+ playsInline                  │
          │                    ❌
          ✅                    │
                              用户点击
                                │
                              play()
                                │
                                ✅
```

---
## 一句话记忆

> **iOS 想自动播：先静音；想有声音：让用户点一下。**