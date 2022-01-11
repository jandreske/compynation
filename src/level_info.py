class LevelInfo:
    def __init__(self, file):
        """
        Loads the level overview from a file an fills various dictionaries to translate between ids, passwords and names
        :param file: the file to load the level information from
        """
        self._byPassword = {}
        self._byIndex = {}
        self._passwords = {}
        with open(file) as f:
            self._index = 0
            for line in f.readlines():
                line = line.strip().split(',')
                self._passwords[int(line[0])] = line[1]
                self._byPassword[line[1]] = int(line[0])
                self._byIndex[int(line[0])] = line[2]

    @property
    def first(self):
        """
        Starts a new run at the first level
        :return: the first level to play
        """
        if self._index != 0:
            raise Exception("Can only start a new run once")
        self._index = 1
        return self._byIndex[self._index]

    @property
    def password(self):
        if self._index == 0:
            raise Exception("Need to start a new run first")
        return self._passwords[self._index]

    @property
    def index(self):
        return self._index

    @property
    def next(self):
        """
        Gets the next level in sequence
        :return: the next level to play
        """
        if self._index == 0:
            raise Exception("Need to start a new run first")
        if self._index == max(self._byIndex.keys()):
            return 0
        self._index = self._index + 1
        return self._byIndex[self._index]

    def by_password(self, password):
        """
        Initializes a new run and returns the level name matching the given password
        :param password: the password for the level to start at
        :return: the starting level for the password or the first level if the password does not exist
        """
        if self._index != 0:
            raise Exception("Can only start a new run once")
        try:
            index = self._byPassword[password]
        except KeyError:
            index = 1
        self._index = index
        return self._byIndex[self._index]

    @property
    def last(self):
        return max(self._byIndex.keys())
