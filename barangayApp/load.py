from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Barangay

barangay_mapping = {
    'name_2': 'Mun_Name',
    'id_3': 'Bgy_Code',
    'name': 'Bgy_Name',
    'geom': 'MultiPolygon',
}
barangay_shp = Path(__file__).resolve().parent / 'shape_files' / 'psa_biliran_barangays.shp'

def run(verbose=True):
    lm = LayerMapping(Barangay, barangay_shp, barangay_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

# municipal_mapping = {
#     'id_2': 'ID_2',
#     'name': 'NAME_2',
#     'geom': 'MultiPolygon',
# }

# municipal_shp = Path(__file__).resolve().parent / 'shape_files' / 'biliran_municipals_1.shp'

# def run(verbose=True):
#     lm = LayerMapping(Municipal, municipal_shp, municipal_mapping, transform=False)
#     lm.save(strict=True, verbose=verbose)