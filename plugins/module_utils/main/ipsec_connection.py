from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Connection(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_connection',
        'del': 'del_connection',
        'set': 'set_connection',
        'search': 'get',
        'toggle': 'toggle_connection',
    }
    API_KEY_PATH = 'swanctl.Connections.Connection'
    API_KEY_PATH_REQ = 'connection'
    API_MOD = 'ipsec'
    API_CONT = 'connections'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'local_addresses', 'remote_addresses', 'pools', 'proposals', 'unique',
        'aggressive', 'version', 'mobike', 'encapsulation', 'reauth_seconds',
        'rekey_seconds', 'over_seconds', 'dpd_delay_seconds', 'dpd_timeout_seconds',
        'send_certificate_request', 'send_certificate', 'keying_tries',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'encapsulation': 'encap',
        'local_addresses': 'local_addrs',
        'remote_addresses': 'remote_addrs',
        'reauth_seconds': 'reauth_time',
        'rekey_seconds': 'rekey_time',
        'over_seconds': 'over_time',
        'dpd_delay_seconds': 'dpd_delay',
        'dpd_timeout_seconds': 'dpd_timeout',
        'send_certificate_request': 'send_certreq',
        'send_certificate': 'send_cert',
        'keying_tries': 'keyingtries',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'aggressive', 'mobike', 'encapsulation', 'send_certificate_request'],
        'list': ['local_addresses', 'remote_addresses', 'pools', 'proposals'],
        'select': ['send_certificate', 'unique'],
        'select_opt_list': ['version'],  # don't know why this is a list instead of a dict
        'int': [
            'keying_tries', 'dpd_timeout_seconds', 'dpd_delay_seconds', 'over_seconds',
            'rekey_seconds', 'reauth_seconds',
        ],
    }
    FIELDS_VALUE_MAPPING = {
        'version': {
            'IKEv1+IKEv2': 0,
            'IKEv1': 1,
            'IKEv2': 2,
        }
    }
    INT_VALIDATIONS = {
        'keying_tries': {'min': 0, 'max': 1000},
        'dpd_timeout_seconds': {'min': 0, 'max': 500000},
        'dpd_delay_seconds': {'min': 0, 'max': 500000},
        'over_seconds': {'min': 0, 'max': 500000},
        'rekey_seconds': {'min': 0, 'max': 500000},
        'reauth_seconds': {'min': 0, 'max': 500000},
    }
    EXIST_ATTR = 'tunnel'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.tunnel = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
