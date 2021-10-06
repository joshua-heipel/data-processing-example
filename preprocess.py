import os
import const
import argparse
from hobo_io import read_raw_hobo, write_10min_hobo
from data_processing import filter_timeseries

# command line arguments -----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Peprocess raw hobo data.')
parser.add_argument('--input', type=str, help='Path of the input directory.', required=True)
parser.add_argument('--output', type=str, help='Path of the output directory.', required=True)
parser.add_argument('--id', type=str, help='The ID of the hobo device.', required=True)
parser.add_argument('--start', type=str, help='The start time of the observation period.', default=const.START)
parser.add_argument('--end', type=str, help='The end time of the observation period.', default=const.END)

if __name__ == '__main__':

    # parse command line arguments
    args = parser.parse_args()
    infile = os.path.join(args.input, args.id + '.csv')
    outfile = os.path.join(args.output, args.id + '.csv')

    # read data
    data = read_raw_hobo(infile)

    # filter timeseries (to observation period)
    data = filter_timeseries(data, args.start, args.end)

    # write output
    write_10min_hobo(data, outfile)
