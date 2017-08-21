README
===
# Overview
This is the global weather simulation data visualization project.  

![](https://i.imgur.com/k3L8m0c.png)


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

## Environment
1. Install [git], 
2. Install python*  (with [SciPy]), and then [pillow]
3. Install a web server (optional)
  
For step 2, If you haven't have python installed, or have no idea how to install scipy, I would recommend [anaconda], which is the [scipy] compatible distribution I use. From then on, installing pillow should be as easy as running the command, `conda install pillow`.

\* I use python 3, and it might not work with 2
# Deploy
## Instructions
1. [clone the project](#clone-the-project)
2. [generate images](#generate-images)
3. [move images](#move-images)
4. [serve it](#web-server)
5. Review your works on your favorite browser ;)


## Clone the project
First, make sure you have [git] installed, and it's added to your path.

Now, from the commandline run
`$ git clone https://github.com/hsinewu/earth.git <project_name>`

The files should be downloaded to `./<project_name>/` folder, if <project_name> omitted, it should be at `./earth/`

For more instructions on how to clone project, visit [github](https://help.github.com/articles/cloning-a-repository/)

## Generate images
Mainly, it's about `json/` and `palette.py`
```
project
└── scripts/
    │── json/        - user defined color table in json format
    │── make_json.py - generate color.json (in grey scale) base on percentage (experimental)
    │── maria.py     - generate image from database via mysql.connector (experimental)
    │── palette.py   - generate image from local netcdf file, provides cil interface
    └── print_csv.py - generate image from csv text file (experimental)
```
### palette .py
*Purpose*: Generate images from local netcdf file  
*Input*: netcdf, [json](#json)  
*Output*: png  

Several comment-line arguments are provided, to show help run `python palette.py -h`.

| Option | Definition | Format | Default |
|-|-|-|-|
| help | list help message | N/A (switch) | N/A |
| time | starting date, also name of netcdf file | yyyyMMddhh | 2016120100 |
| item | list of variable names to be rendered | 1+ space seperated strings | "temp2" |
| dhour | length of time interval | integer* | 6 |
| src | netcdf file path | directory | ./ |
| dest | output path | directory | ./ |
| force | overwrite existing images | N/A (switch) | False |

\* Have some considerations when it's not dividable by 24, but haven't test it. Better use 1, 2, 3, 4, 6, 12, 24 or multiple. Or maybe it's just js problem but not python.

*Example*:  
To generate variables `var1`, `var2`, `var3` from `2016120100.nc`, where the time interval is 6 hours:
`$ python palette.py --item var1 var2 var3 --time 2016120100 --dhour 6`


### json/
*Purpose*: Defining color tables for each variables  
*Naming*: var1.json, which will be used to render `var1`, and so on  

*Example*:  
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
| Field | Definition | format |
|-|-|-|
| stops | breakpoint of colors | numbers |
| palette | List of RGB values | 0~255, every 3 values form a RGB |
| offset* | (optional) offset value added to stops | number |

\* I use it to transform units between `K` and `℃`, ex: `"offset":-273.15` .

*pseudo code*: (regarding how values and colors are mapped)
```python
if val < stops[0]:
  color = palette[0]
elif val < stops[1]:
  color = palette[1]
# ..and so on so forth
else
  color = palette[-1] # last color
```

### make_json .py
*Purpose*: Generate json according to percentage.  
*Input*: netcdf  
*Output*: json  

*Usage*:  
Currently no arguments are provided, read the code and change corresponding vairbles.
```python
# in make_json.py
if __name__ == '__main__':
  ifn = 'file.nc'          # change this to specify netcdf file name
  items = ['var1', 'var2'] # change this to specify variable names
    # ...

```
btw, don't forget do put your generated json file into `json/` folder.

### maria .py
*Purpose*: Retrive data from database and generate a image.  
*Input*: Database  
*Output*: png  

*Usage*: configure `database.yaml`, then change the variable/table name in the code.
```python
elm, tbl = 'olr', ''
cursor.execute( "select %s from %s;" % (elm, tbl))
```

### print_csv .py
*Purpose*: Output image from text  
*Input*: text (space separated)  
*Output*: png  

*Example*:  
`$ python print_csv var1.json var1_001.txt`

## Move images
Move images to `data/`, this is defined as variable *ROOTDIR* in `earth.js`, which is the main script for this app.
```
project
└── data/
    │── 2016120100/   # dataset 1
    │── 2016120200/   # dataset 2
    │── ...           # and so on
    └── dataset.json  # dataset schema
```

### dataset.json
Defining the schema of the set of data.
Effectively, it will change options in dropdown menu. (dat.gui)

*Example*:
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

| Field | Definition | Format |
|-|-|-|
| names | list of *dataset* names (under `data/`) . | Strings |
| items | list of *variables* in this set of data. | Strings |
| dh | time interval, the value of `--dhour` when generating images. | Integer |
| length | number of images for each variable(in one time period). | Integer |

> Notice that, according to the requirement, you can't mix datasets of different schema together. In that case, consider using [hash/](#hash) as an alternative.


## Web Server
### Chose a server
Just use whatever you prefer, though if you want to use `form.php` it needs to support php.

A short list of web servers:
+ [IIS] For windows
+ [nginx]
+ [apache]

Also, if you want a more integrated solution:
+ [xampp]
+ [MAMP]

The discussion of setting up and configuring web servers is out of the scope of this document.

## Miscellaneous
### Available GET parameter for `index.html`
| Name | Purpose | Values |
|-|-|-|
| variable | set displaying *variable* | `items` defined in dataset.json |
| report | set displaying *dataset* | `names` defined in dataset.json |
| view | set display mode | "dataset" or "forecast" |
| hash | set display data | String |

### hash
This was used to put uploaded data, but of course you can put yours too.
```
project
└── hash/
    └── my_data  # ?hash=my_data
        │── 2016120100/   # dataset 1
        └── dataset.json  # dataset schema

```
Basically, every subfolder in hash works simillary as `data/`, but it will only be loaded when explicitly specified by GET parameter *hash*.

### legend
##### TODO: make it easier to customize?
To add a legend for `var1`, you need to modify html and css.

HTML:
Under `#legends` insert a `.legend>.legend-text+.legend-unit`, make your own values and unit.

```htmlmixed
<div class="legend"> <!-- 4th element -->
    <div class="legend-text">295 265 235 205 175 145</div>
    <div class="legend-unit">K</div>
</div>
```

CSS:
Go to `css/legend.css`, insert 2 rules and you are done.
In the follwing, you will have to change both "4"s in `nth-child(4)` according to your positioning in html, from previous step.
```css
#legends.var1 > .legend:nth-child(4) {
  display: block;
}

.legend:nth-child(4) {
  background: linear-gradient(to top, #fff, #c0c0c0, #4040ff, #40a0ff, #40ffff, #ffff40, #ff8040, #ff4040); /* use your color */
  line-height: calc( 250px/7); /* divided by how many values you have */
}
```

Notes:
This works because in javascript it will update `#legends`'s className base on current display.
pseudo code:

```javascript
function onUpdate() {
    document.getElementById('legends').className = viz.item;
    // ...
}
```

### form.php
Provides netcdf upload.

[git]: https://git-scm.com/download/
[scipy]: https://www.scipy.org
[pillow]: https://python-pillow.org
[anaconda]: https://www.continuum.io/downloads
[IIS]: https://www.iis.net/learn/get-started
[nginx]: https://nginx.org/en/
[apache]: https://httpd.apache.org/
[xampp]: https://www.apachefriends.org/
[MAMP]: https://www.mamp.info/en/

