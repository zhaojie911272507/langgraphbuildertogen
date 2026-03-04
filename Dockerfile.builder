# LangGraph Builder - 可视化设计前端
FROM node:20-alpine AS builder

WORKDIR /app

# 安装依赖
COPY langgraphbuilder/package.json langgraphbuilder/yarn.lock* ./
RUN yarn install --frozen-lockfile

# 复制源码并构建
COPY langgraphbuilder/ .
RUN yarn build

# 生产阶段
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# 复制构建产物
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
