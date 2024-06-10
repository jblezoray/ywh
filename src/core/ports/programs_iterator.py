

class ProgramsIterator:
    def __iter__(self):
        raise NotImplementedError()
    
    def __next__(self):
        raise NotImplementedError()

class ProgramsIteratorBuilder:
    def build(self) -> ProgramsIterator:
        raise NotImplementedError()
