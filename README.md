# Setup  
Require requests.  
```
pip (or pip3) install requests
```  
Also you need prepare the `secret.py` by yourself.  
see the `secret_sample.py` for example.

# Usage  
You can embed this program in your code.  
see the `test_notification.py` for example.  
Also it is one way to use in pipe.  
For example,  
```
hogehoge | python test_notification.py
```  
This will make `test_notification.py` run after `hogehoge` ended.