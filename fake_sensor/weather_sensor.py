import csv

def read_csv_data_loop(file):
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        while True:
            for row in reader:
                yield dict(zip(header, row))
            csv_file.seek(0)

class WeatherSensor:

    def __init__(self, dataset_csv_filepath):
        self.dataset_csv_filepath = dataset_csv_filepath

    def get_data_from_dataset(self):
        return read_csv_data_loop(self.dataset_csv_filepath)
