## write_fort20

Authors: Matthew Scarborough, Mark Loveland, Namo Wichitrnithed

### Installation

In this folder, run `pip install .`

### Usage

For help, use `write_fort20 -h`.
Example usage for Hurricane Harvey, where the run is 20 days, the mesh is `fort.14`, the hourly gauge files are stored in the directory `data/`:

	write_fort20 -f fort.14 -o harvey.20 -i data -dt 3600 -t '2017-08-16-6:00' -d 9

The output here is `harvey.20`.

### Extended Example
The basic structure of the provided data folder is this:

```bash
├── 30m_cut.14
├── TemplateFlows
├── Harvey
│   ├── shukai.txt
├── Ike
│   ├── shukai.txt
└── Edouard
    └── shukai.txt
...
```
Here `shukai.txt` is the missing flow data for the respective river. Then inside each storm folder, run

	python3 shukai_gauges.py

This will create a local directory `data` which contains all the river flow data. Specifically, this script does the following:

1. Creates a folder `data`, deleting any existing one
2. Copies the 45 river csv files from `TemplateFlows` to `data`
3. Parses the river names in `shukai.txt` and matches them to the correct indices as specified in [gauge_info](https://docs.google.com/spreadsheets/d/1TmZHVMFxkr7OIIkLz5q_fRM_fL_4IiBtKnD4bvYImdg/edit?usp=sharing).**Note that the river names in `shukai.txt` should be as close to the ones in the table as possible, since we're using fuzzy search to match them**.
4. Writes the time series for each river in `shukai.txt` to the corresponding CSV file in `data`, overwriting the existing one from `TemplateFlows`

As the script finishes, the `data` folder should contain 45 river CSV files. Then, if we pick Harvey, we would run

	write_fort20 -f ../30m_cut.14 -o harvey.20 -i data -dt 3600 -t '2017-08-16-6:00' -d 9

and the output will be `harvey.20`.
	


