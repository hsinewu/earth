README
===
### About
This is the global satellite data visualization project.

## Project structure
```
project
│── css/
│── data/     - put image output here
│── js/
│── scripts/  - python scripts
│── textures/ - image assets
│── form.php  - netcdf uploader (experimental)
└── index.html   
```

## Deploy
1. clone this project.
2. generate output image.
3. put images to `data/`
4. serve the project ( except for `scripts/` )
5. done

## Use scripts to generate images
```
project
└── scripts/
    │── json/        - user defined color table in json format
    │── make_json.py - generate color.json (in grey scale) base on percentage
    │── maria.py     - generate image from database via mysql.connector
    │── master.py    - unused
    │── palette.py   - generate image from local netcdf file, provides cil interface
    └── print_csv.py - generate image from csv text file
```
### `palette.py`
Generate images from local netcdf file, several comment-line arguments are requied.
Show help: `python palette.py -h`
#### Example:
To generate variables `var1`, `var2`, `var3` from `2016120100.nc`, where the time interval is 6 hours:
`$ python palette.py --item var1 var2 var3 --time 2016120100 --dhour 6`

Currently `--time` argument is used to define the starting date of the data, also the name of the netcdf file. Accepted format is `yyyyMMddhh`.

### json/
Defined color tables
Example:
```json
{
	"stops":[
        10, 20, 30, 40
	]
	,"palette":[
        0, 0, 0,
        64, 64, 64,
        128, 128, 128,
        192, 192, 192,
        256, 256, 256
	]
}
```
`stops` defines **intervals**
`palette` defines **colors**
Also, there is an optional `offset` field. Which I use to transform units between `K` and `℃`.

pseudo code:
```python=
if val < stops[0]:
  color = palette[0]
elif val < stops[1]:
  color = palette[1]
# ..and so on so forth
else
  color = palette[-1] # last color
```

### `make_json.py`
Currently no commandline argument provided.
Read the code and change corresponding vairbles.
```python=
# in make_json.py
if __name__ == '__main__':
	ifn = 'file.nc'          # change this
	items = ['var1', 'var2'] # change this
    # ...

```

## Move images to `data/`
```
project
└── data/
    │── 2016120100/
    │── 2016120200/
    │── 2016120300/
    └── dataset.json
```
### `dataset.json`
Defining the schema of the set of data.
Effectively, it will change options in dropdown menu. (dat.gui)
Example:
```json
{
  "names":[
    "2016120100",
    "2016120200",
    "2016120300"
  ],
  "items":[
    "aprs",
    "slm",
    "tsw"
  ],
  "dh": 6,
  "length": 181
}
```
`names`: list of report(**directory**) names (under `data/`) .
`items`: list of **variables** in this set of data.
`dh`: time interval, the value of `--dhour` when generating images.
`length`: number of images for each variable(in one time period).