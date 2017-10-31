import requests, os, sys, re, json

args = sys.argv[1:] 
argNr = 0
for i in args:
    if re.match('--mode', i):
        mode = args[argNr + 1]
    if re.match('--ip', i):
        ip = args[argNr + 1]
    argNr = argNr + 1

metronome_get  = 'http://' + ip + ':9000/v1/jobs?embed=schedules'
metronome_post = 'http://' + ip + ':9000/v0/scheduled-jobs'

headers = { 'Accept': 'application/json', 
            'Cache-Control': 'no-cache',
            'Content-type': 'application/json' }
    
if mode == 'backup':
    response = requests.get(metronome_get, headers=headers)
    metronome_jobs = response.json()
    with open('metronome_scheduled-jobs.json', 'w') as job:
        json.dump(metronome_jobs, job)
        print 'Metronome response: ' + response.text
    print 'Metronome backup finished'
    
elif mode == 'restore':
    with open('metronome_scheduled-jobs.json', 'r') as metronome_jobs:    
        jobs = json.load(metronome_jobs)
    for i in xrange(1,len(jobs)):
        job_data = json.dumps(jobs[i])
        response = requests.post(metronome_post, data=job_data, headers=headers)
        print 'Metronome response: ' + response.text
    print 'Metronome restore finished'
    