import unittest
from my_map_creator import MapCreator  # Make sure to import your MapCreator class
import pandas as pd

class TestMapCreator(unittest.TestCase):
    def setUp(self):
        # Sample data
        data = {'UTM_X': [500000, 500100], 'UTM_Y': [4649776, 4649876], 'Label1': ['Location1', 'Location2'], 'Label2': ['Info1', 'Info2']}
        self.df = pd.DataFrame(data)
        self.columns_for_coordinates = ('UTM_X', 'UTM_Y')
        self.columns_for_label = ['Label1', 'Label2']

        # Initialize MapCreator
        self.map_creator = MapCreator(self.df, self.columns_for_coordinates, self.columns_for_label, is_cords_utm=True)

    def test_utm_to_latlon_conversion(self):
        # Test the UTM to latitude/longitude conversion
        lat, lon = self.map_creator.df[self.columns_for_coordinates].iloc[0]
        self.assertIsInstance(lat, float, "Latitude should be a float")
        self.assertIsInstance(lon, float, "Longitude should be a float")

    def test_set_columns_for_label(self):
        # Test the set_columns_for_label method
        new_labels = ['Label1']
        self.map_creator.set_columns_for_label(new_labels)
        self.assertIn('Label1', self.map_creator.df_labels.columns, "Label1 should be in the labels dataframe")

    def test_create_map(self):
        # Test the create_map method
        # Note: You might need to mock folium.Map.save method if you don't want to create an actual file during the test
        self.map_creator.create_map(map_name='test_map')
        # Check if file exists or other checks to ensure map was created successfully

    def test_data_integrity(self):
        # Test if the data remains consistent after operations
        initial_row_count = len(self.df)
        self.assertEqual(initial_row_count, len(self.map_creator.df), "Row count should remain the same after initialization")

        # Add more tests related to data integrity if needed

# Run the tests
if __name__ == '__main__':
    unittest.main()