import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import css from "rollup-plugin-import-css";
import terser from '@rollup/plugin-terser'; //  plugin to generate a minified bundle with terser


export default [
    {
        input: 'src\\telegram\\static\\telegram\\_js\\highlight\\json.js',
        plugins: [
            nodeResolve(),
            commonjs(),
            css({
                inject: true,
            })
        ],
        output: {
            format: 'es',
            file: 'src\\telegram\\static\\telegram\\_js\\highlight\\json.min.js',
            plugins: [terser()]
        },
    }
]