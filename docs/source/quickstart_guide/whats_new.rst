What's new in version 2
=======================

The AtLAST Sensitivity Calculator was first developed as part of the AtLAST Design Study (funded by the European Union's Horizon Europe research and innovation programme under grant agreement No. 951815). As part of the AtLAST2 Design Consolidation Phase (funded by the European Union's Horizon Europe research and innovation programme under grant agreement No. 101188037), a new version of the code has been developed. The key objective of this new version is to provide a calculator that takes into account the variety of instruments that are being developed for current (sub-)mm telescopes so that science users can better constrain their science cases.

Code refactor
+++++++++++++
Refactored the codebase to have a more modular structure for the calculation process. In the
previous version, the code was structured in a singular streamlined process that made it difficult
to modify the calculation process. The new structure allows for better organisation of the
code and makes it easier to add new instruments or to modify the calculation process in the
future. These changes include separating the calculation input parameters into different classes 
based on their category, and introducing instrument modules where instrument data and methods are 
stored (see :ref:`Class Structure <class structure>` for high level view of the new structure).

New instruments
+++++++++++++++
Introduced instrument modules where instrument data and methods are stored. The users can 
select the instrument they want to use and the relevant data and methods for that instrument 
will be used in the calculations (see section  in :ref:`Instrument Selection <instrument selection>`
for more details.). This is a significant change from the previous version where
all of the data and methods for a generic heterodyne instrument were stored in a single module. 
This new structure makes it easier to add new instruments in the future (see section in 
:ref:`Add a New Instrument <add new instrument>`).

Changes to the treatment of the atmosphere
++++++++++++++++++++++++++++++++++++++++++