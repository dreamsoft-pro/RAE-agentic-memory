javascript
import { fetchLanguage } from '@/lib/api';

angular.module('dpClient.helpers')
  .factory('LangLoader', function (LangService) {
    return function(options) {
      const selectedLang = options.key || 'pl'; // [BACKEND_ADVICE]
      
      if (!selectedLang) {
        console.log("Undefined lang, selecting lang=pl");
      }
      
      return LangService.getLang(selectedLang);
    };
  });
