from ...infrastructure.db.driver_applications import retrieve_all_for_driver 
from ...infrastructure.db.driver_applications import retrieve_all_for_logist 

def get_all_driver_applications_for_driver(login):
    return retrieve_all_for_driver(login)

def get_all_driver_applications_for_logist(login):
    return retrieve_all_for_logist(login)
