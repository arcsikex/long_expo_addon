# LONG EXPOSURE Video Effect
This addon lets you create a long exposure effect in Blende Video Sequence Editor.
The workflow is the same as descirbed in Aidin Robbins' [LONG EXPOSURE Video Effect](https://youtu.be/H2SYdgMDvMM) video.


# Installation
1. Download the [long_expo_effect.py](long_expo_effect.py) file
2. In Blender go to Edit -> Preferences -> Add-ons ->Install
3. Select the downloaded file

# How to use it
1. Select a **video strip**
2. Open up the **Strip** Panel
3. Search for **Long Exposure Effect** panel
4. Click the button
5. Change the properties on the redo panel

## Properties:

- Levels: The number of duplicated strips, the higher the value the more you can see the effect. But **it can slow down your scene significantly**. (I recommend to set it to ~40-50)
- Opacity: Opacity of the duplicated layers (you should keep it around 0.05)
- Fade In / Fade Out: Start/End the effect gradually. If they are unchecked the beginning/end will be cut off

## Hint
To improve playback performance in the Preview window got to **View -> View Settings -> Proxy render Size ->** Set it to **25%**
