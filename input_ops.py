import numpy as np
import tensorflow as tf

from util import log

def check_data_id(dataset, data_id):
    if not data_id:
        return

    wrong = []
    for id in data_id:
        if id in dataset.data:
            pass
        else:
            wrong.append(id)

    if len(wrong) > 0:
        raise RuntimeError("There are %d invalid ids, including %s" % (
            len(wrong), wrong[:5]
        ))


def create_input_ops(dataset,
                     batch_size,
                     num_threads=16,           # for creating batches
                     is_training=False,
                     data_id=None,
                     scope='inputs',
                     shuffle=True,
                     ):
    '''
    Return a batched tensor for the inputs from the dataset.
    '''
    family_ops = {}
    input_ops = {}

    if data_id is None:
        data_id = dataset.ids
        log.info("input_ops [%s]: Using %d IDs from dataset", scope, len(data_id))
    else:
        log.info("input_ops [%s]: Using specified %d IDs", scope, len(data_id))

    # single operations
    with tf.device("/cpu:0"), tf.name_scope(scope):
        family_ops['id'] = tf.train.string_input_producer(
           tf.convert_to_tensor(data_id),
            capacity=128
        ).dequeue(name='family_ids_dequeue')

        #m = dataset.get_data(data_id[0])


        def load_fn(id):
            # image [h, w, c]
            valid = False
            while not valid:
                try:
                    image = dataset.get_data(id) # return dict  of family tuples corresponding to 1 family
                    valid = True
                except:
                    pass
            print(image)

            return image #This is an dict of tuple of (family_id, numpy array of 4 layer image)

        family_images = tf.py_func(
            load_fn, inp=[family_ops['id']],
            Tout=[tf.Tensor],
            name='func_hp'
        )

        def load_img(id):
            return (id, family_images[id])
        
        input_ops['id'], inputs_ops['image']  = tf.py_func(
            load_img, inp=family_images.keys(),
            Tout=[tf.string, tf.float32],
            name='func_hp'
        )



        input_ops['id'].set_shape([])
        input_ops['image'].set_shape(list(m.shape))

    # batchify
    capacity = 2 * batch_size * num_threads
    min_capacity = min(int(capacity * 0.75), 1024)

    if shuffle:
        batch_ops = tf.train.shuffle_batch(
            input_ops,
            batch_size=batch_size,
            num_threads=num_threads,
            capacity=capacity,
            min_after_dequeue=min_capacity,
        )
    else:
        batch_ops = tf.train.batch(
            input_ops,
            batch_size=batch_size,
            num_threads=num_threads,
            capacity=capacity,
        )

    return input_ops, batch_ops
