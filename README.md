# AnsibleModuleGenerator
Generate python code for Cassandra Ansible modules using jinja2


cog.py -D year=2018 -D author="Rhys Campbell" -D email="rhys.campbell@googlemail.com" -D github_url=http://github.com/rhysmeister \
        -D ansible_metadata="{ metadata: \"value\" }" -D module_name=cassandra_backup -D version_added=2.2.2 \
        -D short_description="short text" -D requirements="Blah" -D description="ABCDEFG" -D options="option1: Blah blah" \
        -D examples="example1" -D status_command="statusbackup" -D enable_command="enablebackup" -D disable_command="disablebackup"
        -d -o cassandra_backup.py
