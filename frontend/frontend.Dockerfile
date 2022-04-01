FROM node:16-alpine3.14
WORKDIR /frontend
RUN npm install -g npm@8.6.0
RUN npm install -g @vue/cli
CMD [ "sh", "start.sh" ]
