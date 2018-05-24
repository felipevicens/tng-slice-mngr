#!/usr/bin/python
import os, sys, requests, json, logging
from flask import jsonify

import database.database as db

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("slicemngr:repo")
LOG.setLevel(logging.INFO)



#################################### Sonata Repositories information #####################################
def get_base_url():
    #http://tng-rep:4012/records/nsir/ns-instances
    ip_address=db.settings.get('SLICE_MGR','SONATA_REPO')
    base_url = 'http://'+ip_address+':4012'
    
    return base_url


####################################### /records/nsir/ns-instances #######################################
#POST to send the NSI information to the repositories
def safe_nsi(NSI_string):
    LOG.info("NSI_MNGR2REPO: Sending information to the repositories")
    url = get_base_url() + '/records/nsir/ns-instances'
    header = {'Content-Type': 'application/json'}
    data = json.dumps(NSI_string)
    response = requests.post(url, data, headers=header, timeout=1.0, )
    jsonresponse = json.loads(response.text)
    
    if (response.status_code == 200):                                              #TODO: change the value according to tng-rep when this will be changed
        LOG.info("NSI_MNGR2REPO: NSIR storage accepted.")
    else:
        error = {'http_code': response.status_code,
                 'message': response.json()}
        jsonresponse = error
        LOG.info('NSI_MNGR2REPO: nsir to repo failed: ' + str(error))
    
    return jsonresponse


#GET all NSI information from the repositories
def getAll_saved_nsi():
    LOG.info("NSI_MNGR2REPO: Requesting all NSIs information from repositories")
    url = get_base_url() + '/records/nsir/ns-instances'
    header = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=header)
    LOG.info(response.text)
    jsonresponse = json.loads(response.text)
    
    if (response.status_code == 200):                                              #TODO: change the value according to tng-rep when this will be changed
        LOG.info("NSI_MNGR2REPO: all NSIR received.")
    else:
        error = {'http_code': response.status_code,
                 'message': response.json()}
        jsonresponse = error
        LOG.info('NSI_MNGR2REPO: nsir getAll from repo failed: ' + str(error))
    
    return jsonresponse


  
######################## /records/nsir/ns-instances/<service_instance_uuid> #############################
#GET specific NSI information from the repositories
def get_saved_nsi(nsiId):
    LOG.info("NSI_MNGR2REPO: Requesting NSI information from repositories")
    url = get_base_url() + '/records/nsir/ns-instances/' + nsiId
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers)
    jsonresponse = json.loads(response.text)
    
    if (response.status_code == 200):                                              #TODO: change the value according to tng-rep when this will be changed
        LOG.info("NSI_MNGR2REPO: NSIR received.")
    else:
        error = {'http_code': response.status_code,
                 'message': response.json()}
        jsonresponse = error
        LOG.info('NSI_MNGR2REPO: nsir get from repo failed: ' + str(error))
    
    return jsonresponse

#TODO: do we send all the invariant information (i.e.: name, id, etc) again with the changed paramters? 
#PUT update specific NSI information in repositories
def update_nsi(updatedata, nsiId):
    LOG.info("NSI_MNGR2REPO: Updating NSI information")
    url = get_base_url() + '/records/nsir/ns-instances/' + nsiId
    headers = {'Content-Type': 'application/json'}
    data = updatedata
    response = requests.put(url, headers, data)
    jsonresponse = json.loads(response.text)
    
    if (response.status_code == 200):                                              #TODO: change the value according to tng-rep when this will be changed
        LOG.info("NSI_MNGR2REPO: NSIR updated.")
    else:
        error = {'http_code': response.status_code,
                 'message': response.json()}
        jsonresponse = error
        LOG.info('NSI_MNGR2REPO: nsir update action to repo failed: ' + str(error))
    
    return jsonresponse

#DELETE soecific NSI information in repositories
def delete_saved_nsi(nsiId):
    LOG.info("NSI_MNGR2REPO: Deleting NSI")
    url = get_base_url() + '/records/nsir/ns-instances/' + nsiId
    response = requests.delete(url)
    jsonresponse = json.loads(response.text)
    
    if (response.status_code == 200):                                              #TODO: change the value according to tng-rep when this will be changed
        LOG.info("NSI_MNGR2REPO: NSIR deleted.")
    else:
        error = {'http_code': response.status_code,
                 'message': response.json()}
        jsonresponse = error
        LOG.info('NSI_MNGR2REPO: nsir delete action to repo failed: ' + str(error))
    
    return jsonresponse