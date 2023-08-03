## Code installation and dataset setup

---

The `mr_proc` workflow comprises an `mr_proc` codebase that operates on a `mr_proc` dataset with a specific directory structure (initialized with a `tree.py` script). 

---

### mr_proc code+env installation
1. Change directory to where you want to clone this repo, e.g.: `cd /home/<user>/projects/<my_project>/code/`
2. Create a new [venv](https://realpython.com/python-virtual-environments-a-primer/): `python3 -m venv mr_proc_env`
   * Alternatively (if using [Anaconda/Miniconda](https://www.anaconda.com/)), create a `conda` environment: `conda create --name mr_proc_env python=3.9`
3. Activate your env: `source mr_proc_env/bin/activate` 
   * If using Anaconda/Miniconda: `conda activate mr_proc_env`
4. Clone this repo: `git clone https://github.com/neurodatascience/mr_proc.git`
5. Change directory to `mr_proc` 
6. Install python dependencies: `pip install -e .`  

### mr_proc dataset directory setup 

Run `tree.py` to create the `mr_proc` dataset directory tree:
```bash
python tree.py --mr_proc_root <DATASET_ROOT>
```
Where
- `data_disk`: data storage location on a local disk
- `DATASET_ROOT`: root (starting point) of the mr_proc structured dataset

!!! Suggestion

    We suggest naming DATASET_ROOT directory after a study or a cohort. 
