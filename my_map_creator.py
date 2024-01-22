import utm
import folium
import pandas as pd


def utm_to_latlon(utm_x, utm_y, zone_number=30, zone_letter='T'):
    """
    Convert UTM coordinates to Latitude and Longitude.
    Assumes zone number 30 and zone letter 'T' for Madrid.
    """
    try:
        lat, lon = utm.to_latlon(utm_x, utm_y, zone_number, zone_letter)
        return lat, lon
    except Exception as e:
        print("Error en la conversión:", e, " utm_x: ", utm_x, "utm_y: ", utm_y, " ")
        return None, None


class MapCreator:
    df: pd.DataFrame
    df_cords: pd.DataFrame
    df_labels: pd.DataFrame
    columns_for_coordinates: list
    is_cords_utm: bool

    def __init__(self, df: pd.DataFrame, columns_for_coordinates: list, is_cords_utm=True):
        self.df = df
        self.df_cords = df.filter(items=columns_for_coordinates)
        self.is_cords_utm = is_cords_utm
        self.columns_for_coordinates = columns_for_coordinates

        if is_cords_utm:
            self.__to_lat_lon()

    def set_columns_for_label(self, columns_for_label: list):
        self.df_labels = self.df.filter(items=columns_for_label)

    def set_df(self, df):
        self.df = df

    def __to_lat_lon(self):
        """
        Convert UTM coordinates to Latitude and Longitude if is_cords_utm is True.
        """
        # Apply the conversion to each row in the DataFrame
        self.df_cords[self.columns_for_coordinates] = self.df_cords.apply(
            lambda row: utm_to_latlon(row[0], row[1]), axis=1, result_type='expand'
        )
        self.df_cords = self.df_cords.dropna()

    def create_map(self, output_dir='Maps/', map_name='map'):
        # Creating a map centered around Madrid
        madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=12)

        # Adding the coordinates and labels to the map
        for idx, (cord_row, label_row) in enumerate(zip(self.df_cords.iterrows(), self.df_labels.iterrows())):
            _, cord_data = cord_row
            _, label_data = label_row
            label_parts = [f"{col_name}: {label_data[col_name]}" for col_name in self.df_labels.columns]
            label = '\n'.join(label_parts)  # Join all parts with a newline character
            folium.Marker([cord_data['lat'], cord_data['lon']], popup=label).add_to(madrid_map)

        # Save the map to an HTML file
        map_file = output_dir + map_name + '.html'
        madrid_map.save(map_file)
