import os
from string import Template

plugin_name=input('Select a name for the plugin: ')
plugin_priority=input('Which priority should this plugin have? (default: 0) ')
plugin_allow_others=input('Should this plugin block other plugins from running? [y/N] ')

if not plugin_priority:
    plugin_priority = 0

plugin_allow_others = 'y' == plugin_allow_others or \
    'Y' == plugin_allow_others or \
    'yes' == plugin_allow_others or \
    'YES' == plugin_allow_others or \
    'Yes' == plugin_allow_others

if plugin_allow_others:
    plugin_allow_others = 'True'
else:
    plugin_allow_others = 'False'

with open('plugin.template', 'r') as plugin_template:
    plugin_template = ''.join(plugin_template.readlines()) + '\n\n'
    template = Template(plugin_template)
    plugin = template.substitute(dict(
        name=plugin_name,
        priority=plugin_priority,
        allow_others=plugin_allow_others
    ))

    os.mkdir('plugins/{0}' . format(plugin_name))
    with open('plugins/{0}/main.py' . format(plugin_name), 'w+') as plugin_file:
        plugin_file.write(plugin)
        plugin_file.close()
    with open('plugins/{0}/requirements.txt' . format(plugin_name), 'w+') as requirements_file:
        requirements_file.write(
            '# specify your required packages here, one per line\n' + \
            '# lines starting with # will be ignored\n'
        )
        requirements_file.close()
