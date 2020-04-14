from json import dumps
import pyproj
import shapefile as shp
from collections.abc import Iterable   # drop `.abc` with Python 2.7

  
class geoJSON_feature(dict):
  """an improved dictionary to represent a geoJSON feature"""
  @property
  def properties(self):
    return self["properties"]
  
  @property
  def geometry(self):
    return self["geometry"]
  
  def flatten(self):
    """Return a flatten version of the feature. Useful tu use with Pandas Dataframes
    
    Example:
      pd.DataFrame(feature.flatten())
    """
    d = dict()
    for k,v in self.properties.items():
      d[k] = v
      
    for k,v in self.geometry.items():
      d[f"geometry_{k}"] = v
      
    return d
  
  def to_JSON(self):
    return dumps(self)

config = dict(
  UTM_zone = '33T',
  emisphere = 'north'
)

utmProj = pyproj.Proj(f"+proj=utm +zone={config['UTM_zone']}, +{config['emisphere']} +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
def utm_to_decimal(coord):
  """Transform UTM coordinates into decimal longitude and latitude."""
  assert len(coord) == 2
  lon, lat = utmProj(*coord, inverse=True)
#   lon = round(lon,3)
#   lat = round(lat,3)
  return (lon,lat)


def utm_to_decimal_recursive(nested):
  """recursively convert coordinates."""
  out = []
  for entry in nested:
    if not isinstance(entry[0], Iterable):
      out.append(utm_to_decimal(entry))
    else:
      out.append(utm_to_decimal_recursive(entry))
  return(out)


def shp_record2geoJSON_feature(reader, index):
  """Transform a shp record in geoJSON format.
  
  reader: shapefile reader (reader = shp.Reader(shp_path))
  index [int] : record index
  
  key_property : name of the discriminant property to assign a custo value
  values_dict : a dict wich possible values of key_property as keys, and corresponding custom values
  
  a new 'value' property will be added to the record. This property corresponds to
  values_dict[proeprties.key_property].
  
  """
  # get the field names from the shape reader
  field_names = [field[0] for field in reader.fields[1:]]
  sr = reader.shapeRecords()[index]
  
  atr = dict(zip(field_names, sr.record))
  geom = sr.shape.__geo_interface__
  temp = utm_to_decimal_recursive(geom['coordinates'])
  geom['coordinates'] = temp

#   if key_property is not None:
#     key = atr[key_property]
#     atr['value'] = values_dict.get(key,None)
  
  return geoJSON_feature(
    type="Feature",
    geometry=geom,
    properties=atr
  )


def reader2geoJSON_features(reader, records='all'):
  """transform a shapefile reader in a list of geoJSON features.
  
  reader: a shapefile Reader instance (defined in module shapefile)"""
  
  if records=='all':
    records = range(len(reader.records()))
    
  return [shp_record2geoJSON_feature(reader, i) for i in records]



def shapefile2geoJSON_features(path):
  """transform a shapefile in a list of geoJSON features."""
  return reader2geoJSON_features(shp.Reader(path))