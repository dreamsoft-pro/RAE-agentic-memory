javascript
if (cache.get(this.resourceFullOptions) && !force) {
    def.resolve(cache.get(this.resourceFullOptions));
} else {
    const requestConfig = {
        method: 'GET',
        url: $config.API_URL + this.resourceFullOptions
    };

    // [BACKEND_ADVICE] Handle API call and cache update logic here.
    '@/lib/api'.get(requestConfig)
        .then((data) => {
            cache.put(this.resourceFullOptions, data);
            def.resolve(data);
        })
        .catch((error) => {
            def.reject(error);
        });
}

return def.promise;

AttributeService.prototype.getFullOptionsPublic = function (force) {
    const def = $q.defer();
    const _this = this;
