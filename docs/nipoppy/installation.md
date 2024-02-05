## Code installation and dataset setup

---

The Nipoppy workflow comprises a Nipoppy codebase that operates on a Nipoppy dataset with a specific directory structure (initialized with a `tree.py` script). 

---

### Nipoppy code+env installation
1. Change directory to where you want to clone this repo, e.g.: `cd /home/<user>/projects/<my_project>/code/`
2. Create a new [venv](https://realpython.com/python-virtual-environments-a-primer/): `python3 -m venv nipoppy_env`
   * Alternatively (if using [Anaconda/Miniconda](https://www.anaconda.com/)), create a `conda` environment: `conda create --name nipoppy_env python=3.9`
3. Activate your env: `source nipoppy_env/bin/activate`
   * If using Anaconda/Miniconda: `conda activate nipoppy_env`
4. Clone this repo: `git clone https://github.com/neurodatascience/nipoppy.git`
5. Change directory to `nipoppy`
6. Install python dependencies: `pip install -e .`

### Nipoppy dataset directory setup 

Run [`nipoppy/tree.py`](https://github.com/neurodatascience/nipoppy/blob/main/nipoppy/tree.py) to create the Nipoppy dataset directory tree:
```bash
python nipoppy/tree.py --nipoppy_root <DATASET_ROOT>
```
Where:

- `DATASET_ROOT`: root (starting point) of the Nipoppy structured dataset

!!! Suggestion

    We suggest naming DATASET_ROOT directory after a study or a cohort. 
