ACTIVE = 'ACTIVE'
NOT_STARTED = 'NOT_STARTED'
TERMINATED = 'TERMINATED'


EMPLOYEE_ACTIVE_STATUS = [
    (ACTIVE, 'Active'),
    (NOT_STARTED, 'Not Started'),
    (TERMINATED, 'Terminated'),
]


DEPARTMENT = 'DEPARTMENT'
CONTACTS = 'CONTACTS'
POSITIONS = 'POSITIONS'
LOCATION = 'LOCATION'
COMPANY = 'COMPANY'

LIST_RELATION_DISPLAY =  ['department', 'contacts', 'positions', 'location', 'company']

DISPLAY_FIELDS = [
    (DEPARTMENT, 'department'),
    (CONTACTS, 'contacts'),
    (POSITIONS, 'positions'),
    (LOCATION, 'location')
]


class RateLimitConfig:
    LIMIT = 10
    PERIOD = 60
