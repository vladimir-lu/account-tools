from setuptools import setup, find_packages

setup(name='account-tools',
      version='0.0.1',
      description='Tools for dealing with statements from different bank account providers',
      url='https://github.com/vladimir-lu/account-tools',
      author='Vladimir Lushnikov',
      license='BSD-3',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Office/Business :: Financial :: Accounting'
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      entry_points={
          'console_scripts': ['stmt2=account_tools.stmt2:main'],
      },
      install_requires=[
          'docopt >= 0.6',
      ],
      tests_require=[
          'nose >= 1.2',
      ]
      )
