import csv
import random

import numpy as np
from matplotlib import pyplot
from shapely.geometry import Polygon, Point


class Generator:

    def __init__(self, header: list = None, class_map: dict = None, dir_: str = 'data'):
        self.header: list = header or ['x', 'y', 'class']
        self.class_map: dict = class_map or {'in': 'black', 'out': 'white'}
        self.dir_: str = dir_

    @staticmethod
    def _show_plot(data: dict):
        if data['in']['data'] is not None:
            pyplot.scatter(data['in']['data'][:, 0],
                           data['in']['data'][:, 1], 15,
                           c='b')
        if data['out']['data'] is not None:
            pyplot.scatter(data['out']['data'][:, 0],
                           data['out']['data'][:, 1], 15,
                           c='g')
        pyplot.show()

    @staticmethod
    def _generate_random_points(poly: Polygon, num_in: int, num_out: int):
        min_x, min_y, max_x, max_y = poly.bounds
        inside = []
        outside = []
        while len(inside) < num_in or len(outside) < num_out:
            random_point = Point([random.uniform(min_x, max_x),
                                  random.uniform(min_y, max_y)])
            if random_point.within(poly) and len(inside) < num_in:
                inside.append(random_point)
            if not random_point.within(poly) and len(outside) < num_out:
                outside.append(random_point)

        return inside, outside

    def _write_to_csv(self, data: dict, file_name: str):
        path = self.dir_ + '/' + file_name
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            for row in data.get('in', {}).get('data', []):
                data['in']['handler'](row, writer)
            for row in data.get('out', {}).get('data', []):
                data['out']['handler'](row, writer)

    def _handler_in_polygon(self, row, writer):
        writer.writerow(np.append(row, [self.class_map['in']]))

    def _handler_out_polygon(self, row, writer):
        writer.writerow(np.append(row, [self.class_map['out']]))

    def _prepare_data(self, poly: Polygon):
        points_in, points_out = self._generate_random_points(poly, 500, 500)
        cord_in = np.array([[p.x, p.y] for p in points_in])
        cord_out = np.array([[p.x, p.y] for p in points_out])
        data = {
            'in': {
                'data': cord_in,
                'handler': self._handler_in_polygon
            },
            'out': {
                'data': cord_out,
                'handler': self._handler_out_polygon
            }
        }
        return data

    def generate_circle_bounded(self, file_name: str, plot: bool = False):
        point = Point(50, 50)
        circle = point.buffer(50, 50)
        data = self._prepare_data(circle)

        if plot:
            self._show_plot(data)

        self._write_to_csv(data, file_name)

    def generate_triangle_bounded(self, file_name: str, plot: bool = False):
        triangle = Polygon([(1, 1), (50, 100), (100, 1)])
        data = self._prepare_data(triangle)

        if plot:
            self._show_plot(data)

        self._write_to_csv(data, file_name)

    def generate_rectangle_bounded(self, file_name: str, plot: bool = False):
        array = np.array(np.random.random((1000, 2)) * 100)

        def write_handler(item, writer):
            if item[1] >= 50:
                writer.writerow(np.append(item, [self.class_map['in']]))
            else:
                writer.writerow(np.append(item, [self.class_map['out']]))

        data = {
            'in': {
                'data': array,
                'handler': write_handler
            }
        }

        if plot:
            self._show_plot(data)

        self._write_to_csv(data, file_name)

    def generate_linear_diagonal_split(self, file_name: str, plot: bool = False):
        rectangle = Polygon([(1, 1), (1, 100), (100, 100), (1, 1)])
        data = self._prepare_data(rectangle)

        if plot:
            self._show_plot(data)

        self._write_to_csv(data, file_name)

    def generate_squares_bounded(self, file_name: str, plot: bool = False):
        array = np.array(np.random.random((1000, 2)) * 100)

        def write_handler(item, writer):
            if item[0] >= 50 > item[1]:
                writer.writerow(np.append(item, [self.class_map['out']]))
            elif item[0] < 50 and item[1] < 50:
                writer.writerow(np.append(item, [self.class_map['in']]))
            elif item[0] >= 50 and item[1] >= 50:
                writer.writerow(np.append(item, [self.class_map['in']]))
            elif item[0] < 50 <= item[1]:
                writer.writerow(np.append(item, [self.class_map['out']]))

        data = {
            'in': {
                'data': array,
                'handler': write_handler
            }
        }

        if plot:
            self._show_plot(data)

        self._write_to_csv(data, file_name)

    def generate_all(self):
        print('Start generating circle bounded data...')
        self.generate_circle_bounded('data1.csv')
        print('Finished generating circle bounded data.')

        print('Start generating triangle bounded data...')
        self.generate_triangle_bounded('data2.csv')
        print('Finished generating triangle bounded data.')

        print('Start generating rectangle bounded data...')
        self.generate_rectangle_bounded('data3.csv')
        print('Finished generating rectangle bounded data.')

        print('Start generating diagonal split data...')
        self.generate_linear_diagonal_split('data4.csv', True)
        print('Finished generating diagonal split bounded data.')

        print('Start generating square bounded data...')
        self.generate_squares_bounded('data5.csv')
        print('Finished generating square bounded data.')


if __name__ == '__main__':
    generator = Generator()
    generator.generate_all()
