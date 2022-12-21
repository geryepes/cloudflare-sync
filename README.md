# DNS zone Cloudflare Sync 

### The goal of this project is to have a set of DNS records from a Cloudflare DNS zone  in sync with the public IP address obtained by querying the url https://ident.me

## Service configuration
Edit the file `/etc/cloudflare-sync/config.ini` to configure the service.

Contente example
```
[DEFAULT]
SyncIntervalSeconds = 300
#Cloudflare API credentials
email = email@gmail.com
token = 123456789123456789

# DNS record name: foo.domain.com.ar
[foo] 
zone_name = domain.com.ar
type = A # Record type
proxied = True # If proxied by Cloudflare?

[bar]
zone_name = devops.net.ar
type = A
proxied = False
```

Aply the config by restarting the service
```
systemctl restart cloudflare-sync.service
```

In this example the dns records `foo.domain.com.ar` and `bar.domain.com.ar` will be configured in Cloudflare with our public IP address