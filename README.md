☑️Mail  
☑️Slack  
☑️Twitter  

# Require  
At least require **requests, requests_oauthlib**.  
```
pip (or pip3) install requests equests_oauthlib
```  
Other kinds of libraries are the same.  
If you need, install it.  
Also you need to **prepare the `notificator_secrets.yaml`** by yourself.  
See the `example.yaml` for detail.

# Usage  
You can embed this module in your code.  
See the `test_notification.py` for example.  
Also, it is one way to use in pipe.  
For example,  
```
hogehoge | python notify.py
```  
This will make `notify.py` run after `hogehoge` ended.  
I recommend this style because we do not need to embed this in the code.  

# For Lazy People
You can just use `notify.py`  
Only you need to do is rewrite the secret in the code or `notificator_secrets.yaml` for your setting.  

# setup_alias.sh
It will set up a alias of "python notify.py" to notify in your rc file.