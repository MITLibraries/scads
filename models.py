from google.appengine.ext import ndb

class MetadataSpec(ndb.Model):
    """ Sub model class for characterizing metadata fields """
    name = ndb.StringProperty(required=True)
    presetValue = ndb.StringProperty(indexed=False)
    defaultValue = ndb.StringProperty(indexed=False)
    valueList = ndb.StringProperty(indexed=False)
    optional = ndb.BooleanProperty(default=False)
    sticky = ndb.BooleanProperty(default=False)

class Workflow(ndb.Model):
    """ Model class describing a workflow, which is a set of
        operating parameters for constructing bags, destined
        for a common location
    """
    name = ndb.StringProperty(required=True)
    icon = ndb.StringProperty(indexed=False, default="Gear.gif")
    version = ndb.IntegerProperty(default=1)
    destinationName = ndb.StringProperty(indexed=False)
    destinationUrl = ndb.StringProperty(indexed=False)
    destinationEmail = ndb.StringProperty(indexed=False)
    bagNameGenerator = ndb.StringProperty(indexed=False)
    packageFormat = ndb.StringProperty(indexed=False, default="zip")
    checksumType = ndb.StringProperty(indexed=False, default="md5")
    maxBagSize = ndb.IntegerProperty(indexed=False, default=-1)
    metadata = ndb.StructuredProperty(MetadataSpec, repeated=True)

class Agent(ndb.Model):
    """ Model class for group of workflows associated with an agent """
    name = ndb.StringProperty(required=True)
    trackVersion = ndb.BooleanProperty(default=True)
    workflows = ndb.IntegerProperty(repeated=True)
