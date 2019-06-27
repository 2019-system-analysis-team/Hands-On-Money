(1) pip install flask

(2) pip install flask-sqlalchemy 

(3) python run.py

(4) visit localhost:5000

> commented by sirius
> -- start--

install for conda user:
1. change source from orign to tuna:

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

2. install must have package

```
conda insatll flask
conda insatll flask-sqlalchemy
conda insatll flask-bcrypt
```

3. run `python run.py`

> -- end --

Deployment Testing
95.179.171.246:5000
