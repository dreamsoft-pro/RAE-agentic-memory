angular.module('digitalprint.app')
    .controller('printshop.ConfigAttributesCtrl', function($scope, $modal, $filter, $config,
                                                           Notification, PsConfigAttributeService, FileUploader,
                                                           PsConfigAttributeTypeService, PsConfigAttributeNatureService,
                                                           AuthDataService) {

        $scope.specialFunctions = ["", "rotation", "rounding", "cuttingDie"]
        $scope.attributes = [];

        resetForm();

        $scope.sortChange = false;

        $scope.sortableOptions = {
          stop: function(e, ui) {
            $scope.sortChange = true;
          },
          axis: 'y',
          placeholder: 'success',
          handle: 'button.button-sort',
          cancel: ''
        };

        PsConfigAttributeService.getAll(true).then(function(data) {
            $scope.attributes = data;
            console.log(data);
        }, function(data) {
            Notification.error($filter('translate')('error'));
        });

        $scope.countProducts = {};
        PsConfigAttributeService.countProducts().then(function(data) {
            $scope.countProducts = data;
        });

        PsConfigAttributeTypeService.getAll().then(function(data) {
            $scope.types = data;
        });

        PsConfigAttributeNatureService.getAll().then(function(data) {
            $scope.natures = [{ID:null, function:'blank'}].concat(data);
        });

        function resetForm() {
            $scope.form = {};
            $scope.form.type = 1;
        }

        $scope.getCountProducts = function(item) {
            var find = _.find($scope.countProducts.attrs, {
                attrID: item.ID
            });
            return find ? find.count : 0;
        }

        $scope.getTypeName = function(item) {
            var elem = _.findWhere($scope.types, {
                ID: item.type
            });

            return elem ? elem.name : '...';
        }

        $scope.refresh = function() {
            PsConfigAttributeService.getAll(true).then(function(data) {
                $scope.attributes = data;
            });
            $scope.sortChange = false;
        }

        $scope.sortCancel = function() {
            $scope.refresh();
        }

        $scope.sortSave = function() {

            var result = [];
            _.forEach($scope.attributes, function(elem) {
                result.push(elem.ID);
            });

            PsConfigAttributeService.sort(result).then(function(data) {
                $scope.sortChange = false;
            });
        }

        $scope.copy = function(attr) {

            PsConfigAttributeService.copy(attr.ID).then(function(data) {
                $scope.refresh();
                Notification.success($filter('translate')('success'));
            }, function(data) {
                Notification.error($filter('translate')('error'));
            })
        }

        $scope.add = function() {

            PsConfigAttributeService.add($scope.form).then(function(data) {
                $scope.attributes.push(data);
                resetForm();
                Notification.success($filter('translate')('success'));
            }, function(data) {
                Notification.error($filter('translate')('error'));
            });

        }

        $scope.editStart = function(elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-attribute.html',
                scope: $scope,
                controller: function($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = {};
                    $scope.form = angular.copy(elem);

                    $scope.save = function() {

                        PsConfigAttributeService.edit($scope.form).then(function(data) {
                            var idx = _.findIndex($scope.attributes, {
                                ID: $scope.form.ID
                            });
                            if (idx > -1) {
                                $scope.attributes[idx] = angular.copy($scope.form);
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function(data) {
                            Notification.error($filter('translate')('error'));
                        });

                    }

                    $scope.cancel = function() {
                        $modalInstance.close();
                    }

                }
            })
        }

        $scope.remove = function(elem) {

            PsConfigAttributeService.remove(elem).then(function(data) {
                var idx = _.findIndex($scope.attributes, {
                    ID: elem.ID
                });
                if (idx > -1) {
                    $scope.attributes.splice(idx, 1);
                }
                Notification.success($filter('translate')('removed') + " " + elem.name);
            }, function(data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.uploadIcon = function (attribute) {
            console.log('uploadIcon');
            $modal.open({
                templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                scope: $scope,
                backdrop: 'static',
                keyboard: false,
                controller: function ($scope, $modalInstance) {

                    var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

                    var header = {};
                    header[accessTokenName] = AuthDataService.getAccessToken();

                    var uploader = $scope.uploader = new
                    FileUploader({
                        'url': PsConfigAttributeService.getUploadUrl(),
                        queueLimit: 1,
                        headers: header,
                        'autoUpload': false
                    });

                    uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item, options) {
                            var itemName = item.name.split('.');
                            var lastItem = itemName.pop();
                            var possibleExtensions = ['jpg', 'jpeg', 'png', 'svg','webp'];

                            if (possibleExtensions.indexOf(lastItem) > -1) {
                                return true;
                            }
                            Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                            return false;
                        }
                    });

                    $scope.ok = function () {

                        var file = uploader.queue[0];
                        $scope.file = file;

                        var formData = [];

                        formData.push({'attributeID': attribute.ID});
                        file.formData = formData;

                        uploader.uploadItem(file);

                        uploader.onSuccessItem = function (fileItem, response, status, headers) {
                            if (response.response == true) {
                                attribute.icon = response.icon;
                                attribute.iconID = response.icon.ID;
                                attribute.iconUrl = response.icon.url;

                                var attributeIdx = _.findIndex($scope.attributes, {ID: attribute.ID});
                                if (attributeIdx > -1) {
                                    $scope.attributes[attributeIdx].iconID = attribute.iconID;
                                    $scope.attributes[attributeIdx].icon = attribute.icon;
                                    $scope.attributes[attributeIdx].iconUrl = attribute.iconUrl;
                                }
                                Notification.success($filter('translate')('file_uploaded'));
                                $modalInstance.close();
                            } else {
                                Notification.success($filter('translate')('uploading_problem'));
                            }
                        };
                    };

                    $scope.cancel = function () {
                        if (uploader.isUploading) {
                            alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                        } else {
                            $modalInstance.close();
                        }
                    };
                }
            });
        };

        $scope.deleteIcon = function (attribute) {

            PsConfigAttributeService.deleteIcon(attribute.ID).then(function (data) {
                if (data.response) {
                        attribute.icon = null;
                        attribute.iconID = null;
                        attribute.iconUrl = null;
                    var attributeIdx = _.findIndex($scope.types, {ID: attribute.ID});
                    if (attributeIdx > -1) {
                        $scope.attributes[attributeIdx].icon = null;
                        $scope.attributes[attributeIdx].iconID = null;
                        $scope.attributes[attributeIdx].iconUrl = null;
                        Notification.success($filter('translate')('deleted_successful'));
                    }
                }
            });

        };
    });
