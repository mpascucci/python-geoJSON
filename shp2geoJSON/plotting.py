from matplotlib.pyplot import gca, text
from collections.abc import Iterable   # drop `.abc` with Python 2.7
from numpy import array

def flatten_shapes_list(nested):
  """transform a multypoligon in a list of polygons.
  This is an help function for plot_geoJSON_feature"""
  out = []
  for entry in nested:
    if not isinstance(entry[0][0], Iterable):
      out.append(entry)
    else:
      out += flatten_shapes_list(entry)
  return out

def plot_geoJSON_feature(feature, text=None, ax=None):
    """Plot a plot_geoJSON_feature"""
    if ax is None:
      ax = gca()
    ax.set_aspect('equal')
    ax.axis('off')

    
    if feature.geometry['type'] == 'Polygon':
      shapes = [array(feature.geometry['coordinates'][0]).T,]
    elif feature.geometry['type'] == 'MultiPolygon':
      shapes = flatten_shapes_list(feature.geometry['coordinates'])
      shapes = [array(pts).T for pts in shapes]
    else:
      raise Exception("unknown shape")
  
    # fet plot attribute from
    color = feature.properties.get('color','k')
    weight = feature.properties.get('weight', 1)
    opacity = feature.properties.get('opacity', 1)
    fill_color = feature.properties.get('fillColor', None)
    fill_opacity = feature.properties.get('fillOpacity', 1)
    
    for shape in shapes:
      # plot outline
      if color is not None:
        ax.plot(*shape, color, alpha=opacity, lw=weight);
      # fill shape
      if fill_color is not None:
        ax.fill(*shape, fill_color, alpha=fill_opacity)
      # add text
      if text is not None:
        center = shape.mean(axis=1)
        plt.text(*center, text, fontsize=10)
        
        
def hex_color(color_tuple):
  """Transform color tuple in hex form:
      
  >>> hex_color((1,0,0))
  '#ff0000'
  """
  color_str = "#"
  for c in color_tuple:
    t = hex(int(round(c*255)))[2:].zfill(2)
    color_str += t
  return color_str