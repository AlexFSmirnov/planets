# Planets
Simulation of arbitrary planets and their orbits. Each planet has its mass, initial speed and size. Thanks to the global central source of gravity and attraction between planets themselves, the initially random arrangement of planets is slowly moving towards an ideal solar system.

Changing variables in `CONSTANTS` section of the code may result in interesting things.

> sim_3d.py works, but is not fully finished yet.

## Examples
### 2D
You can start simple and just draw the planets:
![4planets](/example_gifs/4planets.gif)

Or you can turn on the `draw_vecs` trigger and display the speed (blue) and gravity force (red) vectors:
![4planets-vectors](/example_gifs/4planets-vectors.gif)

Or even better - turning on the `draw_tracks` trigger will result in planets leaving a trace after themselves:
![4planets-tracks](/example_gifs/4planets-tracks.gif)

The length of this trace, of course, can be changed:
![4planets-tracks-long](/example_gifs/4planets-tracks-long.gif)

Experiment! Here are just a few examples of what you can get:
![atom](/example_gifs/atom.gif)
![15planets](/example_gifs/15planets-tracks.gif)
![35planets](/example_gifs/35planets-tracks.gif)

### 3D
> 3D part is not fully finished yet.

3D is very similar to 2D, except it requires much more computing power and is less entertaining due to the lack of functionality. Though, it still can simulate planets and gravity forces between them:
![black hole](/example_gifs/black_hole.gif)
