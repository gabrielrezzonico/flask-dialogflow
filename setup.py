from setuptools import setup, find_packages

setup(name='Flask-Dialogflow',
      version='0.1.1',
      description='Simple framework for creating Dialog Flow (formerly API.AI) fulfillment webhooks',
      # see: https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Framework :: Flask',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      url='https://github.com/gabrielrezzonico/flask-dialogflow',
      download_url = 'https://github.com/gabrielrezzonico/flask-dialogflow/tarball/0.1.1',
      author='Gabriel Rezzonico',
      author_email='gabriel@byte42.com',
      license='MIT',
      packages=['flask_dialogflow'],
      # $ pip install -e .[dev,test]
      extras_require={
          'dev': ['sphinx'],
          'test': ['pytest', 'pytest-cov'],
      },
      install_requires=['flask'],
      zip_safe=False)


