devicedb yaml setup

Inspired most recently by https://github.com/Flipkart/HostDB

A directory has yaml files. No db (except maybe a caching one in the future)

### Operations create, update, delete:

create:

  - create file (verify does not exist)
  - add file to git
  - commit to git

update:

  - generate new file
  - commit into git

delete:

  - git rm file


namespace/
|- devices/
|   | -- server1
|   | -- server2
|- tags/
|   | -- tag1
|   | -- tag2


servers are grouped by tags

server1:
    id: server1
    Description: A utility server for the example product
    Network:
      cname: utility1.example.com
      fqdn: vhost103.example.com
      ip: undef
      upstream: router1
    Pysical Location:
      Building: Main Store
    Status: Live
    Monitoring:
      https:
        url: https://utility1.example.com/status.php
        match: OK
      ssl:
        url: https://utility1.example.com/
        time-to-expire: 30

tag1:

    name: tag1
    description: Example Product related servers
    members:
      - server1




### URL/API

get full entry

  - all tags: /get/tags/
  - tag1: /get/tags/tag1
  - all devices: /get/devices/
  - server1: /get/devices/server1

create/update device/tag:
  - POST: /update/{devices;tags}/server1  (data contains yaml)
  - verifies yaml, authorization, returns ok

delete device:
  - POST: /delete/devices/server1
  - verifies action
  - special action: scan tags for server and remove as member
  - returns ok

delete tag:
  - POST /delete/tag/tag1
  - verifies, returns OK

add server1 to tag1:
  - /members/tag1/add/server1

remove server1 from tag1:
  - /members/tag1/remove/server1

get members from tag:
  - /get/members/tag1


### Thoughts

 - Could be doable with bottle + python
 - Perhaps a json export option (add /json to end of url)
 - Git commit hooks could push on commit
 - devicedb-core would be super minimal
 - worry about authentication and frontend later


