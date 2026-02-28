javascript
if (cache.get(this.resource) && !force) {
    def.resolve(cache.get(this.resource));
} else {
    Restangular.all(_this.resourcePublic).getList().then(function (data) {
        cache.put(_this.resource, data.plain());
        def.resolve(data.plain());
    }, function (error) {
        def.reject(error);
    });
}

return def.promise;

PageService.prototype.getCustomNames = function () {
    var def = $q.defer();
    var resource = 'ps_pages';

    Restangular.all(resource).one('customName', this.typeID).get().then(function (data) {
        def.resolve(data.plain());
    }, function (error) {
        def.reject(error);
    });

    return def.promise;
};

return PageService;

})();
