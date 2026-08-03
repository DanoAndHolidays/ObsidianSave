# useQuery
> Last Format Time：7/14/2026 20:22:22

[https://www.robinwieruch.de/react-hooks-fetch-data/](https://www.robinwieruch.de/react-hooks-fetch-data/)

---
## case
在一个组件中使用自定义hooks可以将逻辑抽离，以便维护复用。具体来说就是返回一个数组，其中包括但不限于返回state与handler。

```tsx
const App = () => {
  const [data, setData] = useState<Story[]>([]);
  const [search, setSearch] = useState("");
  const [activeSearch, setActiveSearch] = useState("react");

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(`${API}?query=${activeSearch}`);

      setData(result.data.hits);
    };

    fetchData();
  }, [activeSearch]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  };

  const handleSearchSubmit = () => {
    setActiveSearch(search);
    setSearch("");
  };

  return (
    <>
      <input type="text" value={search} onChange={handleSearchChange} />
      <button type="button" onClick={handleSearchSubmit}>
        Search
      </button>

      <ul>...</ul>
    </>
  );
};
```

---
## best practice
这里面的queryKey其实在useEffect中根本没有被使用，但是依旧被作为依赖添加进去了，只要queryKey发生了变化，那么就会触发副作用去获取信息：
```tsx
type UseQueryArgs<T> = {
  queryKey: string[];
  queryFn: () => Promise<T>;
  initialData: T;
};

const useQuery = <T>({ queryFn, queryKey, initialData }: UseQueryArgs<T>) => {
  const [data, setData] = useState<T>(initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);

      try {
        const result = await queryFn();

        setData(result);
      } catch (error) {
        setIsError(true);
      }

      setIsLoading(false);
    };

    fetchData();
  }, [...queryKey]);

  return { data, isLoading, isError };
};
```

具体的使用例子：
```ts
import { useQuery } from "@tanstack/react-query";
import { trpcClient } from "@/integrations/trpc/client";

export const useStatsOverview = () =>
  useQuery({
    queryKey: ["stats", "overview"],
    queryFn: () => trpcClient.stats.overview.query(),
  });

export const useStatsAcceptance = () =>
  useQuery({
    queryKey: ["stats", "acceptance"],
    queryFn: () => trpcClient.stats.acceptance.query(),
  });

export const useStatsTrends = () =>
  useQuery({
    queryKey: ["stats", "trends"],
    queryFn: () => trpcClient.stats.trends.query(),
  });

export const useStatsByCategory = () =>
  useQuery({
    queryKey: ["stats", "byCategory"],
    queryFn: () => trpcClient.stats.byCategory.query(),
  });
```

这里可以看到，我们使用的所有数据都是从trpcClient这里拿到的，不同的客户端之间具有不同的路由
```ts
import { useQuery } from "@tanstack/react-query";
import { trpcClient } from "@/integrations/trpc/client";

export const useGithubTree = (owner: string, repo: string, branch: string = "main") =>
  useQuery({
    queryKey: ["github", "repo", "tree", owner, repo, branch],
    queryFn: () => trpcClient.github.repo.tree.query({ owner, repo, branch }),
    enabled: owner.length > 0 && repo.length > 0,
    staleTime: 5 * 60 * 1000,
  });
```