


# <p align="center"> HoUnai - Tools Warehouse - </p>
During my time working with Houdini, I've encountered various occasions where repetitive tasks could be automated. I want to take this opportunity to share some tools I've developed, either for specific tasks within a company or simply as a personal projects.

## Arnold to Mantra converter

In a previous role, we sometimes received layouts created in Maya that were specifically built up for Arnold. This often meant that lighting artists would spend hours, sometimes even days, converting lights from Arnold to Mantra because our pipeline was set up to render everything from Houdini with Mantra.

To address this issue, I developed <a href="https://github.com/ularrarte/Hounai/blob/main/converter.py">Terrenator</a>, a tool that enables users to select multiple lights and convert them to Mantra-compatible lights with just one click. It’s important to note that the user must check the intensity of the lights afterward, as it is challenging to establish a direct equivalence between the two rendering engines regarding luminance.


## Upgrde version and update output paths

Another company situation: No matter what, before sending some final *.exr* renders to the farm, we were forced to create a new version of the file before it could be sent. While the original file was locked and archived in our company storage as part of the pipeline, this could be quite frustrating, especially when needing two similar versions of a shot under the same parent version:

- Case 1: v16.0 with 1 time scale.
- Case 2: v16.1 with 1.5 time scale and 3 times density.

To alleviate this problem, I developed <a href="https://github.com/ularrarte/Hounai/blob/main/Updator.py">Updator</a>; this tool allows users to create intermediate versions based on their current version while simultaneously updating all necessary paths in the OUT nodes (the location of the files was something quite robust within the pipeline and could not be altered). 
To enhance usability, I also designed a graphical interface using PySide2.

## Add points or objects to a any surface through viewport

<a href="https://github.com/ularrarte/Hounai/blob/main/normaller.py">This</a> was the first experiment I conducted while I was learning Houdini to understand how to integrate Python into a Houdini tool. 
I developed a tool using viewer states that allows me to position any object (or point) tangent to a surface using only the mouse. The tool also enables me (just with the mouse) to change the object's orientation and size post-creation. Additionally, once the object is positioned, all its attributes —such as position, scale, orientation, and type— can be accessed through the multiparm created in the node.

A quick video of how the tool works can be checked <a href="https://www.youtube.com/watch?v=B2-zxt-H1hA">here</a>. 


##

I will use this last part of the post to mention other projects, even if they don't focus on the world of special effects. I believe this can help provide some context about my background.

- <a href="https://github.com/grupo9web/Neon-Rush">Neon Rush</a>
- <a href="https://github.com/grupo9web/GualAPP">GualApp</a>


