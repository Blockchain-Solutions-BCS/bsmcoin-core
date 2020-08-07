from distutils.core import setup
setup(name='BSMspendfrom',
      version='1.0',
      description='Command-line utility for bsmcoin "coin control"',
      author='Gavin Andresen',
      author_email='gavin@bsmcoinfoundation.org',
      requires=['jsonrpc'],
      scripts=['spendfrom.py'],
      )
