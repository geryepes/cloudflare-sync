import logging
import urllib.request
from dataclasses import dataclass, field

from CloudFlare import CloudFlare

logger = logging.getLogger(__package__)

class ZoneDoesNotExis(Exception):
    pass

class DnsRecordDoesNotExist(Exception):
    pass

def get_cf_client(email: str, token: str) -> CloudFlare:
    '''
    Returns a CloudFlare client and the zone id to use in future commands
    '''
    return CloudFlare(email, token, use_sessions=False)

def get_external_ip():
    return urllib.request.urlopen('https://ident.me').read().decode('utf8')


@dataclass
class DnsRecord:
    name: str
    type: str
    proxied: bool
    zone_name: str
    content: str = ''
    zone_id: str = field(repr=False, default='')
    id: str = field(repr=False, default='')

    @property
    def record(self):
        return {
            'name': self.name,
            'type': self.type,
            'content': self.content,
            'proxied': self.proxied
        }


class DnsRecordManager():
    def __init__(self, cf: CloudFlare, dns_record: DnsRecord, external_ip: str) -> None:
        self.cf = cf
        self.dns_record = dns_record
        self.external_ip = external_ip
        if not self.dns_record.id:
            self._initialize()


    def _initialize(self):
        logger.info('Initializing: %s', self.dns_record)
        self.dns_record.zone_id = self._get_zone_id()
        try:
            self.dns_record.id = self._get_id()
        except DnsRecordDoesNotExist:
            self.dns_record.content = self.external_ip
            record = self.cf.zones.dns_records.post(
                self.dns_record.zone_id, data=self.dns_record.record
                )
            self.dns_record.id = record['id']
        else:
            self.dns_record.content = self._get_content()

    def _get_zone_id(self):
        try:
            return self.cf.zones.get(params={'name': self.dns_record.zone_name})[0]['id']
        except IndexError:
            raise ZoneDoesNotExis from IndexError

    def _get_id(self):
        try:
            return self.cf.zones.dns_records.get(
                self.dns_record.zone_id, params={
                    'name': f'{self.dns_record.name}.{self.dns_record.zone_name}'}
                )[0]['id']
        except IndexError:
            raise DnsRecordDoesNotExist from IndexError

    def _get_content(self):
        try:
            return self.cf.zones.dns_records.get(
                self.dns_record.zone_id, params={
                    'name': f'{self.dns_record.name}.{self.dns_record.zone_name}'
                    }
                )[0]['content']
        except IndexError:
            raise DnsRecordDoesNotExist from IndexError

    def update(self):
        self.dns_record.content = self.external_ip
        self.cf.zones.dns_records.put(
            self.dns_record.zone_id,
            self.dns_record.id,
            data=self.dns_record.record
            )
        logger.info('Updated: %s', self.dns_record)

    def should_update(self):
        return self.external_ip != self.dns_record.content
