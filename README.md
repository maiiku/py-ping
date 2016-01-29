# py-ping
Python 2 implementaion of basic ping functionality using socket.IPPROTO_ICMP

## Params
* *host* - ip or hostname. Required.
* *c* - number of ping, pass `True` for continous ping. Defautl: 1
* *timeout* - timeout in seconds for pinging. Default: 1
* *logger* - function to use for logging. Must accept string to be logged. Default: prints to console

## Usage
```python
req = Ping('8.8.8.8')
>> ping 8.8.8.8: 0.042927980423
req.result
>> True
Ping('google.com', c=3)
>> ping google.com: 0.0410561561584
>> ping google.com: 0.0430269241333
>> ping google.com: 0.0418059825897
Ping('doesnotexist.xcc')
>> Unknown host: doesnotexist.xcc
```
