from abc import ABC, abstractmethod

class AbstractBaseInterface(ABC):

    @abstractmethod
    def get_articles():
        pass
    
    @abstractmethod
    def add_article():
        pass

if __name__=='__main__':
    interface = AbstractInterface()