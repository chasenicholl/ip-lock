"""YAML Cloudflare Config Parser."""

import os

import requests
import yaml

from ip_lock.exceptions import DNSZoneNameNotFound, DNSRecordsError, InvalidAuthToken
from ip_lock.log import get_logger
from ip_lock.ip import public_ip_address


class Cloudflare:
    """Converts YAML file into Cloudflare Config Object
    """

    def __init__(self, user_config):
        loglevel = "DEBUG" if user_config.verbose else os.getenv("LOGLEVEL", None)
        self.logger = get_logger("ip_lock.Cloudflare", loglevel=loglevel)

        config_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "cloudflare.yml"
        )
        with open(config_path) as f:
            self.__dict__.update(yaml.safe_load(f))
        self.__dict__.update(user_config.__dict__)
        self._update_headers()
        self._validate_auth_token()
        self.__dict__.update({"public_ip_address": public_ip_address()})

    def _update_headers(self):
        """Update headers dictionary with user defined values
        """
        headers = {
            "Authorization": f'{self.headers["Authorization"]}{self.auth_token}',
            # "X-Auth-Key": self.auth_token,
            "X-Auth-Email": self.auth_email,
            "Content-Type": "application/json",
        }
        self.headers = headers

    def _validate_auth_token(self):
        """Validate CloudFlare Token
        """
        url = "{}/user/tokens/verify".format(self.base_api_uri)
        res = requests.get(url, headers=self.headers).json()
        if not res["success"]:
            raise InvalidAuthToken(f"Invalid Auth Token: {self.auth_token}\n" f"{res}")

    def find_zone_id_by_name(self):
        """Find your Zone ID by DNS name
        """
        url = "{}/zones?name={}".format(self.base_api_uri, self.dns_zone_name)
        response = requests.get(url, headers=self.headers)
        if response and response.status_code == 200:
            result = response.json()["result"]
            return result[0]["id"]
        raise DNSZoneNameNotFound(f'DNS Zone Name: "{self.dns_zone_name}" ' "not found")

    def list_dns_records(self):
        """List DNS records for CloudFlare Zone

        GET /zones/:zone_identifier/dns_records
        """
        url = "{}/zones/{}/dns_records?".format(self.base_api_uri, self.dns_zone_id)
        if hasattr(self, "dns_record_type") and self.dns_record_type:
            url = f"{url}type={self.dns_record_type}"
        response = requests.get(url, headers=self.headers)
        if response and response.status_code == 200:
            return response.json()["result"]
        raise DNSRecordsError(
            f"Response Code: {response.status_code} \n",
            f"Response Body: {response.json()}",
        )

    def should_update_records(self, records):
        """Determine if public IP has changed
        """
        for record in records:
            if record["content"] != self.public_ip_address:
                return True
        return False

    def reduce_to_targets(self, records):
        """Reduce DNS records to self.target_zone_names
        """
        targets = []
        for record in records:
            if record["name"] in self.target_zone_names:
                targets.append(record)
        return targets

    def update_dns_record(self, record):
        """Update DNS Record IP Address
        """
        url = "{}/zones/{}/dns_records/{}".format(
            self.base_api_uri, self.dns_zone_id, record["id"]
        )
        payload = {
            "type": record["type"],
            "name": record["name"],
            "content": self.public_ip_address,
        }
        self.logger.debug("{} {}".format("PUT", url))
        self.logger.debug(payload)
        if self.dry_run:
            self.logger.debug("Dry run, not actually sending request.")
            return True
        return requests.put(url, json=payload, headers=self.headers).json()["success"]

    def update(self):
        """Update DNS records (if we need too)
        """
        self.dns_zone_id = self.find_zone_id_by_name()
        records = self.reduce_to_targets(self.list_dns_records())
        if not self.force and not self.should_update_records(records):
            self.logger.debug(
                "Public IP address matches DNS " "records, no update needed."
            )
            return

        if not self.force:
            self.logger.debug("Public IP address changed! Updating DNS Records...")
        else:
            self.logger.debug("Forcing update of DNS Records...")
        self.logger.debug(
            "{} --> {}".format(records[0]["content"], self.public_ip_address)
        )

        self.logger.debug("")
        self.logger.debug("Updating {} records...".format(len(records)))
        for record in records:
            if not self.force and record["content"] == self.public_ip_address:
                continue
            self.logger.debug("")
            self.logger.debug("Updating: {}...".format(record["name"]))
            if self.update_dns_record(record):
                self.logger.debug("Update Successful.")
                continue
            self.logger.debug("Update Failed.")
        self.logger.debug("")
        self.logger.debug("Complete.")
