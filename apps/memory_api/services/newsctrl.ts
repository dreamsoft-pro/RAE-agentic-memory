javascript
'use strict';

import { getRss } from '@/lib/api/news';
import { BackendAdvice } from '@/lib/utils/backend-advice';

angular.module('dpClient.app')
    .controller('index.NewsCtrl', function($scope) {
        $scope.articles = [];

        function init() {
            getNews();
        }

        async function getNews() {
            try {
                const data = await getRss();
                BackendAdvice.logHeavyOperation('Fetching news RSS');
                if (data.items) {
                    $scope.articles = data.items;
                }
            } catch (error) {
                console.error('Failed to fetch news:', error);
            }
        }

        init();
    });
