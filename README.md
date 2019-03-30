# AnsibleModuleGenerator
Generate python code for Cassandra Ansible modules using cog

==Type 1==

cog.py -d -D module_name="cassandra_backup" -o generated_modules/cassandra_backup.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_binary" -o generated_modules/cassandra_binary.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_gossip" -o generated_modules/cassandra_gossip.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_handoff" -o generated_modules/cassandra_handoff.py cassandra_module_type1.py
cog.py -d -D module_name="cassandra_thrift" -o generated_modules/cassandra_thrift.py cassandra_module_type1.py

==Type 2==

cog.py -d -D module_name="cassandra_autocompaction" -o generated_modules/cassandra_autocompaction.py cassandra_module_type2.py

==Type 3==

cog.py -d -D module_name="cassandra_compactionthreshold" -o generated_modules/cassandra_compactionthreshold.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_compactionthroughput" -o generated_modules/cassandra_compactionthroughput.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_interdcstreamthroughput" -o generated_modules/cassandra_interdcstreamthroughput.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_streamthroughput" -o generated_modules/cassandra_interdcstreamthroughput.py cassandra_module_type3.py
cog.py -d -D module_name="cassandra_traceprobability" -o generated_modules/cassandra_traceprobability.py cassandra_module_type3.py

# Copy generated modules to ansible git repo from this project's root...
cp generated_modules/*.py ../ansible/lib/ansible/modules/database/cassandra/
