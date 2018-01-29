from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.utils import to_categorical
import pandas as pd
import numpy as np
import datetime
from itertools import chain, repeat, cycle

# for model.fit function -> keras description
# class_weight: Optional dictionary mapping class indices (integers) to a weight (float) value,
# used for weighting the loss function (during training only).
# This can be useful to tell the model to "pay more attention" to samples from an under-represented class.
def get_class_weight(train_dir):
    # to be implemented
    class_weight = dict()
    return class_weight


def preprocess_input(x):
    x /= 255.
    x -= 0.5
    x *= 2.
    return x


def save_string( num_freezed_layers, lr):
    current_date = '{:%d.%m.%Y %H:%M:%S}'.format(datetime.datetime.now())
    save_string1 = current_date + "_Inception_num_freezedLayers_%d _r_%g" % (num_freezed_layers, lr)
    save_string_return = save_string1.replace(" ", "_")
    save_string_return = save_string_return.replace(":", "_")
    save_string_return = save_string_return.replace(".", "_")
    save_string_return = save_string_return + ".h5"
    return save_string_return


def csv_to_lists(csv_file_name, sep=','):
    # parse csv
    df = pd.read_csv(csv_file_name, sep=sep)
    # change csv to list
    values_list = df.values.tolist()
    X = []
    y = []
    # parse training list and create x_train and y_train lists
    for element in values_list:
        X.append(element[0])
        # if that list does contain anything
        if type(element[1]) is str:
            y.append(list(map(int, element[1].split())))
        # if that list doesn't contain anything
        else:
            y.append([])

    X = np.array(X)
    y = np.array(y)
    return X, y


def to_multi_label_categorical(labels, dimension = 9):
    results = np.zeros((len(labels),dimension))
    for i in range(len(labels)):
        temp = to_categorical(labels[i],num_classes=dimension)
        results[i] = np.sum(temp, axis=0)
    return results

def apply_mean(image_data_generator):
    """Subtracts the dataset mean"""
    image_data_generator.mean = np.array([103.939, 116.779, 123.68], dtype=np.float32).reshape((3, 1, 1))

#Generator
def grouper(n, iterable, padvalue=None):
    g = cycle(zip(*[chain(iterable, repeat(padvalue, n-1))]*n))
    for batch in g:
        yield list(filter(None, batch))
 
 
def multilabel_flow(path_to_data, idg, photo_name_to_label_dict, bs=256, target_size=(32,32), train_or_valid='train'):
    gen = idg.flow_from_directory(path_to_data, batch_size=bs, target_size=target_size, classes=[train_or_valid], shuffle=False)
    names_generator = grouper(bs, gen.filenames)
    for (X_batch, _), names in zip(gen, names_generator):
        names = [n.split('/')[-1].replace('.jpg','') for n in names]
        targets = [photo_name_to_label_dict[int(x)] for x in names]
        yield X_batch, targets