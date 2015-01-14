from setuptools import setup, find_packages

VERSION = '0.0.4'

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("Warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='django-webhooks',
    version=VERSION,
    description='Reusable Django app that provides webhooks',
    long_description=read_md('README.md'),
    author='Andrew Cutler',
    author_email='andrew@voltgrid.com',
    url='https://github.com/voltgrid/django-webhooks',
    package_dir={'webhooks': 'webhooks'},
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
