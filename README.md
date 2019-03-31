# AnsibleModuleGenerator
Generate python code for Cassandra Ansible modules using cog

==Type 1==

```
cog.py -d -D module_name="cassandra_backup" -o generated_modules/cassandra_backup.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_binary" -o generated_modules/cassandra_binary.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_gossip" -o generated_modules/cassandra_gossip.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_handoff" -o generated_modules/cassandra_handoff.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_thrift" -o generated_modules/cassandra_thrift.py cassandra_module_type1.py
```

==Type 2==

```
cog.py -d -D module_name="cassandra_autocompaction" -o generated_modules/cassandra_autocompaction.py cassandra_module_type2.py
```

==Type 3==

```
cog.py -d -D module_name="cassandra_compactionthreshold" -o generated_modules/cassandra_compactionthreshold.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_compactionthroughput" -o generated_modules/cassandra_compactionthroughput.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_interdcstreamthroughput" -o generated_modules/cassandra_interdcstreamthroughput.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_streamthroughput" -o generated_modules/cassandra_streamthroughput.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_traceprobability" -o generated_modules/cassandra_traceprobability.py cassandra_module_type3.py
```

==Copy generated modules to ansible git repo from this project's root...==

```
cp generated_modules/*.py ../ansible/lib/ansible/modules/database/cassandra/
```

==Creating a new module==

* Create new folder in module type folder 1, 2 or 3 (appropriate to cassandra_module_typeN.py python script)
* Create 4 required yaml files...
** <module_name>_examples.yaml - Ansible documentation examples.
** <module_name>_options.yaml - Ansible documentation options.
** <module_name>_return.yaml - Ansible return documentation string.
** <module_name>.yaml - Yaml document that specifies the module. See below...

module_name: Name of module to generate. Generally in the form cassandra_<function>.
author: Author of module.
email: Email of author.
version_added: Ansible version the module was first added to. (string)
short_description: Short description of module. (string)
requirements: Requirements of module.
description: Longer description of module. (list of strings)
options: module option documentation. (redundant?)
module_commands: Dictionary containing sub-keys strings for each type of module.

  type 1 - status, enable, disable subkeys.
  type 2 - enable, disable
  type 3 - get_cmd, set_cmd

status_responses: Possible status responses from commands

  type 1 - active, inactive
  type 2 - Not relevant? Confirm
  type 3 - Renamed (see below)

status_response: Status response for type 3 module command. String
documentation_template: (redundant?)
custom_documentation_template: (redundant?)
module_type: Distinct from the main module type. Internal to type3 modules. Specifies module options...

  keyspace_table_min_max - Add keyspace (string), table (string), min (int) and max(int) options.
  value_int - Add value (int) option.
  value_float - Add value (float) option.
