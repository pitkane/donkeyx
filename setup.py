from setuptools import setup, find_packages

import os

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='donkeyx',
      version='0.1.0',
      description='donkeyx',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/pitkane/donkeyx',
      download_url='',
      author='Many People',
      author_email='mikko@mbit.fi',
      license='MIT',
      entry_points={
          'console_scripts': [
              'donkeyx=donkeyx.management.base:execute_from_command_line',
          ],
      },
      install_requires=['numpy',
                        'pillow',
                        'docopt',
                        'tornado==4.5.3',
                        'requests',
                        'h5py',
                        'python-socketio',
                        'flask',
                        'eventlet',
                        'moviepy',
                        'pandas',
                        ],

      extras_require={
                      'tf': ['tensorflow>=1.9.0'],
                      'tf_gpu': ['tensorflow-gpu>=1.9.0'],
                      'pi': [
                          'picamera',
                          'Adafruit_PCA9685',
                          ],
                      'dev': [
                          'pytest',
                          'pytest-cov',
                          'responses'
                          ]
                  },

      include_package_data=True,

      keywords='selfdriving cars donkeycar donkeyx diyrobocars',

      packages=find_packages(exclude=(['tests', 'docs', 'site', 'env'])),
      )
