from PyQt5.QtCore import QObject, pyqtSignal
import yaml

from lib.converter import ConverterType, Converter
from .logger import logger

class SensorProfileManager(QObject):

    profilesChanged = pyqtSignal()
    profilesPath = 'transducers.yaml'

    def __init__(self):
        super().__init__()
        self.profiles = []

    def loadProfiles(self):
        try:
            with open(self.profilesPath, 'r') as readLocation:
                self.profiles = [Converter(properties) for properties in yaml.full_load(readLocation)]
                self.profilesChanged.emit()
        except Exception as err:
            logger.error('Could not read sensor profiles, using default. Error: ' + str(err))
            self.saveProfiles()

        self.profilesChanged.emit()

    def saveProfiles(self):
        logger.log('Saving profiles to "{}"'.format(self.profilesPath))
        with open(self.profilesPath, 'w') as saveLocation:
            yaml.dump([profile.getProperties() for profile in self.profiles], saveLocation)

    def getProfile(self, name):
        for profile in self.profiles:
            if profile.getProperty('name') == name:
                return profile

    def getProfileNames(self, filterType=None):
        if filterType is None:
            return [prof.getProperty('name') for prof in self.profiles]
        return filter(lambda name: self.getProfile(name).getProperty('type') == filterType, self.getProfileNames())

    def addProfile(self, profile):
        logger.log('Adding profile of type "{}" with name "{}"'.format(
            profile.getProperty('type'),
            profile.getProperty('name')
        ))
        self.profiles.append(profile)
        self.saveProfiles()
        self.profilesChanged.emit()
