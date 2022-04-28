FROM node:16-alpine
WORKDIR /app
COPY package.json ./
COPY ./ ./
RUN npm i
CMD ["npm", "run", "start"]