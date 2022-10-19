# turinglab

## Installation

```bat
pip install git+https://git.slipenko.com/UniversityProjects/turinglab.git
```

## Develop

```bat
python setup.py develop
```

## Usage

```bat
turinglab input_file output_dir [-t TESTS [TESTS ...]] [-e EMPTY_CHARACTER] [-f]
```

### Example

```bat
turinglab 0to1to0.txt .\out -t 101 1E -e E -f
```
or
```bat
turinglab 0to1to0.txt .\out --tests 101 1E --empty-character E --force
```

Content of ```out\report.docx```:

![image](https://user-images.githubusercontent.com/36362599/133917663-f725d137-e33e-4440-8640-15262120c5bb.png)

Content of ```out\graph.svg```:

![image](https://user-images.githubusercontent.com/36362599/133909074-e1928d40-263f-4c80-94ef-4ae495662419.png)

