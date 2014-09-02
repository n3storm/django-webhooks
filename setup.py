from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name='django-webhook',
    version=VERSION,
    description='Reusable Django app that provides webhooks',
    long_description=open('README.md').read(),
    author='Andrew Cutler',
    author_email='andrew@voltgrid.com',
    url='https://github.com/voltgrid/django-webhook',
    package_dir={'webhook': 'webhook'},
    packages=find_packages(),
    package_data = {
        # If any package contains *.txt etc include
        '': ['*.txt', '*.html', '*.md'],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    install_requires=[
        'Django',
        'django-uuidfield'
    ],
)
