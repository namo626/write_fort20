## write_fort20

Authors: Matthew Scarborough, Mark Loveland, Namo Wichitrnithed

### Installation

In this folder, run `pip install .`

### Usage

For help, use `write_fort20 -h`.
Example usage for Hurricane Harvey, where the run is 20 days, the mesh is `fort.14`, the hourly gauge files are stored in the directory `data/`:

	write_fort20 -f fort.14 -o harvey.20 -i data -dt 3600 -t '2017-08-16-6:00' -d 9

The output here is `harvey.20`.
