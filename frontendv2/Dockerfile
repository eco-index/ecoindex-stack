FROM node:16-alpine
WORKDIR /app
COPY package.json ./
COPY ./ ./
RUN npm i --legacy-peer-deps
CMD ["npm", "run", "start"]