openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
  -days 365 -nodes -keyout localhost.key -out localhost.crt \
  -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost"
