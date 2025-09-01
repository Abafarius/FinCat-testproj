# ---------- Build stage ----------
FROM node:20-alpine AS build
WORKDIR /app

# Сначала манифесты — ускоряет кеширование
COPY app/package*.json ./
RUN npm ci || npm install

# Затем исходники
COPY app .

# Собираем (SSR отключён, но Nitro всё равно нужен для SPA)
RUN npm run build

# ---------- Runtime ----------
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

COPY --from=build /app/.output ./.output

EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
