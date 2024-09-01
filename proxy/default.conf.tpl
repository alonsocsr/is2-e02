server {
  listen ${LISTEN_PORT};

  location /static {
    alias /staticfiles/;
  }

  location /media {
    alias /uploads/;
  }

  location / {
    proxy_pass http://${APP_HOST}:${APP_PORT};
    include /etc/nginx/proxy_params;
  }
}