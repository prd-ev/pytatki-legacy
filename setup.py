from setuptools import setup
import pytatki as app

setup(name='Pytatki',
      version=app.__version__,
      description="Organizer klasowy",
      author=app.__author__,
      tests_require=['pytest','pytest-flask']
      )
