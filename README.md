# ANIMATE
Animate is an interpreter written in Python which reads a timed sequence of commands from an Excel file and a number of bitmap images, and then composes movie frames with these commands. It can make simple animations, but also much more complex ones.

![Introduction](pictures/bulldozer_bucket.gif)
[Balls](https://github.com/henkjannl/py-animate/pictures/bouncing_balls_ball.png)

Features:
* it can handle location, rotation, scale and opacity of many images in parallel
* the transitions can be asynchronous
* the stacking of images can be modified on the fly
* it can use nested scripts to generate a composed image that can be used in a script on a higher level
* since Animate uses a spreadsheet to define the animation, all parameters can be driven by relations in the spreadsheet
* to speed up debugging
    * Animate can create frames at a very low frame rate or it can only process frames between a certain interval
    * only a subset of the frames can be recomputed
    * the time can be plotted in the lower left corner of every frame    
* frames can be combined to produce an animated GIF or a movie

Animate heavily relies on open source software such as Python, the Python Imaging Library (PIL) and XLRD. Many thanks to the creators of this great software. Please don't forget to donate to all these great projects.

<br><br>

# Table of Contents
* [Typical workflow](#typical-workflow)
* [Dependencies](#dependencies)
* [The `SCRIPT` command](#the-script-command)
* [The `TABLE` command](#the-table-command)
* [Time in Animate](#time-in-animate)
* [Coordinate system](#coordinate-system)
* [Types of items](#types-of-items)
* [`BRINGTOFRONT` and `SENDTOBACK`](#bringtofront-and-sendtoback)
* [The `IMAGE` item](#the-image-item)
* [The `TEXT` item](#the-text-item)
* [Scaling, rotating and the pole](#scaling-rotating-and-the-pole)
* [The `ASSEMBLY` item](#the-assembly-item)
* [Working with `TIMEOFFSET`](#working-ith-time-offset)
* [The `MASK`](#the-mask)
* [The `CANVAS`](#the-canvas)
* [Reusing a `TABLE` more than once](#reusing-a-table-more-than-once)
<br><br>

# Typical workflow

The animation can be controlled by one or more sheets in a single Excel file:
* In a `SCRIPT`, items can be declared and manipulated
* A `TABLE` is similar to a script but the data is stored in tabular format and some commands cannot be used

An Animate project directory looks like this:
* An Excel file which holds all `SCRIPT`s and `TABLE`s
* A Python file which imports and calls Animate and refers to the Excel file and the main script
* A `..\Pictures` subdirectory which holds all images used in the animation. The bitmaps are typically .png files with transparent background. They can for instance be created using Inkscape.
* A `..\Frames` subdirectory which holds all frames generated by Animate. Does not have to be created by the user, Animate will create this directory if it does not yet exist.

The Excel file typically contains various sheets, each containing a `SCRIPT`, `TABLE`, `ASSEMBLY` or `CANVAS`. One `SCRIPT` is the main script that is reffered to in the python file. 

The python file typically contains just two lines of code:

```python
from Animate import Animate
Animate.Model('Simulation.xls', 'Main')
```
The two parameters refer to the Excel file and the name of the sheet that contains the main script.

<br><br>


# Dependencies

The following libraries must be installed:

| <!-- --> | <!-- --> | <!-- --> |
|----------|----------|----------|
| `python`        | >v3.0                     | python.org                                 |
| `animate`       |                           |                                            |
| `xlrd`          | pip install xlrd          | http://www.python-excel.org/               |
| `pillow`        | pip install Pillow        | https://python-pillow.org/                 |
| `ffmpeg`        |                           | https://ffmpeg.org/                        |
| `ffmpeg-python` | pip install ffmpeg-python | https://github.com/kkroening/ffmpeg-python |

Remarks:
* ffmpeg is only needed if video files need to be created
* in order to use ffmpeg, the ffmpeg library itself first needs to be installed on the system
* ffmpeg-python is a python binder to ffmpeg. Please make sure ffmpeg-python is spelled correctly, there are various similar libraries with different spelling
 
<br><br>

# The `SCRIPT` command
A `SCRIPT` is a timed sequence of commands that influence properties

The columns have a predefined meaning:

| <!-- --> | <!-- --> |
|----------|----------|
| Column A | Contains the time at which an event takes place     |
| Column B | Contains a property or a command                    |
| Column C | Contains an item name or a value                    |
| Column D | Contains a value, if column C contains an item name |

Remarks:
* The other columns can be used for comments or for calculations
* If the cell in column A does not contain a number, the complete row is ignored by the script and can be considered to be a comment
* The time does not have to be ordered
* By definition, Frame0000 corresponds to time 0.00 seconds in the main `SCRIPT`
* Items do not need to be explicitly created. If the item occurs for the first time in the script, Animate automatically creates a new item. Therefore, pay attention to spell the names of the items correctly; if an item name is spelled incorrectly, a second item will be created
* Animate checks if every `Image` item has at least one image designated. If not, an error is raised.
* Commands, properties and item names are not case sensitive
* All items have most properties in common

<br><br>

### **Example 1. A bulldozer**
A `SCRIPT` can look like this:

![](pictures\script_bulldozer.png)
[Bulldozer](pictures\script_bulldozer.png)

This script contains 4 images, all of them showing an item at their default position in the image without transformation:
1. Background.png
2. Bulldozer.png
3. Heap.png
4. Cloud.png

The images are stacked on top of each other like this:

![](pictures\bulldozer_stack.png)

The following sequence is played:
* The bulldozer will ride from `XPOS`=-380 (out of screen on the left side) to `XPOS`=+690 (out of screen on the right side)
* In cells G15 and G16, the time at which the bulldozer reaches `XPOS`=0 is calculated (t=2.13 s). This is the location at which the bulldozer reaches the heap.
* Cell A18 refers to the calculated time in G16. Between t=2.13 and t=6.00, the heap will slide from `XPOS`=0 (default position in the middle of the screen) to `XPOS`=+690 (out of screen on the right side)
* The cloud will move from `XPOS`=+264 at t=0 s to `XPOS`=-781 at t=6 s
* All other properties, such as `YPOS`, are not set, since their default values are OK

![](pictures\timing_bulldozer.png)

The final animation looks like this:

![Example_1](pictures\bulldozer.gif)

Remark:
* The bulldozer, heap and cloud images are now 800x600 pixels, just like the background. It would also have been possible to use smaller images for the bulldozer, heap and cloud, without the surrounding empty space. We should then modify `XPOS` and `YPOS` to compensate for the cropping on left and top. This would improve processing speed and memory use. The administrative burden of accounting for the cropped areas can be taken  care of by the spreadsheet. This was not done here to keep the example simple.

<br>

# The `TABLE` command
When the `TABLE` command is used in a script, the name after the `TABLE` refers to the sheet name in which the `TABLE` is defined. A `TABLE` sheet must be formatted as follows:

| <!-- --> | <!-- --> | <!-- --> |
|----------|----------|----------|
| **Column A** | Specifies the time at which the event takes place                 | The time does not have to be ordered. Animate orders the time and interpolates between the given values.<br>If column A does not contain a number, the row is ignored, cells can be used as comment or for internal calculations |
| **Row 1**    | Specifies the name of the item that needs to be modified          | Items cannot be created in a `TABLE`. Items declared in the calling `SCRIPT` can be modified by a `TABLE` <br> If an item name is not declared in the `SCRIPT` that calls the table, it will be ignored by that script.<br>Note that the same table can also be called by another script, in which the item can be declared |
| **Row 2**    | Specifies the property of the item that needs to be modified      | |
| **Cells**    | Specifies the value for the property of the item at the given time | Not every cell in a time/item combination has to have a value.<br>If a cell has no value, the transition happens smoothly between the time/value pairs that are defined |

Remarks:
* A script can call more than one table. 
* More than one script can call the same table. If the table controls an item that is not in the calling script, the item is ignored
* The table is called by the script using the `TABLE` command. A number is required in column A to distiguish the row from a comment row. However, the value of the time before the TABLE command is ignored. 


<br><br>

### **Example 2: Bulldozer with table**

En this example, the same bulldozer animation is created, but this time a `TABLE` is used.

![Main script](pictures\script_bulldozer_1.png)

The movements of all items are now defined in a `TABLE` that is called by the main `SCRIPT`:

![Table](pictures\table_bulldozer_2.png)

Remarks:
* The `TABLE` allows a more compact way to describe transitions
* The times in column A do not have to be ordered
* If numbers are missing for certain points in time, Animate will interpolate between the values that are present
* If `FIRSTFRAME` and `LASTFRAME` are not specified, the animation will run from t=0 until the last point in time specified
* Between time 0 and the first specified value, the property will be constant until the first specified value
* Same for the last specified value until the end of the animation

<br><br>

# Time in Animate

* In Animate, time is specified in seconds
* By definition, the animation starts at 0 seconds and frame 0 corresponds to t=0 s
* The `FRAMERATE` command defines the ratio between frames and seconds
* Rendered frames are stored in the `..\Frames` subdirectory. If this directory does not exist, it will be created by Animate
* By default, the last event in all script is used to determine how long the animation takes
* If a shorter animation is desired, the `LASTFRAME` command can be used to define the duration. Note that this is a frame number and not a time in seconds

<br>

## Debugging
* For debugging purposes, the `FIRSTFRAME` and `LASTFRAME` commands can be used to render a subset of the frames
* Also for debugging purposes, it can be helpful to temporatily use a lower `FRAMERATE` to test if the animation works well
* With a bitmap viewer such as IrfanView, it is easy to browse though the `..\Frames` directory, to check which frames need to be re-rendered
* It is also possible to use `SHOWTIME` to display the time in each frame 

<br>

# Coordinate system
Animate uses the same coordinate system conventions as bitmaps:
* the origin is in the upper left corner
* positive X-axis is to the right
* positive Y-axis is down

<br>

# Types of items
The following types of items are defined:
| <!-- --> | <!-- --> |
|----------|----------|
| `IMAGE`    | retrieves an bitmap from disk and makes it part of the animation   |
| `TEXT`     | displays text                                                      |
| `ASSEMBLY` | an item that is dynamically made up of other items                 |
| `CANVAS`   | similar to an `ASSEMBLY`, but not erased between subsequent frames |
| `MASK`     | used to mask certain parts of the items below the mask             |

<br><br>

## Global commands
The following commands are only relevant for the main script. These commands are ignored for other scripts:

| <!-- --> | <!-- --> |
|----------|----------|
| `FRAMESPERSECOND` | Sets  the number of frames per second of the animation. This is how the floating point number of the time column translates to discrete frames. |
| `FIRSTFRAME`      | This is property for debug purposes. If the total script takes very long to process, only a subset of the frames can be processed. The value following the `FIRSTFRAME` command references the actual frame number, not the time to which the frame corresponds. |
| `LASTFRAME`       | Similar to `FIRSTFRAME` to determine the last frame in the scene that is processed. |
| `SHOWTIME`        | This property is also for debug purposes. Displays the time in the lower left corner of the frames |
| `HIDETIME`        | Hides the time in the lower left corner of the frames |
| `ANIMATEDGIF`     | Creates an animated GIF of the frames that were created, with a filename followed by the `ANIMATEDGIF` command |
| `MOVIE`           | Creates an mpeg movie of the frames that were created, with a filename followed by the `MOVIE` command |

Remarks:
* For these global commands, a number must be present in column A to prevent the row is ignored, but the value of this number is ignored
* For short animations, AnimatedGIF is conventient.
* If the animation is larger, the GIF file will become very large, and Movie is more suitable
* The AnimatedGIF command stores the rendered images in memory and then creates the GIF at the end. This can require much memory. Only the frames between `FIRSTFRAME` and `LASTFRAME` end up in the animated GIF
* The Movie command uses the frames in the `..\Frames` directory. Therefore, all rendered frames are used. If going from a high to a low `FRAMERATE`, ensure to remove the frames that are no longer needed from the `..\Frames` directory before creating the movie
* If you plan to create a movie, please choose a standard movie format, such as 720x576 (PAL) 1280×720 (HD720p) or 1920×1080 (HD1080p), to ensure the output is compatible with standard movie players.
* After the Movie or AnimatedGIF has been created, the `..\Frames` directory can be removed to save disk space

<br><br>

## Properties common to all items
All items have the following properties in common:

Position, scaling and orientation:
| <!-- --> | <!-- --> |
|----------|----------|
| `XPOS`     | The horizontal position on which the item is positioned. The position corresponds to the position of the image as if the rotation of the image is zero and the scale is 100% in horizontal and vertical direction. Note that the origin of the coordinate system is the top left corner of the image, if `XPOS`=0, the left side of the item will be aligned to the left side of the output stream. |
| `YPOS`     | The vertical position on which the item is positioned. Note that the origin of the coordinate system is the top left corner of the image, if `YPOS`=0, the top of the item will be aligned to the top of the output stream. |
| `ROTATION` | The rotation of the item in degrees. Positive angles are counterclockwise.<br>Rotation and scaling is explained in more detail in the following paragraph. |
| `XSCALE`   | The scale of the item in horizontal direction. A value of 1 means that the scale is not changed. |
| `YSCALE`   | The scale of the item in vertical direction.         |

Position, scaling and orientation modifiers:

| <!-- --> | <!-- --> |
|----------|----------|
| `XMOVE`    | The velocity profile of the movements in horizontal direction. Possible values are explained below |
| `YMOVE`    | The velocity profile of the movements in vertical direction |
| `RMOVE`    | The velocity profile of rotation |
| `SXMOVE`   | The velocity profile of scaling in horizontal direction |
| `SYMOVE`   | The velocity profile of scaling in vertical direction |

The position, scaling and orientation modifiers can have the following values:

| <!-- --> | <!-- --> |
|----------|----------|
| `LINEAR`   | the property changes proportional to time                         |
| `CYCLOID`  | the property changes with a smooth start and finish               |
| `SPRING`   | the property moves to the other value with some dynamic overshoot |
| `ACCEL`    | the property accelerates from low speed to high speed             |
| `DAMPED`   | the property starts fast and then decelerates                     |

<br>

The different values can be depicted as follows:

![](pictures\move.png)

Other properties that are common to all items:

| <!-- --> | <!-- --> |
|----------|----------|
| `XPOLE`        | The pole around which the item is rotated and scaled |
| `YPOLE`        | The pole around which the item is rotated and scaled |
| `OPACITY`      | Determines the transparency of the item. A value of 0 means the item is invisible, a value of 1 means the item is opaque | 
| `BRINGTOFRONT` | Changes the Z-order of the item list, bringing this item on top of the others. This property does not need a value |
| `SENDTOBACK`   | Changes the Z-order of the item list, sending this item to the bottom of the list |
| `TEXTCOLOR`    | Specific for text items: the color for the font of the text |
| `FONT`         | Specific for text items: the font for the text              |

<br><br>

## Properties specific to `SCRIPT`, `ASSEMBLY` and `CANVAS`

| <!--     --> | <!-- --> |
|--------------|----------|
| `WIDTH`      | Sets the width of the output frames, measured in pixels                |
| `HEIGHT`     | Sets the height of the output frames                                   |
| `SCRIPT`     | Calls a `SCRIPT` in another worksheet                                  |
| `TABLE`      | Calls a `TABLE` in another worksheet                                   |
| `ASSEMBLY`   | Creates an `ASSEMBLY` item and calls the worksheet where it is defined. The worksheet that is referred to must be formatted as a `SCRIPT` |
| `CANVAS`     | Creates a `CANVAS` item and calls the worksheet where it is defined. The worksheet that is referred to must be formatted as a `SCRIPT` |
| `IMAGE`      | Loads a different image for an `IMAGE` item                            |
| `TEXT`       | Overwrites the text for a `TEXT` item                                  |
| `TIMEOFFSET` | Applies only to `ASSEMBLY` and `CANVAS`. Determines the time difference between the time base of the calling script and the called script. This is useful if the `ASSEMBLY` or `CANVAS` are called more than once with different instances. This way, not all instances need to start at the same moment, but the same `SCRIPT` or `TABLE` can be used to define each instance. |

Remarks:
* Commands and properties are not case sensitive

<br>

# `BRINGTOFRONT` and `SENDTOBACK`

Items are ordered in a certain Z-order, meaning some items are placed in front of other items. An item can be put in front of the other items using `BRINGTOFRONT`, and placed at the back using `SENDTOBACK`. 

![Bring to front](pictures\moon-example-bring-to-front.png)

Remarks:
* This changes the order of items within a `SCRIPT`, `ASSEMBLY` or `CANVAS`. 
* The `ASSEMBLY` or `CANVAS` can also be placed in front of or behind other items in the script in which they are defined.

<br>

### **Example 3: Solar system**

In this example, 5 moons are spinning around a planet. Each moon is sent to the back when it is at the right of the planet, and brought to the front if it is left of the planet.

![Solar system](pictures\solar_system.gif)

<br><br>


# The `IMAGE` item

The `IMAGE` command loads an image from file and links it to an item with a unique name.

The example below creates an item called Glass, and loads different images at 4 and 5 seconds. The image loaded at 3 seconds will  already be loaded as the script starts.

![](pictures\image.png)

All properties that apply to other items, such as `XPOS` and `XSCALE`, also apply to image items.

<br><br>

# The `TEXT` item

The `TEXT` command declares a `TEXT` item and immediately assigns a text value to it. The text value can be changed ad different moments in time.

<br><br>

# Scaling, rotating and the pole

When scaling and rotating an item, the default pole of scaling and rotating is the upper left corner of the item.

The `XPOLE` and `YPOLE` commands can be used to change the coordinates of the pole of rotation and scaling. 

The coordinates provided with `XPOLE` and `YPOLE` are relative to the upper left corner of the item to which they apply.

![Xpole and Ypole](pictures\xpole_ypole.png)

<br><br>

### **Example 4. Rotating text**

In the main `SCRIPT`, three text objects are defined, each with their own location and pole. The location of `XPOLE` and `YPOLE` is defined relative to the top left corner of the item:

![Rotating text main](pictures\rotate_text_main.png)

The rotations are defined in a separate `TABLE`:

![Rotating text table](pictures\rotate_text_table.png)

The result looks like this:

![Rotating text result](pictures\rotating_text.gif)

Here, it can clearly be seen that the location of `XPOLE` and `YPOLE` is defined relative to the top left corner of the item.

<br><br>


### **Example 5: Rotating cloud**

The main `SCRIPT` of the bulldozer example is again modified, now adding the `XPOLE` and `YPOLE` of the cloud. 

Also, a `TABLE` is added which defines  the rotation, scaling and opacity of the cloud.

![Rotating cloud moves table](pictures\rotating_cloud_main_script.png)

The Moves `TABLE` is extended with cloud control:

![Rotating cloud moves table](pictures\rotating_cloud_moves_table.png)

Note that rotation can span more than 360°.

The resulting animation looks like this:

![Rotating cloud animation](pictures\RotatingCloud.gif)

<br><br>


# The `ASSEMBLY` item

The main script can call an `ASSEMBLY`, which is in fact another script which can be used as an item. Multiple levels can be cascaded. The main script can display a single `ASSEMBLY` multiple times, for example with different scaling, position, rotation or mask.

In the following example, the bulldozer from example 1 is animated. This time, the bulldozer is not a static image, but the wheel and the bucket of the bulldozer can move. 

<br>

### **Example 6: Bulldozer with bucket**

In the main script, the global movement of the bulldozer is taken care of. In fact, the main script had only a minor change compared to example 1: instead of declaring the bulldozer as an `IMAGE`, it was now declared as an `ASSEMBLY`.

![Moving bulldozer main](pictures\bulldozer_bucket_main.png)

In the definition of the `ASSEMBLY` of the bulldozer, the bulldozer itself is drawn with the rotating wheel and bucket on it. 

The `ASSEMBLY` is made up of the following items:

![Bulldozer assembly items](pictures\bulldozer_bucket_items.png)

The items are tied together as follows:

![Bulldozer assembly](pictures\bulldozer_bucket_assembly.png)

The result looks like this:

![Moving bulldozer](pictures\bulldozer_bucket.gif)

<br><br>

<br><br>

# Working with `TIMEOFFSET`

Sometimes it is useful to work with multiple instances of an `ASSEMBLY` or `CANVAS`, but each instance must have an offset in time.

For each instance, it is possible to call the `TIMEOFFSET` to specify that the instance must start at a different moment in time.

The offset given can both be:
* **positive**: the instance starts later than the calling script, or 
* **negative**: the instance starts earlier

As a simple reminder: if a `TIMEOFFSET` of +3 seconds is specified, the called `ASSEMBLY` or `CANVAS` starts at 3 sec.

To let the item start later than the calling script, the offset is subtracted from the time in the calling script. In the example below, the called script starts 3 seconds later than the calling script:

| Calling<br>script | Called<br>script |
|-------------------|------------------|
|     0 sec         |    -3 sec        |
|     1 sec         |    -2 sec        |
|     2 sec         |    -1 sec        |
|     3 sec         |     0 sec        |
|     4 sec         |     1 sec        |
|     5 sec         |     2 sec        |

This demonstrates that negative times in the called `ASSEMBLY` or `CANVAS` can occur. It is possible to also provide negative times in the called scripts to define the behaviour for negative values of the time.

<br>

### **Example 7: Bouncing balls**

In this example, three balls are displayed which bounce on the ground. As each ball bounces, the bottom of the ball is compressed and the ball becomes wider.

In the main script, three balls are declared, each with their own `XPOS` and `TIMEOFFSET`:

![Canvas example animation](pictures\bouncing_balls_main.png)

The ball assembly consists of two half circles, one flipped upside down:

![Canvas example animation](pictures\bouncing_balls_ball.png)

The bouncing and scaling of the ball is defined in a table:

![Canvas example animation](pictures\bouncing_balls_bounce.png)

This produces the following animation:

![Canvas example animation](pictures\bouncing_balls.gif)

# The `MASK`

A `MASK` is used to reveil some parts of the underlying stack, or conceil others. 

The `MASK` accepts a filename as an argument. It works in the following way:
* At the white parts of this mask, the parts of the underlying picture will be revealed
* At the black parts of this mask, the parts of the underlying picture will become transparent
* The grey parts will partly reveal the underlying picture.

At different moments in time, a different bitmap can be loaded as `MASK`.

<br>

### **Example 8: Two cylinders**

In the following example, two hydraulic cylinders are connected by a tube. In the tube, the fluid moves faster than in the cylinders. Also, the bubbles need to follow the trajectory of the tube as they are going from one cylinder to the other. 

![Bubble sections](pictures\two_cylinders.gif)

The stack of this animation is built up as follows:

![Cylinder stack](pictures\two_cylinders_stack.png)

The fluid system is divided in 7 sections
1. cylinder 1
1. straight tube section
1. bended tube section
1. straight tube section
1. bended tube section
1. straight tube section
1. cylinder 2

![Bubble sections](pictures\two_cylinders_sections.png)

In the `SCRIPT` bubbles, 7 bubble items are declared, each with an image with random bubbles, selected from 3 images. An additional sheet 'bubble planning' is used to plan out the location, orientation and speed of each group of bubbles. The main `SCRIPT` script shows a background image, the `ASSEMBLY` with the bubbles, and two pistons.

The bubbles `ASSEMBLY` shows 7 `IMAGE`s of bubbles, each driven by their own `TABLE` which controls location and orientation. On top of the 7 `IMAGE`s, a `MASK` covers the bubbles that are outside the tube. The location and orientation of the bubbles in each of the `TABLE`s is in turn controlled by the sheet 'bubble planning', which just takes care of the mathematics for each section.

![Bubble sections](pictures\two_cylinders_correlations.png)

<br><br>

# The `CANVAS`

A `CANVAS` is like an `ASSEMBLY`; the difference is that the image is not erased in between frames. A `CANVAS` can be useful as a drawing board, to draw text or a graph.

<br>

### **Example 9: Canvas**

The stack for this example is as follows:

![Canvas example stack](pictures\canvas_example_stack.png)

This results in the following animation:

![Canvas example animation](pictures\canvas_demo.gif)

# Reusing a `TABLE` more than once

Sometimes it is useful to plan out the transformations well. In the example below, a single table is used twice on different items that both need to follow the same path. This way, duplicating information is avoided.

### **Example 10: Car**

This example uses three images: 
1. background
1. tires of the car
1. car itself

The car needs to follow a certain route on the road. The imprint of the tires is recorded on a canvas. The hierarchy is built up as follows:

![Car hierarchy](pictures\car-architecture.png)

In this case, the car and the tires have the same image dimensions and are both named 'Vehicle'. Also, the `SCRIPT` 'Main' and the `CANVAS` 'Tracks' both call the `TABLE` 'Route'. In this table, location and orientation of the 'Vehicle' item is controlled. Since both the tires and the car are called 'Vehicle' in their respective worksheers, the `TABLE` modifies location and orientation of both items in exactly the same way.

The main `SCRIPT`:

![Car main script](pictures\car-main.png)

The `CANVAS` named Tracks:

![Car tracks](pictures\car-tracks.png)

The `TABLE` named Route:

![Car route](pictures\car-route.png)

The time intervals are calculated based on a fixed speed in linear movements, and a fixed amount of time for each curve.

The result:

![Car route](pictures\car_demo.gif)

# Adding a camera

In the next example, a higher level of hierarchy is added on top of the main `SCRIPT`. The main `SCRIPT` in the previous example is now an `ASSEMBLY` 'map' which is used twice: once in the `SCRIPT` 'main', and once in an `ASSEMBLY` named 'radar'. 

The 'Radar' `ASSEMBLY` is just 250x250 pixels, and it has circular mask. Below the circular `MASK`, the 'Map' `ASSEMBLY` is moving in X and Y direction, such that car is below the center of the circular mask.

In the 'Main' `SCRIPT`, the 'Map' `ASSEMBLY` is displayed just like in the previous example. On op of the 'map', several items are displayed:
* a magnifying glass, which moves with the car
* the 'Radar' `ASSEMBLY` which is scaled down and rotates with the orientation of the car
* a circle on top of the radar image

### **Example 11: Camera**

The hierarchy is now more complex:

![](pictures\camera-hierarchy.png)

In the 'main' `SCRIPT`, the following items are created:
1. Glass: the magnifying glass which hovers over the car
1. Circle: a black circle around the radar screen
1. Radar: the small radar screen in the bottom left corner
1. FixedMap: the `ASSEMBLY` 'map' with the map and the driving car. It is now renamed 'FixedMap' to prevent the `TABLE` 'table' from modifying it's position

![](pictures\camera-main.png)

The 'Radar' `ASSEMBLY` basically moves the 'Map' `ASSEMBLY` under the mask.

![](pictures\camera-radar.png)

The 'Map' `ASSEMBLY` only has the background map, the tyres `CANVAS` and the Car:

![](pictures\caera-map.png)

The 'Route' `TABLE` controls all movements and rotations:

![](pictures\camera-table.png)

The result:

![](pictures\camera_demo.gif)
