FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run prepare

EXPOSE 5173

CMD ["npm", "run", "dev"]