### Description
This repo contains my work in basic I/O and processing of a sample of radar data. The first goal was to write a reader capable of handling the provided CSV file as well as any other file of similar nature but representing a different scenario. The second goal was to find the radar object in the sample data which most closely matched the reference and characterize its positional and velocity errors.

### Usage
At a terminal, navigate to the directory that contains `proc_sample.py` and type

```bash
python proc_sample.py file [-h] [-v]
 ```
 
 Arguments in brackets are optional.
 
### Dependencies
The only dependency of `proc_sample` is [NumPy](http://www.numpy.org/).
 
### Results
It turns out that the longest tracked radar object `aObject[32]` corresponded to the reference.
