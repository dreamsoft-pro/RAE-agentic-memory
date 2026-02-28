angular.module('digitalprint.app')
    .controller('orders.ProductsCtrl', function ($scope, $state, $filter, $modal, $timeout, $window, ApiCollection,
                                                    DpProductService, Notification, OperationService,
                                                    ProductCardService, RealizationTimeService, OngoingService) {


        OperationService.getAll().then(function (data) {
            $scope.operations = data;
        });

        $scope.showRows = 25;
        $scope.productsConfig = {
            count: 'dp_products/count',
            params: {
                accept: 1,
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.dpProducts.items = data;
                console.log(data);
                setTimeout(function () {
                    $('.div1').width($('.overflowContainer > table').outerWidth());
                }, 300);
            }
        };

        $scope.realisationTimes = [];
        $scope.realisationColors = {
            0: '#45b6af',
            1: '#E26A6A',
            2: '#ffe567'
        };

        if ($state.params.productID) {
            $scope.productsConfig.params.ID = $state.params.productID;
        }

        $scope.dpProducts = new ApiCollection('dp_products', $scope.productsConfig);
        $scope.dpProducts.get();

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.dpProducts.get();
            }, 1000);
        };

        function init() {
            RealizationTimeService.getAll().then(function (data) {
                _.each(data, function (one, index) {
                    if (one.color === null || one.color === '') {
                        one.color = $scope.realisationColors[index % 3];
                    }
                });
                $scope.realisationTimes = data;
            });

            $scope.dpProducts.clearCache();
        }

        init();

        $scope.getProductCard = function (product) {

            ProductCardService.get(product.ID).then(function (data) {
                if (data.success === true) {
                    $window.open(data.link, '_blank');
                }
            });

            return true;
        };

        $scope.getProductXml = function (product) {

            ProductCardService.getXml(product.ID).then(function (data) {
                if (data.success === true) {
                    $window.open(data.link, '_blank');
                }
            });

            return true;
        };

        $scope.noAccept = function(product) {
            var accept = -1;
            DpProductService.accept(product.ID, accept).then(function(data) {
                Notification.success($filter('translate')('success'));
                $scope.setParams();
            }, function(data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.showUserAddress = function( product ) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/user-address-data.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope) {
                    $scope.product = product;
                }
            });
        };

        var globalongoingData = null;

        $scope.showOngoingDetails = function( subProduct ) {

            var modal = $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/production-details.html',
                scope: $scope,
                resolve: {
                    ongoingData: function () {
                        console.log("subProduct.ID"+subProduct.ID);
                        return OngoingService.showForItem(subProduct.ID).then(function (ongoingData) {
                            return ongoingData;
                        });
                    }
                },
                size: 'lg',
                controller: function ($scope, $document, ongoingData) {

                    $scope.changeScale = function( scaleName ) {
                        gantt.ext.zoom.setLevel(scaleName);
                    };

                    globalongoingData = ongoingData;

                    $scope.subProduct = subProduct;
                    $scope.ongoings = ongoingData.ongoings;
                    $scope.logs = ongoingData.logs;
                    $scope.counter = ongoingData.counter;
                }
            });

            modal.rendered.then(function (ongoingData) {
                //drawChart( document.getElementById('GanttChartProduction'), globalongoingData );

                drawChart2(globalongoingData);
            });
        };


        function drawChart2(ongoingData){

            var zoomConfig = {
                levels: [
                    {
                        name:"hour",
                        scale_height: 27,
                        min_column_width:80,
                        scales:[
                            {unit: "hour", step: 1, format: "%d %H:%m"}
                        ]
                    },
                    {
                        name:"day",
                        scale_height: 27,
                        min_column_width:80,
                        scales:[
                            {unit: "day", step: 1, format: "%d %M"}
                        ]
                    },
                    {
                        name:"week",
                        scale_height: 50,
                        min_column_width:50,
                        scales:[
                            {unit: "week", step: 1, format: function (date) {
                                var dateToStr = gantt.date.date_to_str("%d %M");
                                var endDate = gantt.date.add(date, -6, "day");
                                var weekNum = gantt.date.date_to_str("%W")(date);
                                return "#" + weekNum + ", " + dateToStr(date) + " - " + dateToStr(endDate);
                            }},
                            {unit: "day", step: 1, format: "%j %D"}
                        ]
                    },
                    {
                        name:"month",
                        scale_height: 50,
                        min_column_width:120,
                        scales:[
                            {unit: "month", format: "%F, %Y"},
                            {unit: "week", format: "Week #%W"}
                        ]
                    },
                    {
                        name:"quarter",
                        height: 50,
                        min_column_width:90,
                        scales:[
                            {unit: "month", step: 1, format: "%M"},
                            {
                                unit: "quarter", step: 1, format: function (date) {
                                    var dateToStr = gantt.date.date_to_str("%M");
                                    var endDate = gantt.date.add(gantt.date.add(date, 3, "month"), -1, "day");
                                    return dateToStr(date) + " - " + dateToStr(endDate);
                                }
                            }
                        ]
                    }
                ]
            };

            gantt.ext.zoom.init(zoomConfig);
	        gantt.ext.zoom.setLevel("hour");

            gantt.config.columns = [ 
                {
                    name: "overdue", label: "", width: 38, template: function (obj) {
                        if (obj.deadline) {
                            var deadline = gantt.date.parseDate(obj.deadline, "xml_date");
                            if (deadline && obj.end_date > deadline) {
                                return '<div class="overdue-indicator">!</div>';
                            }
                        }
                        return '<div></div>';
                    }
                },
                {name:"text", label:"Nazwa operacji", width:"*", tree:true }, 
                {name:"start_date", label:"Rozpoczecie", align: "center" }, 
                {name:"end_date", label:"Zakonczenie", align: "center" }, 
                {name:"duration", label:"Czas trwania [s]", align: "center" }, 
                {name:"planned_time", label:"Czas planowany [s]", align: "center" }, 
            ];

            //======================================
            //baseline config
            //======================================
            gantt.config.date_format = "%Y-%m-%d %H:%i:%s";
            gantt.config.bar_height = 16;
	        gantt.config.row_height = 40;
            gantt.addTaskLayer({
                renderer: {
                    render: function draw_planned(task) {
                        if (task.planned_start && task.planned_end) {
                            var sizes = gantt.getTaskPosition(task, task.planned_start, task.planned_end);
                            var el = document.createElement('div');
                            el.className = 'baseline';
                            el.style.left = sizes.left + 'px';
                            el.style.width = sizes.width + 'px';
                            el.style.top = sizes.top + gantt.config.bar_height + 13 + 'px';
                            return el;
                        }
                        return false;
                    },
                    // define getRectangle in order to hook layer with the smart rendering
                    getRectangle: function(task, view){
                        if (task.planned_start && task.planned_end) {
                            return gantt.getTaskPosition(task, task.planned_start, task.planned_end);
                        }
                        return null;
                    }
                }
            });
            gantt.locale.labels.section_baseline = "Planned";
            gantt.templates.task_class = function (start, end, task) {
                if (task.planned_end) {
                    var classes = ['has-baseline'];
                    if (end.getTime() > task.planned_end.getTime()) {
                        classes.push('overdue');
                    }
                    return classes.join(' ');
                }
            };
        
            gantt.templates.rightside_text = function (start, end, task) {
                if (task.planned_end) {
                    if (end.getTime() > task.planned_end.getTime()) {
                        var overdue = Math.ceil(Math.abs((end.getTime() - task.planned_end.getTime()) / (1000)/*/ (24 * 60 * 60 * 1000)*/));
                        var text = "<b>Opoznienie: " + overdue + " [s]</b>";
                        return text;
                    }
                }
            };        
        
            gantt.attachEvent("onTaskLoading", function (task) {
                task.planned_start = gantt.date.parseDate(task.planned_start, "xml_date");
                task.planned_end = gantt.date.parseDate(task.planned_end, "xml_date");
                return true;
            });
            //============= END ==================
            // END baseline config
            //============== END =================
            


            gantt.date.seconds_start = function(date){
                return date;
              };
              
              gantt.date.add_seconds = function(date, inc){
                
                var new_date = new Date(+date + 1000);
                return new_date;
              };              
              
              gantt.config.date_grid = "%Y-%m-%d %H:%i:%s";
              gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";

              gantt.config.min_duration = 1000; // (1 second)
              
              gantt.config.scale_unit = "hour";
              gantt.config.duration_unit = "seconds";
              gantt.config.date_scale = "%d %H:%i:%s";
              gantt.i18n.setLocale("pl");
              gantt.clearAll(); 

            gantt.init("gantt_here");

            _.each(ongoingData.ongoings, function(ongoing) {

                //var dateStart = Date(ongoing.startDate);
                //var endDate = Date(ongoing.endDate);
                var group = gantt.addTask({
                    id: ongoing.ID,
                    text: ongoing.operationName,
                    start_date: ongoing.startDate,
                    end_date: ongoing.endDate,
                    progress: 0.5,
                    planned_time: ongoing.estimatedTime,
                    planned_start: gantt.date.parseDate(ongoing.planned_start, "xml_date"),
                    planned_end: gantt.date.parseDate(ongoing.planned_end, "xml_date"),
                    deadline: ongoing.deadline,
                    render:"split"
                });
                _.each(ongoing.logs, function(log) {
                    gantt.addTask({
                        id: log.ID,
                        text: "Arkusz: "+log.sheetNumber+" Strona: "+log.processSideType,
                        start_date: log.startDate,
                        end_date: log.endDate,
                        parent: group
                    });
                });
                console.log("======ONGOING===========");
                console.log(ongoing);
                console.log("=================");
                /*if( ongoing.processes ) {
                    _.each(ongoing.processes, function(process) {

                        console.log("======process===========");
                        console.log(process);
                        console.log("=================");
                        gantt.addTask({
                            id: process.ID+1000,
                            text: process.name,
                            start_date: process.startDate,
                            end_date: process.endDate,
                            progress: 0.1,
                            planned_time: process.estimatedTime
                        }, group);
                    });
                }*/
            });
        }

        function drawChart(element, ongoingData) {

            console.log(element);

            var g = new JSGantt.GanttChart(element, 'hour');
            g.setHourColWidth(60);
            g.setDayColWidth(60);
            // ID, name, startDate, endDate, class, httpLink (not work),

            var ganttGroup;
            _.each(ongoingData.ongoings, function(ongoing) {
                g.AddTaskItem(new JSGantt.TaskItem(ongoing.ID, ongoing.operationName,ongoing.startDate, ongoing.endDate, 'gtaskred','', 0, 'Operator', 0,  1,0,1,'','','Some Notes text',g));
                if( ongoing.processes ) {
                    _.each(ongoing.processes, function(process) {
                        ganttGroup = process.ganttGroup !== undefined ? process.ganttGroup : 0;

                        g.AddTaskItem(new JSGantt.TaskItem(process.ID+1000, process.name,process.startDate, process.endDate, 'gtaskred','', 0, 'Operator', 0,  ganttGroup, ongoing.ID,1,'','','Some Notes text',g));
                    });
                }
            });
            g.Draw();

        }

    });