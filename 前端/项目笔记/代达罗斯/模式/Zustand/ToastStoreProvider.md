# ToastStoreProvider

[[useContext]]

---
## 



```tsx
import { type ReactNode, useState } from "react";
import { ToastStoreContext, createToastStore } from "./toastStore";

export const ToastStoreProvider = ({ children }: { children: ReactNode }) => {
  // 一般是还会有个setter被解构出来的
  const [store] = useState(() => createToastStore());

  return (<ToastStoreContext.Provider value={store}>
	  {children}
  </ToastStoreContext.Provider>)
};

```