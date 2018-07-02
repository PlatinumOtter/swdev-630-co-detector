# swdev-630-co-detector

Example GET for a user

`curl http://127.0.0.1:5000/alerts/daniel`

Example POST alert

`curl --header "Content-Type: application/json" --data '{"User":["daniel","mike"],"EnvParam":"CO","Threshold":"10000"}' http://127.0.0.1:5000/alerts`

Example Update

`curl --header "Content-Type: application/json" --data '{"RegValue":"500"}' http://127.0.0.1:5000/update/CO`