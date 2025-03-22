from fabric import task, Connection
from invoke.context import Context


@task
def deploy(c):
    source_name = 'pmm_appdx_47'
    archive_name = f'{source_name}.tar.gz'
    local_ctx = Context(c.config)
    with local_ctx.cd(f'../{source_name}'):
        local_ctx.run('git pull')
    with local_ctx.cd('..'):
        local_ctx.run(f'tar -czvf {archive_name} {source_name}')
    cn = Connection(
        host=c.host,  # Uses the host from the CLI
        user="crchemist",

        connect_kwargs={"key_filename": '/Users/crchemist/.ssh/id_rsa_gh',
                        "allow_agent": False,
                        "look_for_keys": False},
    )
    cn.put(f'/Users/crchemist/development/{archive_name}', f'/home/crchemist/data/{archive_name}')
    with cn.cd('~/data'):
        cn.run(f'tar -xzvf {archive_name}')
        cn.run(f'rm {archive_name}')
    with cn.cd(source_name):
        cn.run('git pull')
