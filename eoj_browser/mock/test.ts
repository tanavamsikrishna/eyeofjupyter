// test.ts

import { MockMethod } from 'vite-plugin-mock'



export default [
    {
        url: '/snapshots',
        method: 'get',
        response: () => {
            return [
                "test/test.ipynb/1700662570.843829",
                "test/test.ipynb/1700662572.585462",
                "test/test.ipynb/1700662570.29712",
                "test/test.ipynb/1700662568.828779",
                "test/test.ipynb/1700825772.119094",
                "test/test.ipynb/1700662569.832397",
                "test/test.ipynb/1700662569.331969"
            ]
        },
    },

] as MockMethod[]
