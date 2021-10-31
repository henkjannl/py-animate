# Example 3: Solar system

In this example, 5 moons are spinning around a planet. 

![Solar system](solar_system.gif)

Each moon:
* is sent to the back using `SENDTOBACK` when it is at the right of the planet, and 
* brought to the front using `BRINGTOFRONT` if it is left of the planet.

![Bring to front](Design/Order.png)

The main `SCRIPT` 'Script' just declares the background and the 'Planets' `ASSEMBLY`:

|    |  A  |  B  |  C  |  D  |
|:--:|:---:|:---:|:---:|:---:|
| **1** | Time | Command | Item | Value |
| **2** | -6 | FramesPerSecond | 15 |  |
| **3** | -5 | Width | 800 |  |
| **4** | -4 | Height | 600 |  |
| **5** | -3 | AnimatedGIF | solar_system.gif |  |
| **6** |  |  |  |  |
| **7** | -2 | Image | BackgroundL | Background.png |
| **8** | -1 | Image | BackgroundR | Background.png |
| **9** | -1 | Assembly | Planets | Planets |
| **10** |  |  |  |  |
| **11** | 0 | BringToFront | Planets |  |
| **12** |  |  |  |  |
| **13** | 0 | Xpos | BackgroundL | 0 |
| **14** | 5 | Xpos | BackgroundL | 160 |
| **15** | 0 | Xpos | BackgroundR | -800 |
| **16** | 5 | Xpos | BackgroundR | -640 |


This is implemented in the `SCRIPT` 'Planets':

|    |  A  |  B  |  C  |  D  |
|:--:|:---:|:---:|:---:|:---:|
| **1** | Time | Command | Item | Value |
| **2** | -27.5 | Width | 800 |  |
| **3** | -26.5 | Height | 600 |  |
| **4** |  |  |  |  |
| **5** | -25.5 | Image | Planet | Planet.png |
| **6** | -24.5 | Xpos | Planet | 206 |
| **7** | -23.5 | Ypos | Planet | 106 |
| **8** |  |  |  |  |
| **9** | -22.5 | Image | Moon01 | Planet.png |
| **10** | -21.5 | Image | Moon02 | Planet.png |
| **11** | -20.5 | Image | Moon03 | Planet.png |
| **12** | -19.5 | Image | Moon04 | Planet.png |
| **13** | -18.5 | Image | Moon05 | Planet.png |
| **14** |  |  |  |  |
| **15** | -17.5 | Xpole | Moon01 | 194 |
| **16** | -16.5 | Xpole | Moon02 | 194 |
| **17** | -15.5 | Xpole | Moon03 | 194 |
| **18** | -14.5 | Xpole | Moon04 | 194 |
| **19** | -13.5 | Xpole | Moon05 | 194 |
| **20** |  |  |  |  |
| **21** | -12.5 | Ypole | Moon01 | 194 |
| **22** | -11.5 | Ypole | Moon02 | 194 |
| **23** | -10.5 | Ypole | Moon03 | 194 |
| **24** | -9.5 | Ypole | Moon04 | 194 |
| **25** | -8.5 | Ypole | Moon05 | 194 |
| **26** |  |  |  |  |
| **27** | 0 | Table | Moonlocations |  |
| **28** |  |  |  |  |
| **29** | 0 | Rotation | Moon01 | 0 |
| **30** | 0 | Rotation | Moon02 | 0 |
| **31** | 0 | Rotation | Moon03 | 0 |
| **32** | 0 | Rotation | Moon04 | 0 |
| **33** | 0 | Rotation | Moon05 | 0 |
| **34** |  |  |  |  |
| **35** | 5 | Rotation | Moon01 | 720 |
| **36** | 5 | Rotation | Moon02 | -360 |
| **37** | 5 | Rotation | Moon03 | 720 |
| **38** | 5 | Rotation | Moon04 | -720 |
| **39** | 5 | Rotation | Moon05 | 360 |
| **40** |  |  |  |  |
| **41** | -5 | BringToFront | Moon01 |  |
| **42** | -4 | BringToFront | Moon02 |  |
| **43** | -3 | BringToFront | Moon03 |  |
| **44** | -2 | BringToFront | Moon04 |  |
| **45** | -1 | BringToFront | Moon05 |  |
| **46** |  |  |  |  |
| **47** | 0 | BringToFront | Moon01 |  |
| **48** | 1 | BringToFront | Moon02 |  |
| **49** | 2 | BringToFront | Moon03 |  |
| **50** | 3 | BringToFront | Moon04 |  |
| **51** | 4 | BringToFront | Moon05 |  |
| **52** | 5 | BringToFront | Moon01 |  |
| **53** |  |  |  |  |
| **54** | -7.5 | SendToBack | Moon01 |  |
| **55** | -6.5 | SendToBack | Moon02 |  |
| **56** | -5.5 | SendToBack | Moon03 |  |
| **57** | -4.5 | SendToBack | Moon04 |  |
| **58** | -3.5 | SendToBack | Moon05 |  |
| **59** |  |  |  |  |
| **60** | -2.5 | SendToBack | Moon01 |  |
| **61** | -1.5 | SendToBack | Moon02 |  |
| **62** | -0.5 | SendToBack | Moon03 |  |
| **63** | 0.5 | SendToBack | Moon04 |  |
| **64** | 1.5 | SendToBack | Moon05 |  |
| **65** |  |  |  |  |
| **66** | 2.5 | SendToBack | Moon01 |  |
| **67** | 3.5 | SendToBack | Moon02 |  |
| **68** | 4.5 | SendToBack | Moon03 |  |



The locations of the planets are controlled in a separate `TABLE` 'Moonlocations', which are essentially just `SIN` and `COS` functions with a different phase:

|    | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | 
|:--:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **1** | t | phi | Moon01 | Moon02 | Moon03 | Moon04 | Moon05 |  | Moon01 | Moon02 | Moon03 | Moon04 | Moon05 |  | Moon01 | Moon02 | Moon03 | Moon04 | Moon05 |  | Moon01 | Moon02 | Moon03 | Moon04 | Moon05 | 
| **2** |  |  | Xpos | Xpos | Xpos | Xpos | Xpos |  | Ypos | Ypos | Ypos | Ypos | Ypos |  | Xscale | Xscale | Xscale | Xscale | Xscale |  | Yscale | Yscale | Yscale | Yscale | Yscale | 
| **3** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
| **4** |  |  | -1.57 | -0.31 | 0.94 | 2.19 | 3.4 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
| **5** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 
| **6** | 0 | 0 | -74 | 119.47 | 432.52 | 432.52 | 119.47 |  | 100 | 119.02 | 111.75 | 88.24 | 80.97 |  | 0.2 | 0.05 | 0.11 | 0.28 | 0.34 |  | 0.2 | 0.05 | 0.11 | 0.28 | 0.34 | 
| **:** | : | : | : | : | : | : | : | : | : | : | : | : | : | : | : | : | : | : | : | : |
