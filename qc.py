import os
import pandas as pd
import argparse
from hobo_io import read_10min_hobo, read_reference, write_hourly_hobo
from data_processing import filter_timeseries
from util import quality_control, hourly_mean, regression_model, replace_na
import const

# command line arguments -----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Perform QC procedure and fill gaps with a linear regression model.')
parser.add_argument('--input', type=str, help='Path of the input directory.', required=True)
parser.add_argument('--output', type=str, help='Path of the output directory.', required=True)
parser.add_argument('--reference', type=str, help='The file with data of the reference stations.', required=True)
parser.add_argument('--id', type=str, help='The ID of the hobo device.', required=True)
parser.add_argument('--start', type=str, help='The start time of the observation period.', default=const.START)
parser.add_argument('--end', type=str, help='The end time of the observation period.', default=const.END)

if __name__ == '__main__':

    # parse command line arguments
    args = parser.parse_args()
    infile = os.path.join(args.input, args.id + '.csv')
    outfile = os.path.join(args.output, args.id + '_Th.csv')

    # read data
    data = read_10min_hobo(infile)
    data = filter_timeseries(data, args.start, args.end)
    reference_data = read_reference(args.reference)
    reference_data = filter_timeseries(reference_data, args.start, args.end)

    # quality control
    data = quality_control(data)
    data = hourly_mean(data)

    # linear regression
    data = pd.merge(reference_data, data, left_on='date_time', right_on='date_time', how='right')
    predictions, _ = regression_model(data, list(reference_data.columns)[1:], 'temp')
    data = replace_na(data, predictions, 'temp')

    # write output
    data = pd.DataFrame({'date': data.date_time,
                         'th': data.temp,
                         'origin': data.qc_total.apply(lambda x: 'R' if x else 'H')})
    write_hourly_hobo(data, outfile)