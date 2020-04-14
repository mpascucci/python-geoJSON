from distutils.core import setup

setup(name='shp2geoJSON',
      version='1.1',
      description='shapefile to geoJSON conversion',
      install_requires=['pyshp','pyproj','matplotlib'],
      author='Marco Pascucci',
      author_email='marpas.paris@gmail.com',
      url='',
      packages=['shp2geoJSON'],
     )
