from abc import ABC, abstractmethod
import shutil
import yaml

class AbstractBaseInterface(ABC):
    @staticmethod
    def get_kenfile():
        with open('Kenfile', 'r') as kenstream:
            return yaml.safe_load(kenstream)
    
    @staticmethod
    def reset_kenfile():
        shutil.copyfile('templates/kenfile.yaml', 'Kenfile')


    @abstractmethod
    def get_articles():
        pass
    
    @abstractmethod
    def add_article():
        pass

if __name__=='__main__':
    interface = AbstractInterface()
    interface.reset_kenfile()