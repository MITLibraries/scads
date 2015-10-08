import logging
from webapp2 import RequestHandler, Route, WSGIApplication
from webapp2_extras import json
from google.appengine.ext import ndb
from models import Agent, Workflow

class WorkflowsHandler(RequestHandler):

    def get(self):
        agent = find_agent(self.request)
        if agent is None:  # get 'em all
            wf_list = { "workflows" : [build_uri(self, key.id()) for key in Workflow.query().iter(keys_only=True)] }
        else: # just those for agent
            wf_list = { "workflows" : [build_uri(self, key_id) for key_id in agent.workflows] }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(wf_list))

    def post(self):
        workflow = Workflow(**json.decode(self.request.body))
        versions = Workflow.query(Workflow.name == workflow.name).order(-Workflow.version).fetch(1)
        if any(versions): # bump version to one greater that last known one
            workflow.version = versions[0].version + 1
        new_key = workflow.put()
        logging.info("Create/update: %s", new_key.id())
        if any(versions): # replace earlier with this version in relevant agent workflow sets
            old_id = versions[0].key.id()
            for agent in Agent.query(Agent.trackVersion == True, Agent.workflows == old_id):
                agent.workflows.remove(old_id)
                agent.workflows.append(new_key.id())
        self.redirect('/workflows')

    def put(self):
        agent = Agent(**json.decode(self.request.body))
        agent.put()

class WorkflowHandler(RequestHandler):

    def get(self):
        workflow = find_workflow(self.request)
        if workflow is None:
            self.error(404)
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.encode(workflow.to_dict()))

    def delete(self):
        workflow = find_workflow(self.request)
        if workflow is None:
            self.error(404)
        else: # remove from agent workflow sets then delete
            for agent in Agent.query(Agent.workflows == workflow.key.id()):
                agent.workflows.remove(workflow.key.id())
            workflow.key.delete()

def find_workflow(request):
    wflow_id = request.get("id")
    if wflow_id:
        return ndb.Key(Workflow, int(wflow_id)).get()

def find_agent(request):
    agent_id = request.get("agent")
    if agent_id:
        return ndb.Key(Agent, agent_id).get()

def build_uri(handler, key_id):
    return RequestHandler.uri_for(handler, 'workflow', _full=True) + "?id=" + str(key_id)

app = WSGIApplication([
    Route('/workflows', handler=WorkflowsHandler, name='workflows'),
    Route('/workflow', handler=WorkflowHandler, name='workflow')], debug=True)
