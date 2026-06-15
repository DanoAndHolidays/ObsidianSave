# useQuery
> Last Format Time：6/15/2026 10:50:12

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