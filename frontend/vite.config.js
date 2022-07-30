import { fileURLToPath, URL } from 'url'

import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'
import { createHtmlPlugin } from "vite-plugin-html";


// https://vitejs.dev/config/
export default ({ mode }) => {

  const env = loadEnv(mode, process.cwd())

  return defineConfig({
    plugins: [
      vue(),
      createHtmlPlugin({
        minify: true,
        inject: {
          data: {
            API_KEY: env.VITE_API_KEY
          }
        }
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      port: 8080,
      origin: 'http://localhost:8080',
      host: true,
    },
  })
}
