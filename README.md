# AnsibleModuleGenerator
Generate python code for Cassandra Ansible modules using cog


cog.py -d -D module_name="cassandra_backup" -o generated_modules/cassandra_backup.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_binary" -o generated_modules/cassandra_binary.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_gossip" -o generated_modules/cassandra_gossip.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_handoff" -o generated_modules/cassandra_handoff.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_thrift" -o generated_modules/cassandra_thrift.py cassandra_module_type1.py
