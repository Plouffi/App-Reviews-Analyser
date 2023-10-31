/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_IS_MOCK: boolean // Flag to get Mocked data
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

VITE_IS_MOCK=false
declare const VITE_APP_NAME: string;
declare const VITE_APP_VERSION: string;