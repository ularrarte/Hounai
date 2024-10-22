# HoUnai - Tools Warehouse -

During this time that I have been working with Houdini, there are certain occasions in which I am presented with repetitive tasks that can be automated. 
I will use this space to share such tools, they can be tools that I have developed for certain tasks within a company (implemented in its pipeline) or simply tools that I have wanted to do at a certain time, without having to supply a particular need. 

### Converting Lights
When I was working in a previous company, sometimes we would get a layout that was completely done in Maya, for the Arnold render engine. There were days, where lighting colleagues would spend hours converting lights from Arnold to Mantra, because the pipeline was designed to render everything that was coming out from Houdini, in Mantra.

That's why I developed <a href="https://github.com/ularrarte/Hounai/blob/main/converter.py">Terrenator</a>, a tool that allows to select as many lights as the user wants and with just one click they will be converted to Mantra capable lights. 
Note: The intensity of the lights will have to be checked by the user, since it is impossible to establish an equivalence between both render engines in terms of luminance.
