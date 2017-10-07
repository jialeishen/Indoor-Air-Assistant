![logo](https://github.com/jialeishen/Indoor-Ozone-PPB/blob/master/newlogo.jpg)
# Indoor-Air-Assistant

{{% toc %}}

## Introduction
---
**Indoor Air Assistant** is a program which aims to estimate the indoor ozone concentration levels based on a single zone mass balance model, but is still in development (For more information, please visit my [Github](https://github.com/jialeishen/Indoor-Air-Assistant)).

The following equation is used to describe the rate of change of indoor ozone concentration with time:

$$\frac{dC}{dt}=\lambda C_o+\frac{S'}{V}-\lambda C-\sum v_d A_i \frac{C}{V}$$

The ozone deposition velocity to a surface encompasses the transport of ozone to the surface and the reactivity of a surface with ozone, which can be calculated by:

$$\frac{1}{v_d}=\frac{1}{v_t}+\frac{1}{v_s}=\frac{1}{v_t}+\frac{4}{\gamma \langle v \rangle}$$

This program uses the values of $v_d$, $v_t$ and $\gamma$ in literature to estimate the indoor ozone concentration levels using the above equations. You can read [my publication]({{< ref "publication/hb2017_2.md" >}}) for more detailed information.

## How to use
---
This program is python-based. If you have already installed [python](https://www.python.org/) on your own computer, you can just download this program and run it on your python IDE. Meanwhile some python packages are necessary for running this program, including [wxPython](https://www.wxpython.org), [numpy](http://www.numpy.org/) and [matplotlib](http://matplotlib.org/). Please make sure your computer has successfully installed them. If you don't have python on your computer, you can download the software ([inAir_v1.1.0.zip](https://github.com/jialeishen/Indoor-Air-Assistant/releases/download/v1.1.0/inAir.zip)) we have already packaged by pyinstaller and directly use it on your computer (Windows, Linux and Mac OS). However, the packaged software might not always be the latest version. Thanks for your support.

## Download
---
### v1.1.0
 - [Source code](https://github.com/jialeishen/Indoor-Air-Assistant/archive/master.zip)
 - [inAir_v1.1.0.zip](https://github.com/jialeishen/Indoor-Air-Assistant/releases/download/v1.1.0/inAir.zip)

## Acknowledge
---
This program is supported financially by the national key project of the Ministry of Science and Technology, China on “[Green Buildings and Building Industrialization](http://buildingventilation.org/eng_index.html)” through Grant No. 2016YFC0700500. Special thanks to all the researchers who contributes to the investigation of indoor air quality, since the program was inspired by their works, particularlly the [IMPACT](http://www.ucl.ac.uk/sustainableheritage-save/impact/index.htm) program.
