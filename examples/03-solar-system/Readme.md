# Example 3: Solar system

In this example, 5 moons are spinning around a planet. 

![Solar system](solar_system.gif)

Each moon:
* is sent to the back using `SENDTOBACK` when it is at the right of the planet, and 
* brought to the front using `BRINGTOFRONT` if it is left of the planet.

![Bring to front](Design/moon-example-bring-to-front.png)
