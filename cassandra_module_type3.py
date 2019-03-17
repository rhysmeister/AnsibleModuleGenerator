[[[cog
import cog, yaml
header = yaml.load(open('templates/header.yaml', 'r'))
cog.outl("#!/usr/bin/python")
cog.outl("")
cog.outl("# %s %s <%s>" % (header['year'], header['author'], header['email']))
cog.outl("# %s" % header['github_url'])
]]]
[[[end]]]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type
[[[cog
import cog, yaml
ansible_metadata = yaml.load(open('templates/ansible_metadata.yaml', 'r'))
cog.outl("ANSIBLE_METADATA = { \"metadata_version\": \"%s\", \"status\": \"%s\", \"supported_by\": \"%s\" }" % (ansible_metadata['metadata_version'], ansible_metadata['status'], ansible_metadata['supported_by']))
]]]
[[[end]]]
DOCUMENTATION = '''
---
[[[cog
import cog, yaml
module_file = 'templates/3/{0}/{0}.yaml'.format(module_name)
ansible_module = yaml.load(open(module_file, 'r'))
cog.outl("module: %s" % ansible_module['module_name'])
cog.outl("author: \"%s (%s)\"" % (ansible_module['author'], ansible_module['email']))
cog.outl("version_added: %s" % ansible_module['version_added'])
cog.outl("short_description: %s" % ansible_module['short_description'])
cog.outl("requirements: [ %s ]" % ansible_module['requirements'])
cog.outl("description:")
for item in ansible_module['description']:
    cog.outl("\t- {0}".format(item))
module_options = open('templates/3/{0}/{0}_options.yaml'.format(module_name), 'r')
module_options = module_options.read()
cog.out("options: \n%s" % module_options)
]]]
[[[end]]]
'''

EXAMPLES = '''
[[[cog
import cog
module_examples = open('templates/3/{0}/{0}_examples.yaml'.format(module_name), 'r')
module_examples = module_examples.read()
cog.out("%s" % module_examples)
]]]
[[[end]]]
'''

RETURN = '''
[[[cog
import cog
module_return = open('templates/3/{0}/{0}_return.yaml'.format(module_name), 'r')
module_return = module_return.read()
cog.out("%s" % module_return)
]]]
[[[end]]]
'''

from ansible.module_utils.basic import AnsibleModule, load_platform_subclass

class NodeToolCmd(object):
    """
    This is a generic NodeToolCmd class for building nodetool commands
    """

    def __init__(self, module):
        self.module                 = module
        self.host                   = module.params['host']
        self.port                   = module.params['port']
        self.password               = module.params['password']
        self.passwordFile           = module.params['passwordFile']
        self.username               = module.params['username']
        self.nodetool_path          = module.params['nodetool_path']
        self.debug                  = module.params['debug']

    def execute_command(self, cmd):
        return self.module.run_command(cmd)

    def nodetool_cmd(self, sub_command):
        if self.nodetool_path is not None and not self.nodetool_path.endswith('/'):
            self.nodetool_path += '/'
        cmd = "{0}nodetool --host {1} --port {2}".format(self.nodetool_path,
                                                         self.host,
                                                         self.port)
        if self.username is not None:
            cmd += " --username {0}".format(self.username)
            if self.passwordFile is not None:
                cmd += " --passwordFile {0}".format(self.passwordFile)
            else:
                cmd += " --password '{0}'".format(self.password)
        # The thing we want nodetool to execute
        cmd += " {0}".format(sub_command)
        if self.debug:
            print(cmd)
        return self.execute_command(cmd)

class NodeToolGetSetCommand(NodeToolCmd):

    """
    Inherits from the NodeToolCmd class. Adds the following methods;

        - get_cmd
        - set_cmd
    """

    def __init__(self, module, get_cmd, set_cmd):
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd

    def get_command(self):
        return self.nodetool_cmd(self.get_cmd)

    def set_command(self):
        return self.nodetool_cmd(self.set_cmd)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            host=dict(type='str', default='$(hostname)'),
            port=dict(type='int', default=7199),
            password=dict(type='str', no_log=True),
            passwordFile=dict(type='str', no_log=True),
            username=dict(type='str', no_log=True),
            [[[cog
                import cog
                if ansible_module['module_name'] == "cassandra_compactionthreshold":
                    cog.outl("keyspace=dict(type='str', required=True),")
                    cog.outl("table=dict(type='str', required=True),")
                    cog.outl("min=dict(type='int', required=True),")
                    cog.outl("max=dict(type='int', required=True),")
                else:
                    cog.outl("value=dict(type='float', required=True),")
            ]]]
            [[[end]]]
            nodetool_path=dict(type='str', default=None, required=False),
            debug=dict(type='bool', default=False, required=False),
        ),
        supports_check_mode=True
    )

    [[[cog
        import cog
        cog.outl("get_cmd = '%s'" % ansible_module['module_commands']['get_cmd'])
        if ansible_module['module_name'] == "cassandra_compactionthreshold":
            cog.outl("keyspace = module.params['keyspace']")
            cog.outl("table = module.params['table']")
            cog.outl("min = module.params['min']")
            cog.outl("max = module.params['max']")
            cog.outl("set_cmd = \"{0}".format(ansible_module['module_commands']['set_cmd']) + " {0} {1} {2} {3}\".format(keyspace, table, min, max)")
        else:
            cog.outl("set_cmd = \"{0}".format(ansible_module['module_commands']['set_cmd']) + " {0}\".format(module.params['value'])")

    ]]]
    [[[end]]]

    n = NodeTool3PairCommand(module, get_cmd, set_cmd)

    rc = None
    out = ''
    err = ''
    result = {}
    changed = False

    (rc, out, err) = n.get_command()
    out = out.strip()

    if module.params['value'] == out:

        if rc != 0:
            module.fail_json(name=get_command, msg=err)
        changed = False
    else:

        if module.check_mode:
            changed = True
        else:
            (rc, out, err) = n.set_command()
            out = out.strip()
            if rc != 0:
                module.fail_json(name=set_command, msg=err)
            changed = True

    result['changed'] = changed
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err
    module.exit_json(**result)


if __name__ == '__main__':
    main()
