'use strict';

angular.module('paginationAPI', [])
	.factory('Pagination', function($filter, $document) {

		var multipleSort = false;

		$document.keydown(function(e) {
			if(e.keyCode === 17) {
				multipleSort = true;
			}
		});
		$document.keyup(function(e) {
			if(e.keyCode === 17) {
				multipleSort = false;
			}
		});

		return {

			//z settings bierze maxSize i numberOfPages
			//wykorzystane w templatkach
			rangePage: function(settings) {

		        var start = 0;
		        var stop = settings.numberOfPages;
		        if(settings.numberOfPages > settings.maxSize) {
		            start = Math.max( settings.currentPage - Math.floor(settings.maxSize/2) , 0);
		            stop = start + settings.maxSize;
		            
		            if(stop > settings.numberOfPages) {
		                stop = settings.numberOfPages;
		                start = stop - settings.maxSize;
		            }        
		            
		            
		        }
		        
		        return _.range(start, stop);
		    },
		    setPage: function(settings, page) {
		        if(page >=0 && page < settings.numberOfPages) {
		            settings.currentPage = page;
		        }

		    },
		    search: function(srcTable, settings, searchItem, onlyRefresh) {
		        var filteredTable = $filter('filter')(
		            srcTable,
		            searchItem
		            
		        );


		        if(settings.sortingOrder !== '') {
		            filteredTable = $filter('orderBy')(filteredTable, settings.sortingOrder);
		        }
		        
		        if(onlyRefresh) {
		        	settings.numberOfPages = Math.ceil(filteredTable.length/settings.pageSize);
		        	if(settings.currentPage >= settings.numberOfPages) {
		        		settings.currentPage = settings.numberOfPages-1;
		        	}
		            return filteredTable;
		        }
		        
		        settings.currentPage = 0;
		        settings.numberOfPages = Math.ceil(filteredTable.length/settings.pageSize);


		        return filteredTable;
		    },
		    sortBy2: function(orderBy) {
		      // sprawdzamy czy nie klikamy w to samo bez multiple sort
		      if( !($scope.sortArray.length === 1 && _.contains($scope.sortArray, orderBy)) ) {
		        // kasujemy
		        if(!multipleSort) {
		          $scope.sortArray = [];
		        }
		      }
		      if(_.contains($scope.sortArray, orderBy)) {
		        $scope.sortArray = _.without($scope.sortArray, orderBy);
		        $scope.sortArray.push('-'+orderBy);
		      } else if(_.contains($scope.sortArray, '-'+orderBy)) {
		        $scope.sortArray = _.without($scope.sortArray, '-'+orderBy);
		        $scope.sortArray.push(orderBy);
		      } else {
		        $scope.sortArray.push(orderBy);
		      }
		      console.log($scope.sortArray);
		    },
		    sortBy: function(srcTable, settings, searchItem, newSortOrder) {
		    	console.log(newSortOrder);

		    	// newSortOrder = ''+newSortOrder;
		    	//sprawdzamy czy już jest wybrane sortowanie po danym sortOrder
		    	if(_.contains(settings.sortingOrder, newSortOrder)
		    		|| _.contains(settings.sortingOrder, '-'+newSortOrder)) {


		    		//sprawdzamy czy już wcześniej nie było tego sortOrder wpisane do reverse
		    		if(_.contains(settings.sortingReverse, newSortOrder)) {
		    			settings.sortingReverse = _.without(settings.sortingReverse, newSortOrder);
		    			//usuwamy wpis z przeciwnością i dajemy zwykły
		    			settings.sortingOrder = _.without(settings.sortingOrder, '-'+newSortOrder);
		    			settings.sortingOrder.push(newSortOrder);

		    		} else {

			    		if(!multipleSort) {
				        	//czyścimy tablicę jeżeli nie jest multipleSort
				    		settings.sortingOrder = [];
				    		settings.sortingReverse = [];
				    	}

		            	settings.sortingReverse.push(newSortOrder);
		            	//usuwamy wpis z listy sortowanych elementów
		            	settings.sortingOrder = _.without(settings.sortingOrder, newSortOrder);
		            	//dodajemy przeciwność
		            	settings.sortingOrder.push('-'+newSortOrder);

		            }

		        } else {

			        if(!multipleSort) {
			        	//czyścimy tablicę jeżeli nie jest multipleSort
			    		settings.sortingOrder = [];
			    		settings.sortingReverse = [];
			    	}

			    	settings.sortingOrder.push(newSortOrder);

		        }

		        console.log(settings);
		        //console.log(settings);
		        
		        return this.search(srcTable, settings, searchItem, true);
		        
		    }
		}
	});