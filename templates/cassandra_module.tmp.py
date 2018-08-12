
[[[cog
import cog
cog.outl("#!/usr/bin/python")
cog.outl("")
cog.outl("# %s %s <%s>" % (year, author, email))
cog.outl("# %s" % github_url)
]]]
[[[end]]]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

[[[cog
import cog
cog.outl("ANSIBLE_METADATA = %s" % ansible_metadata)
]]]
[[[end]]]

DOCUMENTATION = '''
---
[[[cog
import cog
cog.outl("module: %s" % module_name)
cog.outl("author: \"%s (%s)\"" % (author, email))
cog.outl("version_added: %s" % version_added)
cog.outl("short_description: %s" % short_description)
cog.outl("requirements: [ %s ]" % requirements)
cog.outl("description:")
cog.outl("    - %s" % description)
cog.outl("options: %s" % options)
]]]
[[[end]]]
'''

EXAMPLES = '''
[[[cog
import cog
cog.outl("%s" % examples)
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
            enable=dict(type='bool', required=True),
            nodetool_path=dict(type='str', default=None, required=False),
            debug=dict(type='bool', default=False, required=False),
        ),
        supports_check_mode=True
    )

    [[[cog
        import cog
        cog.outl("status_command = '%s'" % status_command)
        cog.outl("enable_command = '%s'" % enable_command)
        cog.outl("disable_command = '%s'" % disable_command)
    ]]]
    [[[end]]]

    n = NodeTool3PairCommand(module, status_command, enable_command, disable_command)

    rc = None
    out = ''
    err = ''
    result = {}
    changed = False

    (rc, out, err) = n.status_command()

    if module.params['enable'] == False:

        if rc != 0:
            module.fail_json(name=status_command, msg=err)
        if module.check_mode:
            if out == "running":
                module.exit_json(changed=True)
            else:
                module.exit_json(changed=False)
        if out.strip() == "running":
            (rc, out, err) = n.disable_command()
            changed = True
        if rc != 0:
            module.fail_json(name=disable_command, msg=err)

    elif module.params['enable'] == True:

        if rc != 0:
            module.fail_json(name=status_command, msg=err)
        if module.check_mode:
            if out == "not running":
                module.exit_json(changed=True)
            else:
                module.exit_json(changed=False)
        if out.strip() == "not running":
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
