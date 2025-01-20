# <p align="center"> HoUnai - Tools Warehouse - </p>

During this time that I have been working with Houdini, there are certain occasions in which I am presented with repetitive tasks that can be automated. 
I will use this space to share such tools, they can be tools that I have developed for certain tasks within a company (implemented in its pipeline) or simply tools that I have wanted to do at a certain time, without having to supply a particular need. 


## Arnold to Mantra converter
While working in a previous company, sometimes we would get a layout that was buld-up in Maya completely for Arnold. There were days, where lighting artists would spend hours even days converting lights from Arnold to Mantra, because the pipeline was designed to render everything that was coming out from Houdini, in Mantra.

To fill that necessity, I developed <a href="https://github.com/ularrarte/Hounai/blob/main/converter.py">Terrenator</a>, a tool that allows to select as many lights as the user wants and with just one click they will be converted to Mantra capable lights. 
Note: The intensity of the lights will have to be checked by the user, since it is impossible to establish an equivalence between both render engines in terms of luminance.


## Upgrde version and update output paths
Another company situation: No matter what, before sending some final *.exr* renders to the farm, your were forced to create a new version of the file. At that moment, the original file is locked and stored into the company storage as part of the normal pipeline work. 
This situation was a bit frustrating, as sometimes you wanted to have two similar version of the shot under the same father version: 

- Case 1: v16.0 with 1 time scale.
- Case 2: v16.1 with 1.5 time scale and 3 times density.

To fix this I created <a href="https://github.com/ularrarte/Hounai/blob/main/Updator.py">Updator</a>, a tool that, taking into account the version in which the user is, allows to create intermediate versions, updating also all the necessary paths in the OUT nodes (the location of the files was something quite robust within the pipeline and could not be altered). 
In order to make the tool user-friendly, a graphical interface was also developed using PySide2.
