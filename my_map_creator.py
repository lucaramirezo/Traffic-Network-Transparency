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
    def __init__(self, df: pd.DataFrame, lat_col_name: str = 'LATITUD', long_col_name: str = 'LONGITUD',
                 columns_for_label: list = [],
                 is_cords_utm=True):
        coords = [lat_col_name, long_col_name]
        self.df = df.dropna(subset=coords).copy()  # Drop rows where coordinates are NaN
        self.is_cords_utm = is_cords_utm
        self.columns_for_coordinates = coords
        if is_cords_utm:
            self.__to_lat_lon()

        if columns_for_label is not None:
            self.df_labels = self.df[columns_for_label].fillna('MISSING')
        else:
            self.df_labels = None

    def set_columns_for_label(self, columns_for_label: list):
        self.df_labels = self.df[columns_for_label].fillna('MISSING')

    def set_df(self, df):
        self.df = df.dropna(subset=self.columns_for_coordinates)
        if self.is_cords_utm:
            self.__to_lat_lon()

    def __to_lat_lon(self):
        """
        Convert UTM coordinates to Latitude and Longitude if is_cords_utm is True.
        """
        # Apply the conversion to each row in the DataFrame
        self.df[self.columns_for_coordinates] = self.df.apply(
            lambda row: utm_to_latlon(row[self.columns_for_coordinates[0]], row[self.columns_for_coordinates[1]]),
            axis=1, result_type='expand'
        )
        self.df = self.df.dropna(subset=self.columns_for_coordinates)  # Remove rows where conversion failed

    def create_map(self, output_dir='Maps/', map_name='map'):
        madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=12)

        if self.df_labels is not None:
            coords = self.df.filter(items=self.columns_for_coordinates)
            labels = self.df_labels.to_dict(orient='records') if self.df_labels is not None else [{}] * len(coords)

            for (lat, lon), label in zip(coords.values, labels):
                popup_text = '\n'.join([f"{k}: {v}" for k, v in label.items()]) if label else ''
                folium.Marker([lat, lon], popup=popup_text).add_to(madrid_map)
        else:
            coords = self.df[list(self.columns_for_coordinates)]
            for (lat, lon) in coords.values:
                folium.Marker([lat, lon]).add_to(madrid_map)

        # Save the map to an HTML file
        map_file = f"{output_dir}{map_name}.html"
        madrid_map.save(map_file)
