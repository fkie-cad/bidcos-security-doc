# Bidcos Security Documentation

## doc

The *doc* folder of the repository contains a two-part documentation of the proprietary radio protocol *BidCos*, which was developed by the company [eQ-3](https://www.eq-3.de/start.html) and is used in their smart home product line [HomeMatic](https://www.eq-3.de/produkte/homematic.html).
The first part deals with the general protocol description of *BidCos*, while the second part describes possible attack vectors and their technical implementation on this protocol. How to perform experiments on different test setups is also described in this [video tutorial](https://youtu.be/ou_yOsTa72E).

> :warning: Since the documentation depends heavily on third party sources, we cannot guarantee its completeness or correctness! Please read the [disclaimer](/doc/1-bidcos.md) carefully!



## urh

The *urh* folder contains files for implementing an attack using the software [Universal Radio Hacker](https://github.com/jopohl/urh) and an [SDR](https://de.wikipedia.org/wiki/Software_Defined_Radio) like the [HackRF One](https://greatscottgadgets.com/hackrf/one/).
**Requirements:**

- Latest version of Universal Radio Hacker

- One SDR which can send/receive messages on 868 MHz (for some attacks a second SDR is needed)
- Python3

## License

The content of the folder *doc* is licensed under the [CC-BY-4.0](doc/LICENSE) license and the content of the *urh* folder is licensed under the [GNU GPLv3](urh/LICENSE) license. 
