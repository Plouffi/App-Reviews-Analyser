/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_IS_MOCK: boolean // Flag to get Mocked data
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

VITE_IS_MOCK=false