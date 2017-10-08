import itertools
from numpydataset import *
from rawdata import RawData
from filtereddata import FilteredData

tremor_tasks = ['drnkg', 'fldng',
                'ramr1', 'raml1', 'ramr2', 'raml2',
                'orgpa',
                'ftnl1', 'ftnr1', 'ftnl2', 'ftnr2',
                'ntblt']

dyskin_tasks = ['ramr1', 'raml1', 'ramr2', 'raml2',
                'ftnl1', 'ftnr1', 'ftnl2', 'ftnr2']

brakin_tasks = ['drnkg', 'fldng', 'orgpa',
               'ramr1', 'raml1', 'ramr2', 'raml2',
               'ftnl1', 'ftnr1', 'ftnl2', 'ftnr2']

def get_dataset_names(data_transform):
    return ['-'.join(x) for x in itertools.product([data_transform], ['tre'], tremor_tasks)] \
        + ['-'.join(x) for x in itertools.product([data_transform], ['dys'], dyskin_tasks)] \
        + ['-'.join(x) for x in itertools.product([data_transform], ['bra'], brakin_tasks)]

# dataset prefixes:
# - r               raw
# - fh_[cutoff]     high-pass filter, [cutoff] = cutoff frequency
# - fl_[cutoff]     low-pass filter, [cutoff] = cutoff frequency
# - fb_[low]_[high] band-pass filter, [low], [high] = cutoff frequencies
dataset_names = get_dataset_names('r') \
                + get_dataset_names('fh_1') \
                + get_dataset_names('fh_2') \
                + get_dataset_names('fb_1_20')


# generate "mPower-like" dict from dataset names
dataset = dict(zip(dataset_names, [{'input_1' : x} for x in dataset_names]))


def get_dataset(name, reload_ = False):
    (data_type, outcome, task) = name.split('-')

    if data_type == 'r':
        return RawData(outcome, task, reload_=reload_)
    elif data_type[0] == 'f':
        filter_type = {'b' : 'band', 'h' : 'high', 'l' : 'low'}[data_type[1]]
        freqs = [float(x) for x in data_type.split('_')[1:]]

        return FilteredData(outcome, task, filter_type, freqs, reload_=reload_)
    else:
        raise Exception('Unknown data type:', data_type)