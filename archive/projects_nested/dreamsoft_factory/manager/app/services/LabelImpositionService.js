angular.module('digitalprint.services')
    .service('LabelImpositionService', function ($http, $config) {
        const LabelImpositionService = {}
        const resource = 'labelImposition'

        LabelImpositionService.getForType = function (typeID) {
            return new Promise(function (resolve, reject) {
                $http({
                    method: 'GET',
                    url: $config.API_URL + resource + '/'+typeID
                }).success(function (response) {
                    return resolve(response)
                })
                    .error(function (response) {
                        return reject(response)
                    });
            })
        }

        LabelImpositionService.update = function (data) {
            if (data.ID) {
                return new Promise(function (resolve, reject) {
                    $http({
                        method: 'PUT',
                        url: $config.API_URL + resource + '/'+data.ID,
                        data:data
                    }).success(function (response) {
                        return resolve(response)
                    })
                    .error(function (response) {
                        return reject(response)
                    });
            }
        )
        }
    else
        {
            return new Promise(function (resolve, reject) {
                $http({
                    method: 'POST',
                    url: $config.API_URL + resource,
                    data:data
                }).success(function (response) {
                    return resolve(response)
                })
                    .error(function (response) {
                        return reject(response)
                    });
            })
        }
    }

LabelImpositionService.generate = function (labelImpositionID, dpProductID, calcProductID, calcProductFileID, copyToSpecialFolders) {
    return new Promise(function(resolve, reject) {
        $http({
            method: 'GET',
            url: $config.API_URL + resource + '/generate/'+labelImpositionID+'/'+dpProductID+'/'+calcProductID+'/'+calcProductFileID+'/'+copyToSpecialFolders
        }).success(function (response) {
            return resolve(response)
        })
            .error(function (response) {
                return reject(response)
            });
    })
}

return LabelImpositionService
})
