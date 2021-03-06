# Example 7: Bouncing balls

In this example, three balls are displayed which bounce on the ground. As each ball bounces, the bottom of the ball is compressed and the ball becomes wider.

![Canvas example animation](bouncing_balls.gif)

In the 'main' `SCRIPT`, three balls are declared, each with their own `XPOS` and `TIMEOFFSET`. The moving and scaling of each ball is handled just once by the 'Ball' `SCRIPT` and the 'Bounce' `TABLE`:

![Canvas example animation](Design/bounce_hierarchy.png)

Tha 'main' `SCRIPT` is defined as follows:

![Canvas example animation](Design/bouncing_balls_main.png)

The ball assembly consists of two half circles, one flipped upside down:

![Canvas example animation](Design/bouncing_balls_ball.png)

The bouncing and scaling of the ball is defined in the `TABLE` 'Bounce':

![Canvas example animation](Design/bouncing_balls_bounce.png)

Since in the 'Main' `SCRIPT` a `TIMEOFFSET` up to 2.5 s is used, the motion of the ball in the 'Bounce' `TABLE` must also be defined for times up to -2.5 s.

Also note that the `YMOVE` value is changed to `ACCEL` if the ball reaches the top and to `DAMPED` as it bounces on the ground. This way, a parabolic bounce is approximated.