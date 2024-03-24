# calculator.py
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/xyzpw/calculator.py/total)<br>

A scientific calculator for your terminal emulator.<br>

![calculator_py-preview](https://github.com/xyzpw/calculator.py/assets/76017734/d7ef5ae7-1601-4722-a7d4-66e1442f2dc4)
## Installing Dependancies
Some modules will need to be installed for this application to work properly. See the codeblock below for an example on installing dependencies.
```sh
# install dependencies
$ pip3 install -U -r requirements.txt

# run calculator.py
$ python3 calculator.py
```
## Features
The **calculator.py** script contains several features, the `showhelp` function is useful because it displays usage info about a given function.<br><br>
To use the `showhelp` function, type `showhelp()` inside the script. Optionally, you can display specific info about a given function by passing the function name in as an argument, e.g. `showhelp(log)`, this will display usage information about the `log` function.<br><br>
> [!NOTE]
> The `round` function uses Bankers rounding. Python uses this rounding method by default, so this is used to avoid confusion.
> If you want to round 5 up, use the `roundup` function, this is the most common rounding method.**

### Viewing History
History can be displayed with the `hist` command. Alternatively, the command `history` will do the same.<br>
Optionally, you can view the last `n` equations, or even a range between two specified points in your history.<br><br>

#### Optional History Arguments
Viewing the last `n` equations in your history.
```text
hist n
```
Viewing the history range from the `xth` to `nth` point in history.
```text
hist xth nth
```
**note: history is displayed from oldest to latest**

#### Previous Answer
The `ans` variable is equivalent to your previous expressions answer, therefor you do not have to type in your previous expression.<br>
```text
π = 3.141592653589793
ans == π = true
```

### Constants
You can view the list of inbuild constants with the `const` command. This will display the following output:
```text
c = Speed of light 299,792,458 m/s
g = Standard gravity 9.80665 m/s²
G = Gravitational constant 6.6743e-11 N·m²·kg⁻²
h = Planck constant 6.62607015e-34 J·Hz⁻¹
kb = Boltzmann constant 1.380649e-23 J·K⁻¹
phi = Golden ratio 1.618033988749895
NA = Avogadro constant 6.02214076e+23 mol⁻¹
ke = Coulomb constant 8987551792.3 N·m²·C⁻²
e0 = Electric constant 8.8541878128e-12 F·m⁻¹
R = Gas constant 8.31446261815324 J·K⁻¹·mol⁻¹
```
### Functions
Examples for several, but not all functions.
#### Mathematical
```python
root(4, 16)
# output: 2
log(9, 81)
# output: 2
```
#### Imaginary Numbers
```python
sqrt(-1)
# output: i
```
#### Statistics
```python
binomial(0.25, 5, 2)
# output: 0.263671875
uncertainty([3, 19, 20, 5])
# output: 8.5
```
#### Converting Units
```python
temperature(68, 'f', 'c')
# output: 20
volume(1, 'gal', 'c')
# output: 16
```


# Contributing
Pull requests are unlikely to be merged, but fixes such as typos or grammar/spelling mistakes are more likely to be merged.<br>
## Bug Reports
Bugs can be reported via creating a new issue.<br>
## Misc.
Read [Discussions](https://github.com/xyzpw/calculator.py/discussions/2) for additional info.
