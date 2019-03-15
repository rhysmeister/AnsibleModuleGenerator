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
module_file = 'templates/1/{0}/{0}.yaml'.format(module_name)
ansible_module = yaml.load(open(module_file, 'r'))
cog.outl("module: %s" % ansible_module['module_name'])
cog.outl("author: \"%s (%s)\"" % (ansible_module['author'], ansible_module['email']))
cog.outl("version_added: %s" % ansible_module['version_added'])
cog.outl("short_description: %s" % ansible_module['short_description'])
cog.outl("requirements: [ %s ]" % ansible_module['requirements'])
cog.outl("description:")
for item in ansible_module['description']:
    cog.outl("\t- {0}".format(item))
module_options = open('templates/1/{0}/{0}_options.yaml'.format(module_name), 'r')
module_options = module_options.read()
cog.out("options: \n%s" % module_options)
]]]
[[[end]]]
'''

EXAMPLES = '''
[[[cog
import cog
module_examples = open('templates/1/{0}/{0}_examples.yaml'.format(module_name), 'r')
module_examples = module_examples.read()
cog.out("%s" % module_examples)
]]]
[[[end]]]
'''

RETURN = '''
[[[cog
import cog
module_return = open('templates/1/{0}/{0}_return.yaml'.format(module_name), 'r')
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

class NodeTool3PairCommand(NodeToolCmd):

    """
    Inherits from the NodeToolCmd class. Adds the following methods;

        - status_command
        - enable_command
        - disable_command
    """

    def __init__(self, module, status_command, enable_command, disable_command):
        self.status_command = status_command
        self.enable_command = enable_command
        self.disable_command = disable_command

    def status_command(self):
        return self.nodetool_cmd(self.status_command)

    def enable_command(self):
        return self.nodetool_cmd(self.enable_command)

    def disable_command(self):
        return self.nodetool_cmd(self.disable_command)

def main():
    module = AnsibleModule(
        argument_spec = dict(
            host=dict(type='str', default='localhost'),
            port=dict(type='int', default=7199),
            password=dict(type='str', no_log=True),
            passwordFile=dict(type='str', no_log=True),
            username=dict(type='str', no_log=True),
            state=dict(required=True, choices=['enabled', 'disabled'])),
            nodetool_path=dict(type='str', default=None, required=False),
            debug=dict(type='bool', default=False, required=False),
        supports_check_mode=True)

    [[[cog
        import cog
        cog.outl("status_command = '%s'" % ansible_module['module_commands']['status'])
        cog.outl("enable_command = '%s'" % ansible_module['module_commands']['enable'])
        cog.outl("disable_command = '%s'" % ansible_module['module_commands']['disable'])
        cog.outl("status_active = '%s'" % ansible_module['status_responses']['active'])
        cog.outl("status_inactive = '%s'" % ansible_module['status_responses']['inactive'])
    ]]]
    [[[end]]]

    n = NodeTool3PairCommand(module, status_command, enable_command, disable_command)

    rc = None
    out = ''
    err = ''
    result = {}
    changed = False

    (rc, out, err) = n.status_command()
    out = out.strip()

    if module.params['state'] == "disabled":

        if rc != 0:
            module.fail_json(name=enable_command, msg=err)
        if module.check_mode:
            if out == status_active:
                module.exit_json(changed=True)
            else:
                module.exit_json(changed=False)
        if out == status_active:
            (rc, out, err) = n.disable_command()
            changed = True
        if rc != 0:
            module.fail_json(name=disable_command, msg=err)

    elif module.params['state'] == "enabled":

        if rc != 0:
            module.fail_json(name=status_command, msg=err)
        if module.check_mode:
            if out == status_inactive:
                module.exit_json(changed=True)
            else:
                module.exit_json(changed=False)
        if out == status_inactive:
            (rc, out, err) = n.enable_command()
            changed = True
        if rc is not None and rc != 0:
            module.fail_json(name=enable_command, msg=err)

    result['changed'] = changed
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err
    module.exit_json(**result)


if __name__ == '__main__':
    main()
