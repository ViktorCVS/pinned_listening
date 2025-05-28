# pinned_listening
This project lets you set arbitrary “pins” in an audio file and instantly jump back to those points using a keyboard shortcut.

## Before clone
- Python 3 is required to run this program. Download on official site: https://www.python.org/downloads/

## How to install

You can install the project **with or without Git**. With Git, navigate to the folder where you want to clone the project and run:

```
git clone https://github.com/ViktorCVS/pinned_listening.git
```

Or if you don't have git, download the ZIP from the Releases page, unzip it into your desired directory.

Then create and activate a virtual environment:

```
cd pinned_listening
python -m venv venv
```

If Windows:
```
venv\Scripts\activate
```
If Linux/MacOS:
```
source venv/bin/activate
```

and then:
```
pip install -r requirements.txt
```

## How to start
```
python pinned_listening.py
```

![image](https://github.com/user-attachments/assets/40b16b91-4a44-4696-902a-d9b253995ae0)

## How to use

- Place your audio files in the `audio/` directory inside this repository (optional but recommended).  
- Click the **Open** button and choose your audio file (only `.wav` files are supported).

Use the following controls:  
- **Play**: start playback  
- **Pause**: pause playback  
- **Stop**: stop playback and unload the file  
- **Pin**: mark the current position and assign a keyboard shortcut  
- **Remove Pins**: clear all saved pins  

To jump to a specific timestamp:  
1. Enter the time in the input field (formats supported: `SS`, `M:SS`, or `H:MM:SS`).  
2. Click **Go** to start playing from that time, or **Go and Pause** to move there and immediately pause.  
