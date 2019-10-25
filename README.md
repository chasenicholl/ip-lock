# ip-lock

A Python Utility for updating your DNS provider with your dynamic public IP.

### Supported DNS Providers
- CloudFlare
- ...more to come


### Installation

```shell
curl -sSL https://raw.githubusercontent.com/chasenicholl/ip-lock/master/install.sh | bash
```


### Config File

You can use the `config-sample.yml` as a template, but remember to fill in with your own credentials. 


### API Permissions

The Cloudflare Auth Token will need Zone and DNS permissions.


### Usage

```shell
ip_lock path/to/your/config.yml (--verbose --force --dry-run)
```

### Usage as a cronjob

I recommend installing this as a cronjob, or some form of system scheduled task.

```shell
crontab -e
```

Add this line to your crontab, to check every minute for a Public IP address change.

```crontab
*/1 * * * * /usr/local/bin/ip_lock /absolute/path/to/your/config.yml (--verbose --force --dry-run) >> /var/log/ip_lock.log 2>&1
```