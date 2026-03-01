javascript
import { ConfigProvider } from '@/lib/api';

angular.module('dpClient.config')
  .provider('$config', ConfigProvider);

class ConfigProvider {
  constructor() {
    this.config = {};
  }

  set(key, val) {
    this.config[key] = val;
  }

  get(key) {
    return this.config[key];
  }

  $get() {
    return this.config;
  }
}

// [BACKEND_ADVICE] Heavy logic should be offloaded to backend services as needed.
