// test.ts
import { MockMethod } from "vite-plugin-mock";

export default [
  {
    url: "/list/files",
    method: "get",
    response: () => {
      return [
        "test/test.ipynb/1700662570.843829",
        "test/test.ipynb/1700662572.585462"
      ];
    },
  },
  {
    url: "/list/versions/test/test.ipynb/1700662570.843829",
    method: "get",
    response: () => {
      return [{ file_name: "1700662568.828779" }, { file_name: "1700662569.331969" }];
    },
  }
] as MockMethod[];
