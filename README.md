Comparison of a few parallelism methods in python
=================================================


- The watching script requires `entr`, which you can use your OS package manager to get.
- Use `requirements.txt` to build your virtualenv.

```bash
$ conda create --name mp python=3.6
$ conda activate mp
$ pip install -r requirements.txt
$ brew install entr
$ ./watch.sh
```
