
REQUIREMENTS
======================
* Python 2.7.x
* virtualenv
* pip

INSTALL
======================

* Clone the repository somewhere on your disk
* Create a virtualenv
```bash
virtualenv --no-site-packages ve311
```

* Activate the virtualenv you just created.
```bash
source ve311/bin/activate
```
* Install the required Python libraries, some of have native extensions, so you should have gcc installed
```bash
pip install -r open311/requirements.pip
```
* Go to the test directory, hopefuly all the tests should pass.
```bash
cd open311/tests
```
* Run the application in development mode and start hitting the services
```bash
cd open311
python main.py
```

That's all for now. Ask me questions on @diptanu
