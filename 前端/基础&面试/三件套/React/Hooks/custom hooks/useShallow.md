# useShallow
> Last Format Time：9/16/2026 19:24:51

这时zustande的[源码](https://github.com/pmndrs/zustand/blob/main/src/react/shallow.ts)，就这么几行：
```ts
import React from 'react'
import { shallow } from '../vanilla/shallow.ts'

export function useShallow<S, U>(selector: (state: S) => U): (state: S) => U {
  const prev = React.useRef<U>(undefined)
  return (state) => {
    const next = selector(state)
    return shallow(prev.current, next)
      ? (prev.current as U)
      : (prev.current = next)
  }
}
```

