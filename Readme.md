# Land Use around Italian Football Stadiums

What surrounds Italy's new and planned stadiums — homes, shops, parks, parking, infrastructure?
This project builds a reproducible **GIS pipeline** that draws a 500 × 500 m area around each of **21 Italian stadiums**, classifies the surrounding land use from **OpenStreetMap**, computes the share of each land-use class and exports an interactive map for **kepler.gl**.

> Built during my 2026 internship at Sport Business Lab Consultancy, as supporting analysis for a strategic report on new multifunctional sports facilities in Italy.

---

## Pipeline

```
config/stadiums.py ──> 01 buffers ──> 02 OSM land use ──> 03 classification ──> 04 export
  (21 stadiums,          500×500 m      Overpass API        & % per class          GeoJSON + HTML
   coordinates)          (UTM)          (osmnx)             (dissolve by class)     for kepler.gl
```

| Step | Script | What it does |
|---|---|---|
| 1 | `01_create_buffers.py` | Square 500 × 500 m buffer around each stadium, built in UTM and exported in WGS84 |
| 2 | `02_fetch_landuse.py` | Downloads OSM polygons inside each buffer via the Overpass API (with a pause between requests for fair use) |
| 3 | `03_compute_percentages.py` | Maps OSM tags to land-use classes, **dissolves overlapping polygons** by class to avoid double counting, computes % of the buffer |
| 4 | `04_export_kepler.py` | Merges everything into one GeoJSON for kepler.gl, plus an offline HTML preview |

`run_pipeline.py` runs the four steps in sequence, for all stadiums, priority stadiums only, or a single stadium.

---

## Land-use classes

| Class | Main OSM tags |
|---|---|
| Residential | `landuse=residential`, `building=residential/apartments/house` |
| Commercial | `landuse=commercial/retail`, `shop=*`, `building=office/retail` |
| Public green | `leisure=park/garden`, `landuse=grass/forest`, `natural=wood` |
| Parking | `amenity=parking`, `parking=*` |
| Infrastructure | `railway=*`, `aeroway=*`, `power=*`, `landuse=industrial` |
| Public services | `amenity=school/hospital/university` |
| Water | `natural=water`, `waterway=*` |
| Sports facilities | `leisure=stadium/sports_centre/pitch` |
| Unmapped | buffer area with no OSM coverage |

Each polygon in the output carries `landuse_class`, `area_mq`, `pct_of_buffer`, `stadium_id`, `name`, `city` and `club`.

<!-- Add a screenshot of the kepler.gl map here:
<p align="center"><img src="images/kepler_map.png" width="85%" alt="Land use around a stadium in kepler.gl"></p>
-->

---

## How to run

```bash
conda env create -f environment.yml      # or: pip install -r requirements.txt
conda activate stadi-landuse

python run_pipeline.py                   # all 21 stadiums
python run_pipeline.py --priority-only   # priority stadiums only
python run_pipeline.py --stadium bergamo_new_balance_arena
```

Output:
- `data/output/stadi_landuse_kepler.geojson` → drag and drop on [kepler.gl/demo](https://kepler.gl/demo), colour by `landuse_class`, filter by `city`
- `data/output/stadi_landuse_map.html` → offline preview

---

## Repository structure

```
├── config/stadiums.py        # 21 stadiums: coordinates, priority, coordinate status
├── scripts/
│   ├── utils.py              # square buffer + land-use classifier
│   ├── 01_create_buffers.py
│   ├── 02_fetch_landuse.py
│   ├── 03_compute_percentages.py
│   └── 04_export_kepler.py
├── run_pipeline.py
├── environment.yml / requirements.txt
└── README.md
```

---

## Limitations

- **OSM completeness varies**: land-use mapping is more detailed in some cities than others; unmapped areas are reported explicitly instead of being ignored.
- **Planned stadiums** (Roma Pietralata, Venezia Bosco dello Sport, Bologna temporary stadium) use **approximate coordinates** until final plans are available.
- **Fixed 500 m area**: a square buffer is simple and comparable across stadiums, but does not reflect walking distance on the street network.

---

## Tools

Python · GeoPandas · Shapely · pyproj · OSMnx · Overpass API · kepler.gl

---

## Author

**Carlo Pegoraro** — [GitHub](https://github.com/carlopego14)
