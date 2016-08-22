#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.commands.parameters import (
    get_resource_name_completion_list,
    get_enum_choices,
    get_enum_type_completion_list,
    name_type)
from azure.cli.commands import register_cli_argument
import azure.cli.commands.arm # pylint: disable=unused-import
from azure.mgmt.redis.models.redis_management_client_enums import (
    RebootType,
    RedisKeyType,
    SkuFamily,
    SkuName)

from azure.mgmt.redis.models import (
    ScheduleEntry,
)

class JsonString(dict):

    def __init__(self, value):
        super(JsonString, self).__init__()
        import json
        if value[0] in ("'", '"') and value[-1] == value[0]:
            # Remove leading and trailing quotes for dos/cmd.exe users
            value = value[1:-1]
        dictval = json.loads(value)
        self.update(dictval)

class ScheduleEntryList(list):
    def __init__(self, value):
        super(ScheduleEntryList, self).__init__()
        import json
        if value[0] in ("'", '"') and value[-1] == value[0]:
            # Remove leading and trailing quotes for dos/cmd.exe users
            value = value[1:-1]
        dictval = json.loads(value)
        self.extend([ScheduleEntry(
            row['dayOfWeek'],
            int(row['startHourUtc']),
            row.get('maintenanceWindow', None))
                     for row in dictval])

register_cli_argument('redis', 'name', arg_type=name_type, completer=get_resource_name_completion_list('Microsoft.Cache/redis'), id_part='name')
register_cli_argument('redis', 'redis_configuration', type=JsonString)
register_cli_argument('redis', 'reboot_type', completer=get_enum_type_completion_list(RebootType))
register_cli_argument('redis', 'key_type', choices=[e.value for e in RedisKeyType])
register_cli_argument('redis', 'shard_id', type=int)
register_cli_argument('redis import-method', 'files', nargs='+')

register_cli_argument('redis patch-schedule set', 'schedule_entries', type=ScheduleEntryList)


register_cli_argument('redis create', 'name', arg_type=name_type, completer=None)
register_cli_argument('redis create', 'sku_name', choices=[c.lower() for c in get_enum_choices(SkuName)], type=str.lower)
register_cli_argument('redis create', 'sku_family', choices=[c.lower() for c in get_enum_choices(SkuFamily)], type=str.lower)
register_cli_argument('redis create', 'sku_capacity', choices=[str(n) for n in range(0, 7)])
register_cli_argument('redis create', 'enable_non_ssl_port', action='store_true')
register_cli_argument('redis create', 'tenant_settings', type=JsonString)
register_cli_argument('redis create', 'shard_count', type=int)
register_cli_argument('redis create', 'subnet_id') # TODO: Create generic id completer similar to name
