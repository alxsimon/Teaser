# [EDIT]
This is a fork from the main Teaser repository for my own needs.
Modifications here are targeted for specific uses and may not work in your settings.

The main changes are:
    - create a self-contained singularity image to run Teaser
    - manage mappers and tools with conda
    - include new mappers (e.g. bwa-mem2, minimap2)

The following original directives may not apply in this fork.

To build the singularity image
```
sudo singularity build Teaser.sif Teaser.def
```

To run the easiest way right now is to use an overlay folder with singularity
(careful you need root access):
```
mkdir teaser_overlay

sudo singularity exec --overlay teaser_overlay /opt/Teaser/Teaser.sif \
bash -c 'cd /Teaser && ./teaser.py example_ecoli.yaml'

ll teaser_overlay/upper/Teaser/reports/example_ecoli
```

# Teaser
Teaser analyzes the performance of read mappers based on a data set provided by you. After you enter key characteristics such as read length and reference genome, Teaser will simulate read data including the gold standard alignment. After the simulation, Teaser automatically runs and evaluates each mapper for the selected parameters and summarizes the results in a report. Teaser also supports benchmarking read mappers on real data or custom simulations, as well as testing new mappers and custom parameter sets. You can start using Teaser right now using our web application, or download and install it to use all advanced features.

* [Try the Teaser Web Application](http://teaser.cibiv.univie.ac.at)

## Documentation
The [GitHub Wiki](https://github.com/Cibiv/Teaser/wiki) contains all information on how to start benchmarking mappers with Teaser as well as customization and extension options.

## Quick Start

### Get Teaser
First, get Teaser and enter the Teaser directory with:
```
git clone https://github.com/Cibiv/Teaser.git
cd Teaser
```

### Run Teaser using [Docker](https://www.docker.com/)
To run Teaser with Docker use the following command:
```
docker build -t teaser_git . && docker run -v $(pwd):/teaser -it teaser_git "/usr/bin/teaser_shell.sh"
```

### Or: Run Teaser directly on your system
To install Teaser directly on your system without using Docker, follow the instructions below. For all installation requirements, see the [Installation](https://github.com/Cibiv/Teaser/wiki/Installation) page in our wiki.

To install Teaser use the following command:
```
./install.py
```

Important: Teaser requires an internet connection during installation in order to download the mappers.

### Benchmarking Mappers on an E. coli data set

To see if everything is working, you can try benchmarking mappers for a simple E. coli dataset using:

```
./teaser.py example_ecoli.yaml
```

To start the Teaser [graphical interface](https://github.com/Cibiv/Teaser/wiki/Web-Browser-Interface) use:

```
./server.py
```

Then head to `http://localhost:8888` in a web browser of your choice.

## Citation
If you use Teaser to optimize read mapping in your study, please consider citing: 

[Smolka M, Rescheneder P, Schatz MC, von Haeseler A and Sedlazeck FJ. Teaser: Individualized benchmarking and optimization of read mapping results for NGS data. Genome Biology 2015, 16:235 (22 October 2015).](http://www.genomebiology.com/2015/16/1/235) DOI: 10.1186/s13059-015-0803-1

## License
Teaser is made available under the MIT License.
