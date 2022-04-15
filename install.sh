python -m pip install --upgrade pip
pip install -U pip
python -m pip install -r requirements.txt && python -m spacy download en_core_web_md
# Just to be sure, we do it again but without specifying the python executable
pip install -r requirements.txt && python -m spacy download en_core_web_md
echo "INSTALLATION SUCCESSFUL"