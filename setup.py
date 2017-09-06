from setuptools import setup, find_packages

setup(
  name='browserstack',
  version='1.0.0',
  description='A CLI wrapper for the BrowserStack API',
  url='https://github.com/jsakas/browserstack-cli',
  author='Jon Sakas',
  author_email='jon.sakas@gmail.com',
  license='MIT',
  zip_safe=False,
  install_requires=[],
  packages=find_packages(),
  scripts=[
    'bin/browserstack',
  ]
)
