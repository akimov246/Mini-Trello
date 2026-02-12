FROM nginx:alpine3.23-slim
COPY localhost.crt /etc/ssl/certs/
COPY localhost.key /etc/ssl/private/
COPY default.conf /etc/nginx/conf.d/default.conf
COPY 404.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]