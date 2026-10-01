# HTTPS deployment

Set `DOMAIN` to the public hostname and `LETSENCRYPT_EMAIL` to an address for certificate expiry notices in `.env`. Point the hostname's DNS A/AAAA records at this server and allow inbound TCP ports 80 and 443.

Issue the first certificate before starting the full stack. Stop any service currently using port 80, then run:

```sh
docker compose run --rm --no-deps --service-ports certbot-init
docker compose up -d
```

Nginx redirects HTTP to HTTPS while leaving the ACME challenge path available. The Certbot service renews certificates every 12 hours and reloads Nginx when a renewal succeeds. The Django app is only reachable by the other Compose services; public traffic enters through Nginx on ports 80 and 443.
