from persistent.store_hdf5 import H5Store

def test_h5_append(tmp_path):
    store=H5Store(root=tmp_path/'h5')
    p=store.append('nauka','spec',[1.23])
    assert p.endswith('.h5')
