## Installation and Setup

### mr_proc code+env installation
   - Change dir to where you want to clone this repo, e.g.: `cd /home/<user>/projects/<my_project>/code/`
   - Create a new [venv](https://realpython.com/python-virtual-environments-a-primer/): `python3 -m venv mr_proc_env` 
   - Activate your env: `source mr_proc_env/bin/activate` 
   - Clone this repo: `git clone https://github.com/neurodatascience/mr_proc.git`
   - Change dir to `mr_proc` 
   - Install python dependencies: `pip install -e .`  

### mr_proc dataset directory Setup 
   - mr_proc expects following directory tree with several *mandatory* subdirs and files. 
   - You can run `scripts/mr_proc_setup.sh` to create this directory tree. 
   - You can run `scripts/mr_proc_stutus.sh` check status of your dataset