### Description
This repo contains my work in basic I/O and processing of a sample of radar data. The first goal was to write a reader capable of handling the provided CSV file as well as any other file of similar nature but representing a different scenario. The second goal was to find the radar object in the sample data which most closely matched the reference and characterize its positional and velocity errors.

The original sample data contained range, velocity, and angular GPS measurements for 2000+ time steps.

<center>
<img src="reference.png" alt="reference" width="900px" height="300px">
</center>

### Usage
At a terminal, navigate to the directory that contains `proc_sample.py` and type

```bash
python proc_sample.py file [-h] [-v]
 ```
 
The `file` parameter should be the file name including path of the CSV file. Arguments in brackets are optional.
 
### Dependencies
The only dependency of `proc_sample` is [NumPy](http://www.numpy.org/).
 
### Results
It turns out that the longest tracked radar object `aObject[32]` best matches the reference. Here's the output of running `proc_sample` on the sample file provided in verbose mode:

```bash
> python proc_sample.py Scenario_crossing_left_to_right_50mph.csv -v
> Number of headers: 287
> Number of radar objects: 40
> Number of time steps: 2021
> Longest tracked radar object: aObject[32]
```

#### Positional errors
The context of this discussion assumes that both the GPS used to track the reference and the radar object identification have sub-meter, even sub-centimeter location precision. For someone like myself coming from a meteorological remote sensing background this sounds more like a fantasy, so I'm interested in learning more about this.

Below is a plot of the reference trajectory versus that of `aObject[32]`. It is clear not all trajectory data of `aObject[32]` is valid, and these time steps are ignored in my analysis.
 
![](./reference_object_trajectory.png)
  
The distributions of the trajectory differences and absolute differences between `aObject[32]` and the reference are both bimodal, indicating trajectory errors are dependent on at least one independent variable. The figure below was created by computing these difference fields and counting occurrences in 10 cm bins. Due to the bimodality, the mean and standard deviations reported in the plot should be ignored since they characterize the whole; rather a mean and standard deviation should be computed for each separate distribution.

![range_errors.png](./range_error.png)

I originally speculated the bimodality was the result of beam broadening offsetting the position, e.g., smaller resolution volume closer to host vehicle (peak around 0 cm), larger resolution volume further from host vehicle (peak around 60 cm). However, upon further inspection, it appears the bimodality is due to directional miscalibration, where the position of objects approaching the host vehicle are systematically overestimated, on average by approx. 60 cm. This can be seen in the two-dimensional density plot between range differences and reference velocity. Range data is binned every 10 cm and velocity data is binned every 0.5 kph. The two distributions are clearly separated in this plot, one distribution for objects moving towards the host vehicle and one distribution for objects moving away from the host vehicle.

![](./velocity_range_bias.png)

#### Velocity errors
The convention for this data set has the typical Cartesian (x, y) coordinates rotated 90 deg counterclockwise, so positive x is northward and positive y is westward. Objects moving towards the host vehicle should exhibit negative velocity, and objects moving away from the vehicle should exhibit positive velocity. With this in mind, I computed each radar object's radial velocity using the following two equations.

![](https://latex.codecogs.com/gif.latex?%5Cbg_white%20%5Ctan%28%5Ctheta%29%20%3D%20%5Cfrac%7B%5CDelta%20x%7D%7B%5CDelta%20y%7D%20%7E%7E%2C%7E%7E%20V_r%20%3D%20V_x%20%5Csin%28%5Ctheta%29%20&plus;%20V_y%5Ccos%28%5Ctheta%29)

Below is a plot of the reference velocity versus that of `aObject[32]`. It is interesting to note the relative noisiness in the GPS velocity data, e.g., compared to the GPS range data. I'm interested in learning more about this and the reasons behind it.

![](./reference_object_velocity.png)

The distributions of the velocity differences and absolute differences between `aObject[32]` and the reference are shown in the figure below. The velocity difference distribution is Gaussian with a mean of -0.05 kph and standard deviation of 1.80 kph. Assuming a 1/100th kph is approaching sensor precision, there appears to be no significant systematic bias in radar object velocity.

![](./velocity_error.png)
