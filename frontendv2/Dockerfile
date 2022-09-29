FROM node:16-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --legacy-peer-deps
COPY ./ ./
RUN chown -R node /app/node_modules
USER node
CMD ["npm", "run", "start"]
