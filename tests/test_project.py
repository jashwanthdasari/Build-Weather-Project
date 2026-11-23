import csv, json, os, tempfile, unittest
from unittest.mock import patch

from campussolve.validation import validate_city, validate_float, validate_coordinates, ValidationError
from campussolve.storage import Storage
from campussolve.analytics import summarize, filter_records, warning_flags
from campussolve.importer import import_csv
from campussolve.reports import build_report, export_report
from campussolve.weather_api import geocode_city, fetch_current_weather, WeatherAPIError

SAMPLE = {'city':'Test City','country':'Testland','latitude':1.0,'longitude':2.0,'observed_at':'2026-01-01T12:00',
 'temperature_c':20.0,'feels_like_c':19.0,'humidity_percent':50,'wind_kmh':10.0,'precipitation_mm':0.0,
 'weather_code':0,'condition':'Clear sky','source':'test'}

class ValidationTests(unittest.TestCase):
 def test_city_normalizes(self): self.assertEqual(validate_city('  Hyderabad  '),'Hyderabad')
 def test_blank_city_fails(self):
  with self.assertRaises(ValidationError): validate_city('  ')
 def test_numeric_ranges(self): self.assertEqual(validate_float('42','humidity',0,100),42)
 def test_range_rejected(self):
  with self.assertRaises(ValidationError): validate_float(101,'humidity',0,100)
 def test_coordinates(self): self.assertEqual(validate_coordinates(90,-180),(90.0,-180.0))
 def test_bad_coordinates(self):
  with self.assertRaises(ValidationError): validate_coordinates(91,0)

class StorageAnalyticsTests(unittest.TestCase):
 def test_json_csv_round_trip(self):
  with tempfile.TemporaryDirectory() as d:
   s=Storage(d); s.save_record(SAMPLE); self.assertEqual(len(s.load()),1)
   self.assertTrue(os.path.exists(s.csv_path))
 def test_corrupt_json_recovers(self):
  with tempfile.TemporaryDirectory() as d:
   s=Storage(d)
   with open(s.json_path,'w') as f: f.write('{bad json')
   self.assertEqual(s.load(),[])
   self.assertTrue(any('.corrupt-' in n for n in os.listdir(d)))
 def test_summary(self):
  second=dict(SAMPLE,temperature_c=30,humidity_percent=70,city='Other')
  stats=summarize([SAMPLE,second]); self.assertEqual(stats['count'],2); self.assertEqual(stats['cities'],2)
  self.assertEqual(stats['average_temperature_c'],25.0)
 def test_filters(self):
  self.assertEqual(len(filter_records([SAMPLE],keyword='test')),1)
  self.assertEqual(len(filter_records([SAMPLE],condition='Fog')),0)
  self.assertEqual(len(filter_records([dict(SAMPLE,condition='Light rain')],condition='Rain')),1)
 def test_thresholds(self):
  record=dict(SAMPLE,temperature_c=40,wind_kmh=60,humidity_percent=95)
  self.assertEqual(len(warning_flags(record)),3)
 def test_report_export(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertIn('Executive Summary',build_report([SAMPLE]))
   paths=export_report([SAMPLE],d); self.assertEqual(len(paths),2); self.assertTrue(all(os.path.isfile(p) for p in paths))

class ImportTests(unittest.TestCase):
 def test_valid_and_invalid_rows(self):
  with tempfile.NamedTemporaryFile(mode='w',newline='',encoding='utf-8',delete=False) as f:
   writer=csv.DictWriter(f,fieldnames=['city','temperature_c','humidity_percent','wind_kmh']); writer.writeheader(); writer.writerow({'city':'Alpha','temperature_c':22,'humidity_percent':60,'wind_kmh':4}); writer.writerow({'city':'','temperature_c':'oops','humidity_percent':120,'wind_kmh':-1}); path=f.name
  try:
   records,errors=import_csv(path); self.assertEqual(len(records),1); self.assertEqual(len(errors),1)
  finally: os.unlink(path)
 def test_missing_headers(self):
  with tempfile.NamedTemporaryFile(mode='w',newline='',delete=False) as f: f.write('city,temperature_c\n'); path=f.name
  try: self.assertTrue(import_csv(path)[1])
  finally: os.unlink(path)

class ApiTests(unittest.TestCase):
 @patch('campussolve.weather_api._get_json')
 def test_geocode_parses(self,mock):
  mock.return_value={'results':[{'name':'Hyderabad','country':'India','latitude':17.3,'longitude':78.4,'timezone':'Asia/Kolkata'}]}
  self.assertEqual(geocode_city('Hyd')['country'],'India')
 @patch('campussolve.weather_api._get_json')
 def test_current_weather_parse(self,mock):
  mock.return_value={'current':{'time':'2026-01-01T12:00','temperature_2m':23,'relative_humidity_2m':50,'apparent_temperature':22,'precipitation':0,'weather_code':0,'wind_speed_10m':8}}
  result=fetch_current_weather(17,78,{'name':'City','country':'India'}); self.assertEqual(result['condition'],'Clear sky'); self.assertEqual(result['temperature_c'],23)

class PlotTests(unittest.TestCase):
 def test_plot_files(self):
  try: import matplotlib
  except ImportError: self.skipTest('matplotlib unavailable')
  matplotlib.use('Agg')
  from campussolve.plotting import plot_temperature, plot_distribution
  with tempfile.TemporaryDirectory() as d:
   p1=os.path.join(d,'trend.png'); p2=os.path.join(d,'hist.png')
   plot_temperature([SAMPLE],p1,show=False); plot_distribution([SAMPLE],p2,show=False)
   self.assertTrue(os.path.getsize(p1)>0); self.assertTrue(os.path.getsize(p2)>0)

if __name__ == '__main__': unittest.main()
