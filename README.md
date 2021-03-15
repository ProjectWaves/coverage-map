## View ISP Coverage in Baltimore with Census and FCC Data

This is like a local version of [Fixed Broadband Deployment](https://broadbandmap.fcc.gov/), where we can use python to script things and drop in our own data. 



Extend and modify as you see fit. Currently, it plots different speeds from Comcast from white to dark green. White = not covered, dark green = max speed Comcast offers in this area. I think I also missed a few areas that aren't water but still should be filled in.



You'll notice that everything is white or dark green. Comcast only lists 3 speeds - `0, 987, 1000` megabits per second. :(



That being said, now that we have the starting point for a map (and blocks from the Census), we could use dfiferent speeds than those provided by Comcast to see what the actual coverage looks like.



Perhaps this can be done by running an mlab or speed test server and saving the comcast results?



## How to Run

Run `python draw_map.py` from the directory holding `tl_2020_24510` and `baltimore_data.csv` or `Fixed_Broadband_Deployment_Data__December_2019.csv`. Note: The FCC data is HUGE and hasn't been saved in this repository. You can get it [here](https://opendata.fcc.gov/Wireline/Fixed-Broadband-Deployment-Data-December-2019/whue-6pnt).