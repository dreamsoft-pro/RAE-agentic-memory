javascript
import { Api } from '@/lib/api';
import _ from 'lodash';

angular.module('dpClient.app')
    .controller('SliderCtrl', function ($scope, $rootScope, SettingService) {

        $scope.slides = [];
        $scope.sliderText = '';

        $rootScope.$on('Slider:data', function (event, data) {
            $scope.slides = [];
            $scope.sliderOptions = {
                sliderAutoSlide: 3,
                sliderTransition: 'slide'
            };

            if (!_.isEmpty(data)) {
                const settingApi = new Api(SettingService);
                
                // [BACKEND_ADVICE] Heavy logic to fetch public settings
                settingApi.getPublicSettings('bannerSlider').then(function(settingsData) {
                    if (settingsData.sliderAutoSlide) {
                        $scope.sliderOptions.sliderAutoSlide = settingsData.sliderAutoSlide.value;
                    }
                    if (settingsData.sliderTransition) {
                        $scope.sliderOptions.sliderTransition = settingsData.sliderTransition.value;
                    }
                });
            }
        });
    });
