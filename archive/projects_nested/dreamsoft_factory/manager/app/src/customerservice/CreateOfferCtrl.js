angular.module('digitalprint.app')
  .controller('customerservice.CreateOfferCtrl', function($scope, $timeout, $filter, $modal, $q, OfferService, PsGroupService, PsTypeService, PsAttributeService, PsFormatService, PsPageService, AuctionService, ApiCollection, Notification){

    OfferService.getAll().then(function(data) {
      // console.log(data);
      $scope.offers = data;
    }, function(data) {
      Notification.error($filter('translate')('data_retrieve_failed'));
    });

    OfferService.getCurrent().then(function(data) {
      $scope.currentOffer = data;
      console.log('currentOffer', $scope.currentOffer);
      _.each($scope.currentOffer.items, function(item) {
        item.fileList = [];
        $scope.getItemFiles(item);
      });
    }, function(data) {
      Notification.error($filter('translate')('data_retrieve_failed'));
    });

    PsGroupService.getAll().then(function(data) {
      $scope.products = data;
    }, function(data) {
      Notification.error($filter('translate')('data_retrieve_failed'));
    });

    $scope.currentProduct = false;
    $scope.currentType = false;
    $scope.currentFormat = false;

    $scope.currentPages = false;
    $scope.selectedOptions = {};
    $scope.productItem = {};
    $scope.productItem.deliveryType = 'single';

    var AttributeService;
    var FormatService;

    var PagesService;
    var isAuctionUser = false;

    $scope.singleDeliveries = [
      { value: 'NO LIMIT', name: 'NO LIMIT' },
      { value: 'Inforsys', name: 'Inforsys'},
      { value: 'other', name: 'Inne'}
    ];

    $scope.agencies = [
      { value: 'Saatchi', name: 'Saatchi' },
      { value: 'SGM', name: 'SGM' },
      { value: 'Integraf', name: 'Integraf' },
      { value: 'S4', name: 'S4'},
      { value: 'PRS Multanowski', name: 'PRS Multanowski'},
      { value: 'Simplicity', name: 'Simplicity'},
      { value: 'other', name: 'Inna' }
    ];

    /*
    Użytkownicy do wyszukania 
    */
    $scope.userLimit = 10;
    var usersConfig = {
      // count: 'users/count',
      params: {
        limit: $scope.userLimit
      },
      onSuccess: function(data){
        console.log('users update',data);
        $scope.usersCollection.items = data;
      }
    };

    $scope.usersCollection = new ApiCollection('users/searchAll', $scope.usersConfig);
    
    var updateTableTimeout;
    $scope.findUser = function(val) {
      console.log(val);
      $scope.usersCollection.params.search = val;
      $timeout.cancel(updateTableTimeout);

      updateTableTimeout = $timeout(function(){
        return $scope.usersCollection.clearCache().then(function(data) {
          $scope.usersCollection.items = data;
          console.log(data);
          console.log('items', $scope.usersCollection.items);
          return data;
        });
        // $scope.usersCollection.get();
      }, 300);
      return updateTableTimeout;

    }

    AuctionService.isAuctionUser().then(function(data) {
      isAuctionUser = true;
    });

    $scope.checkIfAuctionUser = function() {
      return isAuctionUser;
    }

    $scope.selectProduct = function(product) {
      $scope.types = [];
      $scope.currentProduct = product;
      PsTypeService.getAll($scope.currentProduct.ID).then(function(data) {
        $scope.types = data;
        // console.log($scope.types);
        if($scope.types.length === 1) {
          $scope.selectType($scope.types[0]);
        }
      }, function(data) {
        $scope.currentProduct = false;
        Notification.error($filter('translate')('data_retrieve_failed'));
      });
    }

    $scope.selectType = function(type) {
      $scope.currentType = type;
      $scope.selectedOptions = {};
      // $scope.groupOptions = {};
      $scope.attributes = {};
      $scope.currentFormat = false;
      $scope.currentPages = false;
      $scope.excludedOptions = [];
      $scope.formatExcluded = [];
      // Pobieranie formatów, cech

      AttributeService = new PsAttributeService($scope.currentProduct.ID, $scope.currentType.ID);
      FormatService = new PsFormatService($scope.currentProduct.ID, $scope.currentType.ID);
      PagesService = new PsPageService($scope.currentProduct.ID, $scope.currentType.ID);

      $q.all([
        FormatService.getAll(),
        PagesService.getAll(),
        AttributeService.getFullOptions()
      ]).then(function(data) {
        $scope.formats = data[0];
        // $scope.productAttributes = data[1];

        $scope.pages = data[1];
        // console.log('getFullOptions', data[2]);
        $scope.attributes = data[2];
        // groupOptions(data[2]);

        $scope.selectFormat($scope.formats[0]);
        if($scope.pages.length && $scope.pages[0].pages) {
          $scope.selectPages($scope.pages[0].pages);
        }
        if($scope.pages.length && $scope.pages[0].minPages) {
          $scope.selectPages($scope.pages[0].minPages);
        }

        // console.log(data);
      }, function(data) {
        $scope.goToTypes();
        Notification.error($filter('translate')('data_retrieve_failed'));
      });
    }

    $scope.selectFormat = function(format) {
      if(format.custom) {
        format.customWidth = format.minWidth;
        format.customHeight = format.minHeight;
      }
      $scope.currentFormat = format;
      // $scope.currentAttributes = _.clone($scope.attributes, true);
      // checkOptionsFormats();
      $scope.checkFormatExclusions();

      $scope.selectDefaultOptions();
    }

    $scope.checkFormatExclusions = function() {
      $scope.formatExcluded = [];
      _.each($scope.attributes, function(attribute, attrIdx) {
        // console.log('attribute.options', attribute.options);
        _.each(attribute.options, function(option, optIdx) {
          // console.log('option', option);
          if(option && option.formats) {
            if(!_.contains(option.formats, $scope.currentFormat.ID)) {
              $scope.formatExcluded.push(option.ID);
              // usuwamy też z zaznaczonych jeżeli tam występuje
              if($scope.selectedOptions[attribute.attrID] == option.ID) {
                delete $scope.selectedOptions[attribute.attrID];
              }
            }
          }
        });
      });

    }

    $scope.selectPages = function(pages) {
      $scope.currentPages = pages;
    }


    $scope.selectDefaultOptions = function() {
      _.each($scope.attributes, function(item) {
        // console.log(item);
        if(!$scope.selectedOptions[item.attrID]
          ) {
          var tmp = item.options[_.first(_.keys(item.options))];
          // console.log('option', tmp);
          $scope.selectOption(item.attrID, tmp);
        }
      });
      // console.log('selected', $scope.selectedOptions);
    }

    $scope.selectOption = function(attrID, item) {
      // parsuje wszystko na 
      $scope.selectedOptions[attrID] = $scope.selectedOptions[attrID]+"";

      if(item === undefined) {
        var optID = $scope.selectedOptions[attrID];
        var item = getOption(optID);
        // console.log(optID);
        if(item === undefined) {
          console.log('nie znaleziono opcji');
          return false;
        }
      }
      $scope.selectedOptions[attrID] = item.ID+"";
      $scope.setExclusions();

      $scope.selectDefaultOptions();
    }

    var getOption = function(optID) {
      optID = parseInt(optID);
      var item = undefined;
      // szukamy po current Attributes
      _.each($scope.attributes, function(attribute) {
        var idx = _.findIndex(attribute.options, {ID: optID});
        // console.log(attribute.options, idx);
        if(idx > -1) {
          item = attribute.options[idx];
          return false;
        }
      });

      return item;
    }

    $scope.setExclusions = function() {
      $scope.excludedOptions = _.clone($scope.formatExcluded);
      // console.log($scope.excludedOptions);
      _.each($scope.selectedOptions, function(optID, attrID) {
        // console.log(optID);
        if(!optID) {
          return false;
        }
        var item = getOption(optID);
        // console.log('item', item)
        if(item.exclusions) {
          $scope.setOptionExclusions(item.exclusions);
        }
      });
    }

    $scope.setOptionExclusions = function(exclusions) {
      // dla każdego exclusion szukamy tej opcji w atrybutach
      _.each($scope.attributes, function(attribute) {

        if(exclusions[attribute.attrID]) {

          // _.each(exclusions, function(exclusionsArray, attrID) {
          _.each(attribute.options, function(option) {
            // console.log(option);
            if(_.contains(exclusions[attribute.attrID], option.ID)) {
              $scope.excludedOptions.push(option.ID);
              // usuwanie z selectedOptions

              if($scope.selectedOptions[attribute.attrID] == option.ID) {
                delete $scope.selectedOptions[attribute.attrID];
              }
              // _.each($scope.selectedOptions, function(val, key) {
              //   if(val === option.ID) {
              //     delete $scope.selectedOptions[key];
              //     return false;
              //   }
              // });
            }
            
          });
          // });
        }
      });

    }

    $scope.goToProducts = function() {
      $scope.currentProduct = false;
      $scope.currentType = false;
    }

    $scope.goToTypes = function() {
      $scope.currentType = false;
      if($scope.types.length === 1) {
        $scope.currentProduct = false;
      }
    }

    $scope.showOffers = function() {
      $modal.open({
        templateUrl: 'src/customerservice/templates/modalboxes/show-offers.html',
        scope: $scope
      })
    }

    $scope.addItem = function() {
      if($scope.productItem.singleDelivery == 'other') {
        $scope.productItem.singleDelivery = $scope.productItem.singleDeliveryOther;
        delete $scope.productItem.singleDeliveryOther;
      }

      var newItem = $scope.productItem;

      newItem.groupID = $scope.currentProduct.ID;
      newItem.typeID = $scope.currentType.ID;
      newItem.formatID = $scope.currentFormat.ID;
      if($scope.currentPages) {
        newItem.pages = $scope.currentPages;
      } else {
        newItem.pages = null;
      }
      newItem.options = [];
      _.each($scope.selectedOptions, function(optID, attrID) {
        // TODO AttrPages
        newItem.options.push({attrID: attrID, optID: optID});
      });
      
      // TODO formatWidth, formatHeight
      console.log($scope.currentFormat);
      if($scope.currentFormat.custom) {
        newItem.formatWidth = $scope.currentFormat.customWidth;
        newItem.formatHeight = $scope.currentFormat.customHeight;
      }
      // console.log($scope.productItem.deliveryType);
      if($scope.productItem.deliveryType === 'single' ) {
        $scope.productItem.multiDelivery = null;
      } else {
        $scope.productItem.singleDelivery = null;
      }
      // console.log(newItem);
      // return false;
      OfferService.addItem(newItem).then(function(data) {
        // console.log($scope.currentOffer, !$scope.currentOffer);
        if(!$scope.currentOffer) {
          $scope.currentOffer = data.offer;
          $scope.currentOffer.items = [];
        }
        if($scope.currentOffer.items === undefined) {
          $scope.currentOffer.items = [];
        }
        $scope.currentOffer.items.push(data.item);
        $scope.getItemFiles(data.item);
        $scope.productItem = {};
        $scope.productItem.deliveryType = 'single';


        $scope.goToProducts();
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      })
    }

    $scope.uploadItemFile = function(offerItem) {

      if(offerItem.files && offerItem.files.length) {
        _.each(offerItem.files, function(file) {
          OfferService.uploadItemFile(offerItem.ID ,file).progress(function(evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            // console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            offerItem.progress = progressPercentage;
          }).success(function(data, status, headers, config) {
            // console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            // console.log(data);
            offerItem.progress = 0;
            offerItem.fileList.push(data.file);
            Notification.success($filter('translate')('success'));
          }).error(function(data,status, headers, config) {
            console.log('error status' + status);
            Notification.error($filter('translate')('error' + status));
          });
        });
      }
    }

    $scope.getFile = function(file) {
      return OfferService.getFile(file.ID);
    }

    $scope.getItemFiles = function(offerItem) {
      OfferService.getItemFiles(offerItem.ID).then(function(data) {
        offerItem.fileList = data;
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    }

    $scope.removeItemFile = function(item, file) {
      OfferService.removeItemFile(file.ID).then(function(data) {
        var idx = _.findIndex(item.fileList, {ID: file.ID});
        if(idx > -1) {
          item.fileList.splice(idx, 1);
        }
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    }

    $scope.removeItem = function(item) {
      OfferService.removeItem(item.ID).then(function(data) {
        var idx = _.findIndex($scope.currentOffer.items, {ID: item.ID});
        if(idx > -1) {
          $scope.currentOffer.items.splice(idx, 1);
        }
        Notification.success($filter('translate')('success'));
      }, function(data) {
        console.log(data);
        Notification.error($filter('translate')('error'));
      })
    }

    $scope.sendOffer = function() {
      // console.log($scope.currentOffer);
      // return;
      if($scope.currentOffer.agency === 'other') {
        $scope.currentOffer.agency = $scope.currentOffer.agencyOther;
        delete $scope.currentOffer.agencyOther;
      }

      $scope.currentOffer.finished = 1;
      if(isAuctionUser && $scope.currentOffer.searchUser) {
        $scope.currentOffer.uID = $scope.currentOffer.searchUser.ID;
      }
      OfferService.update($scope.currentOffer).then(function(data) {
        // console.log(data);
        $scope.currentOffer = false;
      }, function(data) {
        console.log(data);
        Notification.error($filter('translate')('error'));
      })
    }

  });
