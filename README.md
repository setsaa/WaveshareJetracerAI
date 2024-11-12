# Reinforcement Learning on Jetson Nano

Run your reinforcement learning (RL) model on a Jetson Nano.

## Preface

This project was a part of a postgraduate subject at the University of Technology Sydney called `43008 Reinforcement Learning`. Knowledge of Python is expected, as is some familiarity with Linux. If the commands `cd`, `ls` and `sudo` doesn't scare you, you should be good to go.

## Introduction

A Nvidia Jetson Nano is a small computer used for AI IoT devices. A common usecase for students is applying machine learning models to robotics such as remote controlled (RC) cars.

The software for the car we'll be using is a modified version of [Nvidia JetPack SDK](https://developer.nvidia.com/embedded/jetpack) which comprises of 3 components:

- **Jetson Linux** is the name of the distro of [Ubuntu](https://en.wikipedia.org/wiki/Ubuntu) (operating system) the car is using.
- **Jetson AI Stack** is a [CUDA](https://en.wikipedia.org/wiki/CUDA) Accelerated AI stack which includes a complete set of libraries for acceleration of GPU computing, multimedia, graphics, and computer vision.
- **Jetson Platform Services** is a collection of services.

WaveShare is a company that makes the JetRacer AI, a DIY RC car designed to connect with a Jetson Nano computer.

> [!NOTE]
> The WaveShare JetRacer AI is not the same thing as the WaveShare JetRacer ROS AI, which uses a Raspberry Pi and which doesn't do AI processing on-device.

## Requirements

Find a list of requirements in the `requirements.txt` file. Note that because of the fickle nature of the JetRacer, the specific version of each package is very important to maintain. Read the FAQ if you're struggling with installing certain packages.

> [!WARNING]
> Jetson Nano uses an [ARM-based architecture](https://en.wikipedia.org/wiki/ARM_architecture_family), which is different from most Windows machines. This means you have to be careful to chose the correct version of any given package. Further, the Jetson Nano takes advantage of the CUDA platform, meaning some packages that utilise this technology will need to be built and often can't be installed easily using package managers like Poetry or pip. This isn't something you typically have to worry about as JetPack will already have most tools included, but if you have to change the version of a package you need to worry about building it properly.

## Installing JetPack on the JetRacer

_I highly suggest having a display, keyboard and mouse at hand when first setting up the JetRacer._

Download the pre-built JetRacer image from WaveShare [here](https://www.waveshare.com/wiki/JetRacer_AI_Kit#Guide_of_DonkeyCar), it should be around 8.19 GB. Follow the instructions on their website to write the JetRacer image to an SD card. I reccomend using a 128 GB SD card as we're not only going to use the storage for saving files, but also to off-load RAM when we need to (this is called a SWAP file).

> [!WARNING]
> Do **not** install any other image of JetPack than the one from WaveShare as the configuration for the PCA9685 integrated circuit won't work. From experience, I have previously gotten it to work, but if you're not willing to skim through integrated circuit datasheets and learn what an $I^2C$-bus controller is, just use the WaveShare image.

> [!TIP]
> I struggled opening the .zip file from WaveShare on MacOS. Using an app called [The Unarchiver](https://theunarchiver.com/) worked for me.

Your JetRacer should now be able to boot up. Either via SSH or in the terminal, type in the following:

```zsh
cd Jetracer
sudo git checkout master
sudo python3 setup.py install
sudo reboot
```

> [!TIP]
> The IP address of the car will always show on the small on-board display when the car is connected to a network.

Next, to select the power mode of the car, type in this command:

```zsh
sudo nvpmodel -m1
```

The power mode is either `5W` or `MAXN`. `5W` should be used if the car is not connected to a power supply. You can also check which power mode you're using on the small on-board display.

Now, type in these commands, which will install dependencies needed by [Donkey](https://docs.donkeycar.com/) (Donkey is an open source Self Driving Car Platform for remote control cars written in Python and is what we will use):

```zsh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
sudo apt-get install -y python3-dev python3-pip
sudo apt-get install -y libxslt1-dev libxml2-dev libffi-dev libcurl4-openssl-dev libssl-dev libpng-dev libopenblas-dev
sudo apt-get install -y git nano
sudo apt-get install -y openmpi-doc openmpi-bin libopenmpi-dev libopenblas-dev
```