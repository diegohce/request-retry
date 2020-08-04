from setuptools import setup, find_packages

install_requires = []

with open("requirements.txt") as f:
    for l in f.readlines():
        while l.endswith('\n'):
            l = l[:-1]
        if l == '':
            continue
        install_requires.append(l)

setup(name='rerequest',
    version='0.1.0',
    description='requests wrapper',
    url='http://10.54.130.13/core/rerequest',
    author='Diego Cena',
    author_email='dhcena@kiusys.com',
    packages=find_packages(),
    zip_safe=False,
#    package_data={'':['schemas/*.json']},
    install_requires=install_requires)

