cd bend
mkdir .venv
cd .venv
virtualenv hom
source hom/bin/activate
cd ..
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python db_create.py
python run.py

