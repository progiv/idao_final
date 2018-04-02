all: build

prepare:
# Вместо "*.ipynb" подставить имя своего ноутбука, если их несколько
	jupyter nbconvert --to python *.ipynb --output main.py 
	zip -r submission.zip main.py main.sh Makefile
build:
	echo "I can see this in the log!"
	ls /usr/conda/bin
	/usr/conda/bin/python --version
	/usr/conda/bin/pip freeze
run:
	bash main.sh
clean:
	rm submission.*
	rm main.py

