
class FileInfo():
    initial_dataset = None
    fs = None
    sfs = None
    pfs = None

    time_info = None
    increment_dataset = None
    increment_fs = None
    increment_sfs = None
    ls = None
    # time_info = None

    @staticmethod
    def set_initial_file_info(init_db, fs, sfs, pfs):
        FileInfo.initial_dataset = open(init_db, 'r')
        FileInfo.fs = open(fs, 'w')
        FileInfo.sfs = open(sfs, 'w')
        FileInfo.pfs = open(pfs, 'w')
        pass
