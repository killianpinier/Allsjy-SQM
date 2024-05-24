# Allsky-SQM

The SQM software takes SQM reading at a regular interval of time. It uses the
libcamera-still command to take pictures, as well as a machine learning model to
determine the brightness value of each individual region of the image.
The user can create and select a configuration every time they run a new session (when
the run button is clicked). A configuration allows to select a name, a description, and a
reading time interval. It also gives the possibility to choose a grid for the image in order
to divide it into smaller regions. When the SQM takes a reading, it will calculate the
average brightness for each of them. The configuration page also allows to remove
regions of the sky that do not need to be processed for the brightness calculation (for
example: obstacles, or the corners of the image).
The homepage displays the last SQM reading as an image. This image is divided in a
grid (defined in the configuration page) where SQM values are written on top of each
region. A blue mask is also applied to get a visual representation of the sky brightness.
The software applies this mask by applying the highest intensity to the brightest region,
and the lowest intensity to the lest bright region. This gives a normalization which is
then applied to the other regions. Note that the regions that were unselected during the
creation of the selected configuration are not taken into the normalization.
