import { useRouter } from "next/router";

function useQuery() {
  const router = useRouter();
  const { query } = router;

  return query;
}
