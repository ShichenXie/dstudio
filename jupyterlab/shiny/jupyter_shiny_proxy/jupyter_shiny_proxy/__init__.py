import os
import tempfile
import getpass
from textwrap import dedent

def setup_shiny():
    '''Manage a Shiny instance.'''

    name = 'shiny'
    def _get_shiny_cmd(port):
        conf = dedent("""
            run_as {user};
            server {{
                listen {port};
                location / {{
                    site_dir {site_dir};
                    log_dir {site_dir}/logs;
                    bookmark_state_dir {site_dir}/bookmarks;
                    directory_index on;
                }}
            }}
        """).format(
            user=getpass.getuser(),
            port=str(port),
            site_dir='/srv/shiny-server'#os.getcwd()
        )

        f = tempfile.NamedTemporaryFile(mode='w', delete=False)
        f.write(conf)
        f.close()
        return ['shiny-server', f.name]

    return {
        'command': _get_shiny_cmd,
        'launcher_entry': {
            'title': 'Shiny',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'shiny.svg')
        }
    }
