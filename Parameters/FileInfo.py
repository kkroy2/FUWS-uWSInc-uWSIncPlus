
class FileInfo():
    initial_dataset = None
    initial_fs = None
    initial_sfs = None
    time_info = None
    increment_dataset = None
    increment_fs = None
    increment_sfs = None

    @staticmethod
    def set_initial_file_info(init_db, fs, sfs):
        FileInfo.increment_dataset = open(init_db, 'r')
        FileInfo.initial_fs = open(fs, 'w')
        FileInfo.initial_sfs = open(sfs, 'w')
        pass
