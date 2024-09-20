# Create the conda environment
```
conda create -n MMPS python=3.9 -y
```
# Activate the environment
```
conda activate MMPS
```
# Install the required packages
```
conda install -c conda-forge openai langchain tqdm -y
conda install -c anaconda re hashlib -y
conda install -c anaconda datetime -y
```
# Verify the installation
```
python -c "import logging, re, hashlib, datetime, openai, langchain, tqdm; print('All packages installed successfully!')"
```
