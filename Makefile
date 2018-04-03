all: build

prepare:
# Вместо "*.ipynb" подставить имя своего ноутбука, если их несколько
	rm -r build_submission/; mkdir build_submission
	jupyter nbconvert *.ipynb --to python --output-dir=build_submission
#	jupyter nbconvert --to python *.ipynb
	cp -r functions *.py Makefile main.sh model_to_run.pickle build_submission
	cd build_submission; zip -r ../submission.zip .; cd ..
build:
	echo "I can see this in the log!"
	ls /usr/conda/bin
	/usr/conda/bin/python --version
	/usr/conda/bin/pip freeze
run:
	bash main.sh
clean:
	rm submission.*
#	rm main.py
