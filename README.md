# data-processing-example

- implemented with Python 3.6.9
- requirements.txt lists necessary packages
- const.py contains constants used for the qc procedure
- reference_data.csv stores the data of the reference stations for the linear regression model

run preprocessing script:  
python preprocess.py --input <input directory> --output <output directory> --id <hobo id>  
  
run quality control procedure:  
python qc.py --input <input directory> --output <output directory> --reference <file with reference data> --id <hobo id>  
  
more info:  
python preprocess.py -h  
python qc.py -h  
