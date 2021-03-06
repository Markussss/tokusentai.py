import os
import importlib.util as util

def create_plugins():
    # delete previous plugins file and create a new
    if os.path.exists('./plugins.py'):
        print('Removing plugins.py...')
        os.remove('./plugins.py')

    plugins = '# this is an autogenerated file\n\n'

    if not os.path.exists('./plugins'):
        os.mkdir('plugins')

    dependencies = list()
    for plugin_folder in os.listdir('plugins'):
        with open('./plugins/{0}/main.py' . format(plugin_folder)) as plugin:
            plugins = plugins + ''.join(plugin.readlines()) + '\n\n'
        with open('./plugins/{0}/requirements.txt' . format(plugin_folder)) as requirements:
            dependencies = dependencies + requirements.readlines()

    dependencies = list(filter(lambda line: not line.startswith('#'), dependencies))
    install_dependencies(dependencies)

    with open('./plugins.py', 'w+') as plugins_file:
        plugins_file.write(plugins)
        plugins_file.close()

def install_dependencies(modules):
    missing_dependencies = list()
    for module in modules:
        module = module.strip()
        found = util.find_spec(module) is not None
        if not found:
            missing_dependencies.append(module)

    if len(missing_dependencies) > 0:
        install_command = 'pipenv install {0}' . format(' '.join(missing_dependencies))
        try:
            os.system(install_command)
        except:
            print(
                'Run the following command:\n\n{0}' . format(install_command)
            )
        print('Installed missing dependencies, please start the bot again')
        exit()

def run():
    from tokusentai import Tokusentai

    bot = Tokusentai()
    bot.run(os.getenv('TOKEN'))
