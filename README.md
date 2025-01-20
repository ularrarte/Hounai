


# <p align="center"> HoUnai - Tools Warehouse - </p>
During my time working with Houdini, I've encountered various occasions where repetitive tasks could be automated. I want to take this opportunity to share some tools I've developed, either for specific tasks within a company or simply as a personal projects.

## Arnold to Mantra converter

In a previous role, we sometimes received layouts created in Maya thaw were specifically build-up for Arnold. This often meant that lighting artists would spend hours, sometimes even days, converting lights from Arnold to Mantra because our pipeline was set up to render everything using Mantra in Houdini.

To address this issue, I developed <a href="https://github.com/ularrarte/Hounai/blob/main/converter.py">Terrenator</a>, a tool that enables users to select multiple lights and convert them to Mantra-compatible lights with just one click. It’s important to note that the user must check the intensity of the lights afterward, as it is challenging to establish a direct equivalence between the two rendering engines regarding luminance.


## Upgrde version and update output paths

Another company situation: No matter what, before sending some final *.exr* renders to the farm, we were forced to create a new version of the file before it could be sent. While the original file was locked and archived in our company storage as part of the pipeline, this could be quite frustrating, especially when needing two similar versions of a shot under the same parent version:

- Case 1: v16.0 with 1 time scale.
- Case 2: v16.1 with 1.5 time scale and 3 times density.

To alleviate this problem, I developed <a href="https://github.com/ularrarte/Hounai/blob/main/Updator.py">Updator</a>, his tool allows users to create intermediate versions based on their current version while simultaneously updating all necessary paths in the OUT nodes (location of the files was something quite robust within the pipeline and could not be altered). 
To enhance usability, I also designed a graphical interface using PySide2.




