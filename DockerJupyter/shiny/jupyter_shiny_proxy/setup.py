import setuptools

setuptools.setup(
    name="jupyter-shiny-proxy",
    version='1.1',
    url="https://github.com/ryanlovett/jupyter-shiny-proxy",
    author="Ryan Lovett & Yuvi Panda",
    description="Jupyter extension to proxy Shiny Server",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'shiny = jupyter_shiny_proxy:setup_shiny'
        ]
    },
    package_data={
        'jupyter_shiny_proxy': ['icons/shiny.svg'],
    },
)
