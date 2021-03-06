### Machine Learning as a Service for HEP

[![Build Status](https://travis-ci.org/vkuznet/TFaaS.svg?branch=master)](https://travis-ci.org/vkuznet/TFaaS)
[![License:MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/vkuznet/LICENSE)
[![DOI](https://zenodo.org/badge/156857396.svg)](https://zenodo.org/badge/latestdoi/156857396)
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Machine%20Learning%20as%20a%20service%20for%20HEP%20community&url=https://github.com/vkuznet/MLaaS4HEP&hashtags=python,ml)

MLaaS for HEP is a set of Python based modules to read HEP ROOT files and
stream them to ML of user choice for training. It consists of three independent layers:
- data streaming layer to handle remote data,
  see [reader.py](https://github.com/vkuznet/MLaaS4HEP/blob/master/src/python/reader.py)
- data training layer to train ML model for given HEP data,
  see [workflow.py](https://github.com/vkuznet/MLaaS4HEP/blob/master/src/python/workflow.py)
- data inference layer,
  see [tfaas_client.py](https://github.com/vkuznet/MLaaS4HEP/blob/master/src/python/tfaas_client.py)

The general architecture of MLaaS4HEP looks like this:
![MLaaS4HEP-architecture](https://github.com/vkuznet/MLaaS4HEP/blob/master/images/MLaaS4HEP-architecture.png)

The pre-trained models can be easily uploaded to
[TFaas](https://github.com/vkuznet/TFaaS) server for serving them to clients.

### Reading ROOT files
MLaaS4HEP python repository provides two base modules to read and manipulate with
HEP ROOT files. The `reader.py` module defines a DataReader class which is
able to read either local or remote ROOT files (via xrootd). And, `workflow.py`
module provide a basic DataGenerator class which can be used with any ML
framework to read HEP ROOT data in chunks. Both modules are based on
[uproot](https://github.com/scikit-hep/uproot) framework.

Basic usage
```
# get help and option description
./reader.py --help

# here is a concrete example of reading local ROOT file:
./reader.py --fin=/opt/cms/data/Tau_Run2017F-31Mar2018-v1_NANOAOD.root --info --verbose=1 --nevts=2000

# here is an example of reading remote ROOT file:
./reader.py --fin=root://cms-xrd-global.cern.ch//store/data/Run2017F/Tau/NANOAOD/31Mar2018-v1/20000/6C6F7EAE-7880-E811-82C1-008CFA165F28.root --verbose=1 --nevts=2000 --info

# both of aforementioned commands produce the following output
First pass: 2000 events, 35.4363200665 sec, shape (2316,) 648 branches: flat 232 jagged
VMEM used: 960.479232 (MB) SWAP used: 0.0 (MB)
Number of events  : 1131872
# flat branches   : 648
...  # followed by a long list of ROOT branches found along with their dimentionality
TrigObj_pt values in [5.03515625, 1999.75] range, dim=21
```

More examples about using uproot may be found
[here](https://github.com/jpivarski/jupyter-talks/blob/master/2017-10-13-lpc-testdrive/uproot-introduction-evaluated.ipynb)
and
[here](https://github.com/jpivarski/jupyter-talks/blob/master/2017-10-13-lpc-testdrive/nested-structures-evaluated.ipynb)

### How to train ML model on HEP data
The HEP data are presented in [ROOT](https://root.cern.ch/) data-format.
The [DataReader](https://github.com/vkuznet/MLaaS4HEP/blob/master/src/python/reader.py#L188)
class provides access to ROOT files and various APIs to access the HEP data.

A simple workflow example can be found in
[workflow.py](https://github.com/vkuznet/MLaaS4HEP/blob/master/src/python/workflow.py)
code. It contains two examples, one for PyTorch and another for Keras.  It
contains two examples (on for PyTorch and another for TF in Keras) and show
full HEP ML workflow, i.e. it can read remote files and perform the training of
ML models with HEP ROOT files.


If you clone the repo and setup your PYTHONPATH you should be able to run it as
simple as

```
./workflow.py --help

# run the code with list of LFNs from files.txt and using labels file labels.txt
./workflow.py --files=files.txt --labels=labels.txt

# run pytorch example
./workflow.py --files=files.txt --labels=labels.txt --model=ex_pytorch.py

# run keras example
./workflow.py --files=files.txt --labels=labels.txt --model=ex_keras.py

# cat files.txt
#dasgoclient -query="file dataset=/Tau/Run2018C-14Sep2018_ver3-v1/NANOAOD"
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/069A01AD-A9D0-7C4E-8940-FA5990EDFFCE.root
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/577AF166-478C-1F40-8E10-044AA4BC0576.root
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/9A661A77-58AC-0245-A442-8093D48A6551.root
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/C226A004-077B-7E41-AFB3-6AFB38D1A63B.root
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/D1E05C97-DB14-3941-86E8-C510D602C0B9.root
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/6FA4CC7C-8982-DE4C-BEED-C90413312B35.root
/store/data/Run2018C/Tau/NANOAOD/14Sep2018_ver3-v1/60000/282E0083-6B41-1F42-B665-973DF8805DE3.root

# cat labels.txt
1
0
1
0
1
1
1

# run keras example and save our model into external file
./workflow.py --files=files.txt --labels=labels.txt --model=ex_keras.py --fout=model.pb
```

The `workflow.py` relies on two JSON files, one which contains parameters for
reading ROOT files and another with specification of ROOT branches. The later
will be generated by reading ROOT file itself.

### HEP resnet
We provided full code called `hep_resnet.py` as a basic model based on
[ResNet](https://github.com/raghakot/keras-resnet) implementation.
It can classify images from HEP events, e.g.
```
hep_resnet.py --fdir=/path/hep_images --flabels=labels.csv --epochs=200 --mdir=models
```
Here we supply input directory `/path/hep_images` which contains HEP images
in `train` folder along with `labels.csv` file which provides labels.
The model runs for 200 epochs and save Keras/TF model into `models` output
directory.

### TFaaS client
We provide pure python
[client](https://github.com/vkuznet/TFaaS/blob/master/src/python/tfaas_client.py)
to perform all necessary action against TFaaS server. Here is short
description of available APIs:

```
# setup url to point to your TFaaS server
url=http://localhost:8083

# create upload json file, which should include
# fully qualified model file name
# fully qualified labels file name
# model name you want to assign to your model file
# fully qualified parameters json file name
# For example, here is a sample of upload json file
{
    "model": "/path/model_0228.pb",
    "labels": "/path/labels.txt",
    "name": "model_name",
    "params":"/path/params.json"
}

# upload given model to the server
tfaas_client.py --url=$url --upload=upload.json

# list existing models in TFaaS server
tfaas_client.py --url=$url --models

# delete given model in TFaaS server
tfaas_client.py --url=$url --delete=model_name

# prepare input json file for querying model predictions
# here is an example of such file
{"keys":["attribute1", "attribute2"], values: [1.0, -2.0]}

# get predictions from TFaaS server
tfaas_client.py --url=$url --predict=input.json

# get image predictions from TFaaS server
# here we refer to uploaded on TFaaS ImageModel model
tfaas_client.py --url=$url --image=/path/file.png --model=ImageModel
```

### Citation
Please use this publication for further citation:
[http://arxiv.org/abs/1811.04492](http://arxiv.org/abs/1811.04492)
