
import sys
from resources.lib.modules.plugin import router
 
if __name__=='__main__':
_handle = int(sys.argv[1])
_params = sys.argv[2][1:]

dispatcher = router.Router()
dispatcher.dispatch(_handle, _params)

