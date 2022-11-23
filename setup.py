#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    requirements = [req.replace('==', '>=') for req in requirements]


setuptools.setup(
    name='pollination-honeybee-display',
    author='ladybug-tools',
    author_email='info@ladybug.tools',
    maintainer='chris, ladybug-tools',
    maintainer_email='chris@ladybug.tools, info@ladybug.tools',
    packages=setuptools.find_namespace_packages(
        include=['pollination.*'], exclude=['tests', '.github']
    ),
    install_requires=requirements,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url='https://github.com/pollination/honeybee-display',
    project_urls={
        'icon': 'https://raw.githubusercontent.com/ladybug-tools/artwork/master/icons_bugs/grasshopper_tabs/Honeybee.png',
        'docker': 'https://hub.docker.com/r/ladybugtools/honeybee-display'
    },
    description='Plugin for Pollination with all honeybee extensions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='honeybee, display, vtk, ladybug-tools',
    license='PolyForm Shield License 1.0.0, https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt',
    zip_safe=False
)
