# calculator.py
A scientific calculator for your terminal emulator.
# usage
If you want to execute it, you need to add perms, e.g. 
```console
chmod +x calculator.py
```
After adding execution perms, just execute it with
```console
./calculator.py
```
If you are using Windows, you should only need
```console
python3 calculator.py
```
# functions & constants
Comes with multiple functions and constants, some packages will need to be installed. <br>
Examples of some functions:
```python
distance(10, 'in', 'cm') # 25.4 cm
mass(50, 'kg', 'lb') # 110 pounds
nPr(5, 5) / fact(2) # number of times you can arrange the word "apple"
```
The function "log" was changed to be custom, example:
```python
# log(base, number)
log(10, 100) # returns 2
```
You can also eval an equation
```console
./calculator.py -e "nPr(5, 5) / fact(2)"
```
If you need to view/forget a constant, you can view them with the "const" command, via
```console
const
```
if you forget what you typed after clearing your screen with the "clear" command, you can view your history with the "hist" command, e.g.
```console
hist
```
# functions that require packages
Some functions will require external packages, example of one is scipy
```python
z2p(1) # approx. 0.84
p2z(.84) # approx. 1
# these were two examples of scipy's cdf and ppf functions, respectively
```
```python
# stdev function uses statistics package
stdev([1, 2, 3]) # equals 1
# stdev([1, 2, 3], 'pop') for population
# stdev uses sample by default
```
Sample standard deviation formula is given below <br>
$\huge{ s = \sqrt{\frac{\Sigma_{i=1}^{N}(x_i - \bar{x})^2}{N - 1}} }$

