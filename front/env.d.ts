/// <reference types="vite/client" />

declare const APP_NAME: string;
declare const APP_VERSION: string;

interface ImportMetaEnv {
  readonly APP_ENV: string // Env
  readonly BASE_API_URL: string // Base API URL
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}