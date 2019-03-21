## Visualization Tool for Protein Validation in Chimera Platform

#### Install Biopython in Chimera

* Download [biopython](https://biopython.org/wiki/Download)
* python setup.py install --home=/Applications/Chimera.app/Contents/Frameworks/Python.framework/Versions/2.7/
* Enter /Applications/Chimera.app/Contents/Frameworks/Python.framework/Versions/2.7/lib, "mv ./python/\* ./python2.7", "rm -r ./python"
* Restart Chimera, open IDLE, type "import Bio"

#### Install Tool in Chimera

* python install /Applications/Chimera.app

#### Implementation

* Load protein in Chimera
* “Tools -> Utilities -> ECSU Label”, Open the validation tool
* Choose a chain in the drop-down menu
* Enter a threshold value
* Click "Check" button

#### Reference

* Modeling, Simulation and Visualization Student Capstone Conference 2019
