import setuptools

setuptools.setup(
    name='pyyarl',
    version='1.0.0',
    url='https://github.com/jeremyephron/pyyarl',
    author='Jeremy Ephron',
    author_email='jeremye@cs.stanford.edu',
    description='Yet Another Rate Limiter (for Python)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
)
