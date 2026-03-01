/**
 * Created by Rafał on 15-09-2017.
 */
angular.module('digitalprint.services')
    .factory('MainWidgetService', function () {

        function MainWidgetService(json) {
            angular.extend(this, json);
        }

        function compareDates(a, b) {
            if( !a || !b ) {
                return -1;
            }
            var firstValue = a.split('-');
            var secondValue = b.split('-');

            var firstDate = new Date();
            firstDate.setFullYear(firstValue[0], (firstValue[1] - 1 ), firstValue[2]);

            var secondDate = new Date();
            secondDate.setFullYear(secondValue[0], (secondValue[1] - 1 ), secondValue[2]);

            if (firstDate > secondDate) {
                return true;
            } else {
                return false;
            }
        }

        function formatSizeUnits(bytes) {
            if (bytes >= 1073741824) {
                bytes = (bytes / 1073741824).toFixed(2) + ' GB';
            }
            else if (bytes >= 1048576) {
                bytes = (bytes / 1048576).toFixed(2) + ' MB';
            }
            else if (bytes >= 1024) {
                bytes = (bytes / 1024).toFixed(2) + ' KB';
            }
            else if (bytes > 1) {
                bytes = bytes + ' bytes';
            }
            else if (bytes === 1) {
                bytes = bytes + ' byte';
            }
            else {
                bytes = '0 byte';
            }
            return bytes;
        }

        return {
            formatSizeUnits: formatSizeUnits,
            compareDates: compareDates
        };
    });