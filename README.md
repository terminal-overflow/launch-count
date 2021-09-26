# Python Launch Count
## Launch Count
---
This repository provides you with two versions of the program - one with world time zones and one without. Both provide a countdown/up for rocket launches or space related events.

### Dependencies
* pytz (`count.py`)

---
## Installation via GitHub
#### Setting up a virtual environment (optional)
```
virtualenv [environment name]
source [environment name]/bin/activate
```

### Clone the repository (Developers)
```
 git clone https://github.com/terminal-flow/launch-count.git
```

### Or Download
* Click the download button
* Unzip the project file

### Change directory to the project root
```
cd path/to/launch-count
```

### Install requirements
```
pip3 install -r requirements.txt
```

### Run
```
cd src
```
with launch-count with time zones
```
python3 count.py
```
with launch-count without time zones
```
python3 simple_count.py
```

---
## Usage
### Date(s) entry
* The file `info.txt` controls when the 'event' is taking place.
* Format: `t-,year,month,day,hour,minute,second`.
* Any number of dates can be entered (distinguished by a new line).
* A line can be commented out, in either of the files, using a hashtag(#).
* If no date is entered, `count.py` will just display time zones whereas `simple_count.py` will exit.

### Time zone highlight
* The file `highlight.txt` controls which time zones are highlighted and only affects `count.py`.
* Any number of time zones can be entered (distinguished by only a comma or only a new line).

#### Note
These files can be found in the `info/` directory.

### Keybinds
* Q: Quit program
* F: Toggle fullscreen (`count.py` only)
* Esc: Exit fullscreen (`count.py` only)

---
### Example
Launch date from Cape Canaveral: 20 February 2020 at 13:15:18pm (local time)
<br/>
Text in info.txt: `t-,2020,2,20,13,15,18`
<br/>
Text in highlight.txt (optional): `New York`

---
## License
Launch count is released under the Apache License 2.0. See LICENSE for details.
