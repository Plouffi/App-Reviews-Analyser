/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_IS_MOCK: boolean
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

VITE_IS_MOCK=false