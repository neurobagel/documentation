## Code installation and dataset setup

---

mr_proc workflow comprises mr_proc codebase that operates on mr_proc dataset with a specific directory structure, which is initialized with a tree.py script. 

---

### mr_proc code+env installation
   - Change dir to where you want to clone this repo, e.g.: `cd /home/<user>/projects/<my_project>/code/`
   - Create a new [venv](https://realpython.com/python-virtual-environments-a-primer/): `python3 -m venv mr_proc_env` 
   - Activate your env: `source mr_proc_env/bin/activate` 
   - Clone this repo: `git clone https://github.com/neurodatascience/mr_proc.git`
   - Change dir to `mr_proc` 
   - Install python dependencies: `pip install -e .`  

### mr_proc dataset directory setup 
   - Run `python tree.py` to create mr_proc dataset directory tree
   
> Sample cmd:
```bash
python tree.py --mr_proc_root <DATASET_ROOT>
```

- `data_disk`: data storage location on a local disk
- `DATASET_ROOT`: root (starting point) of the mr_proc structured dataset

!!! Suggestion

    We suggest naming DATASET_ROOT directory after a study or a cohort. 
