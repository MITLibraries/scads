# scads - Small Capacity Application Data Service #

scads is an API server for smallish semi-structured data objects such as configurations, profiles, etc
The initial implementation supports only 'workflow' objects used by the HandBag tool: <https://github.com/MITLibraries/handbag>
It is basically a RESTful API server (JSON only) intended to support client tools and UIs. It was written expressly
to be run on Google AppEngine, and makes extensive use of its PaaS environment and services. Currently the service
is a prototype, lacking basic features such as authentication, but they could be added easily in future.

## Handbag API - Endpoints ##

The service exposes only 2 endpoints for use in Handbag contexts (admin UIs, the desktop tool):

### /workflows ###

A _GET_ request will return a list of all workflow URIs on the server. If the query parameter 'agent' is
supplied, only those associated with the named agent will be returned:

    http://mitlib-scads.appspot.com/workflows?agent=helen

A _POST_ to this URI with a JSON representation of a workflow will add it to the server, observing the following rule: if the _name_
of the posted workflow matches any existing one on the server it will be considered a _new_ version of that workflow,
otherwise it will be considered a new workflow. Versions have special behavior associated with them, viz. all
suitably configured agents will be 'upgraded' to this version, and will no longer have access to previous versions. The version number
will be automatically set to one higher than the highest currently on the server for that workflow.
New workflows, however, have no agent impact at all.

A _PUT_ to this URI with a JSON representation of an agent will create or update the set of workflows associated with the agent.
The agent is implicitly created by this PUT, and does not need to have pre-existed on the server. There is no direct way to purge
an agent once defined, but one could effectively deactivate an agent by PUTing the JSON:

    {
      "id": "jeremy",
      "name": "jeremy",
      "workflows": []
    }

Normally, the "workflows" list would contain some real workflow ids: [324098234098, 234290348920, 2342938423]

### /workflow ###

A _GET_ request with a query parameter correctly identifying a workflow will return a JSON representation of it:

    http://mitlib-scads.appspot.comm/workflow?id=4645645754

A _DELETE_ request with a query parameter correctly identifying a workflow will cause the workflow to be removed from the
server. All agent associations with the workflow will also be eliminated, without installing any replacement workflow - e.g. an
earlier version - for the agent.

## Deployment ##

Like most PaaS services, AppEngine has _push-button_ deployment. The AppEngine SDK includes a tool to easily manage the process.
In the directory above where this code is installed ('scads'), simply run:

    appcfg.py update scads/

The service will automatically create a new version of the runtime while retaining the previous one in case a roll-back
becomes necessary. Remember to rename the application (in app.yaml) since GAE requires globally unique application names.

When test coverage and other production-related build processes are added, the app can be configured to deploy directly
from travis CI, so merging a GitHub PR can lead to immediately updated code on the server.
