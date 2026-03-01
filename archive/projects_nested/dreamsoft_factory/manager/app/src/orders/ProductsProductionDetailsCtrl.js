angular.module('digitalprint.app')
    .controller('orders.ProductsProductionDetailsCtrl', function ($scope, $state, $filter, $modal, $timeout, $window, ApiCollection,
        DpProductService, Notification, OperationService,
        ProductCardService, RealizationTimeService, OngoingService) {


        var globalongoingData = null;
        $scope.subProduct = null;

        init();
        
        function init(){
            if ($state.params.productID) {
                OngoingService.showForItem($state.params.productID).then(function (ongoingData) {
                    globalongoingData = ongoingData;
                    drawChart2(globalongoingData);   
                });

                DpProductService.baseCalcInfo($state.params.productID).then(function(data) {
                    console.log(data);
                    $scope.subProduct = data;
                }, function(data) {
                    Notification.error($filter('translate')('error'));
                })
            }
        }

        function drawChart2(ongoingData) {

            var zoomConfig = {
                levels: [
                    {
                        name: "minute",
                        scale_height: 50,
                        min_column_width: 80,
                        scales: [
                            { unit: "day", step: 1, format: "%d %M" },
                            { unit: "minute", step: 1, format: "%H:%m" }
                        ]
                    },
                    {
                        name: "hour",
                        scale_height: 27,
                        min_column_width: 80,
                        scales: [
                            { unit: "hour", step: 1, format: "%d %M %H:%m" }
                        ]
                    },
                    {
                        name: "day",
                        scale_height: 27,
                        min_column_width: 80,
                        scales: [
                            { unit: "day", step: 1, format: "%d %M" }
                        ]
                    },
                    {
                        name: "week",
                        scale_height: 50,
                        min_column_width: 50,
                        scales: [
                            {
                                unit: "week", step: 1, format: function (date) {
                                    var dateToStr = gantt.date.date_to_str("%d %M");
                                    var endDate = gantt.date.add(date, -6, "day");
                                    var weekNum = gantt.date.date_to_str("%W")(date);
                                    return "#" + weekNum + ", " + dateToStr(date) + " - " + dateToStr(endDate);
                                }
                            },
                            { unit: "day", step: 1, format: "%j %D" }
                        ]
                    },
                    {
                        name: "month",
                        scale_height: 50,
                        min_column_width: 120,
                        scales: [
                            { unit: "month", format: "%F, %Y" },
                            { unit: "week", format: "Week #%W" }
                        ]
                    },
                    {
                        name: "quarter",
                        height: 50,
                        min_column_width: 90,
                        scales: [
                            { unit: "month", step: 1, format: "%M" },
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
                { name: "text", label: "Nazwa operacji", width: 300, tree: true },
                //{ name: "start_date", label: "Rozpoczecie", align: "center" },
                //{ name: "end_date", label: "Zakonczenie", align: "center" },
                { name: "duration", label: "Czas trwania [s]", align: "center" },
                { name: "planned_time", label: "Czas planowany [s]", align: "center" },
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
                    getRectangle: function (task, view) {
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



            gantt.date.seconds_start = function (date) {
                return date;
            };

            gantt.date.add_seconds = function (date, inc) {

                var new_date = new Date(+date + 1000);
                return new_date;
            };

            gantt.config.date_grid = "%Y-%m-%d %H:%i:%s";
            gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";

            gantt.config.min_duration = 1000; // (1 second)

            //gantt.config.scale_unit = "hour";
            gantt.config.duration_unit = "seconds";
            //gantt.config.date_scale = "%d %H:%i:%s";

            gantt.plugins({ 
                tooltip: true 
            }); 

            gantt.templates.grid_row_class = function (start_date, end_date, item) {
                //if (item.state == 1) return "blue";
                if (item.state == 2) return "yellow";
                if (item.state == 3) return "green";
            };
            gantt.templates.task_row_class = function (start_date, end_date, item) {
                //if (item.state == 1) return "blue";
                if (item.state == 2) return "yellow";
                if (item.state == 3) return "green";
            };


            gantt.i18n.setLocale("pl");
            gantt.clearAll();



            gantt.init("gantt_here");

            _.each(ongoingData.ongoings, function (ongoing) {

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
                    state: ongoing.state
                });
                _.each(ongoing.logs, function (log) {
                    var sideName = "awers";
                    if(log.processSideType == 2){
                        sideName = "rewers";
                    }
                    var sheet = 1;
                    if(log.sheetNumber != null){
                        sheet = log.sheetNumber;
                    }
                    gantt.addTask({
                        id: log.ID,
                        text: "Arkusz: " + sheet + " " + sideName,
                        start_date: log.startDate,
                        end_date: log.endDate,
                        parent: ongoing.ID
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
    });