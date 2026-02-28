angular.module('digitalprint.app')
    .controller('orders.ScheduleGanttCtrl', function ($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService,
        OngoingService, ProductCardService, ApiCollection, ScheduleService, $timeout,
        $window, $q) {

        $scope.showRows = 10;
        $scope.productsConfig = {
            count: 'schedule/count',
            params: {
                accept: 1,
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.dpProducts.items = data;
                $timeout(function () {
                    drawChart(data);
                }, 500);
            }
        };

        $scope.dpProducts = new ApiCollection('schedule', $scope.productsConfig);
        $scope.dpProducts.get();

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.dpProducts.get();
            }, 1000);
        };

        function init() {
            //$scope.dpProducts.clearCache();

        }

        init();

        function drawChart(products) {

            //gantt.ext.zoom.init(zoomConfig);
            //gantt.ext.zoom.setLevel("hour");

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
                { name: "text", label: "Nazwa", width: 300, tree: true },
                //{ name: "start_date", label: "Rozpoczecie", align: "center" },
                //{ name: "end_date", label: "Zakonczenie", align: "center" },
                { name: "duration", label: "Czas trwania [s]", align: "center" },
                //{ name: "planned_time", label: "Czas planowany [s]", align: "center" },
            ];

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
                if (item.state == true) return "green";
            };
            gantt.templates.task_row_class = function (start_date, end_date, item) {
                //if (item.state == 1) return "blue";
                if (item.state == 2) return "yellow";
                if (item.state == 3) return "green";
                if (item.state == true) return "green";
            };

            //the same nesting level
            gantt.config.order_branch = true;
            //gantt.config.order_branch_free = true;
            gantt.attachEvent("onRowDragEnd", function (id, target) {
                //console.log("Dragged ID:" + id);
                var result = [];
                var ongoingsOrder = [];
                gantt.eachTask(function (task) {
                    //if(stop) return;
                    if (task.nodeLevel == 1) {
                        //console.log("Product: " + task.id);
                        result.push(task.id);
                    } else if (task.nodeLevel == 2) {
                        //console.log("Ongoing: " + (task.id - 10000));
                        ongoingsOrder.push(task.id - 10000);
                    }
                    //stop = true; // stop processing further records
                });

                ScheduleService.sort(result).then(function (data) {
                    $scope.sortChange = false;
                    OngoingService.sort(ongoingsOrder).then(function (dataOngoingSort) {
                        Notification.success($filter('translate')('success'));
                    }, function (dataOngoingSort) {
                        Notification.error($filter('translate')('error'));
                        $scope.sortCancel();
                    });
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                    $scope.sortCancel();
                });
            });

            //baseline config
            gantt.config.bar_height = 16;
            gantt.config.row_height = 40;
            // adding baseline display
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
                        var overdue = Math.ceil(Math.abs((end.getTime() - task.planned_end.getTime()) / (24 * 60 * 60 * 1000)));
                        var text = "<b>Spoznienie: " + overdue + " dni</b>";
                        return text;
                    }
                }
            };


            gantt.attachEvent("onTaskLoading", function (task) {
                task.planned_start = gantt.date.parseDate(task.planned_start, "xml_date");
                task.planned_end = gantt.date.parseDate(task.planned_end, "xml_date");
                return true;
            });

            gantt.i18n.setLocale("pl");
            gantt.clearAll();



            gantt.init("gantt_here");

            //console.log("ITEMS");
            //console.log(products);

            _.each(products, function (product) {
                if (product.ID && product.products[0].ongoings && product.products[0].ongoings.startDate != null && product.products[0].ongoings.endDate != null) {
                    //console.log("ITEM");
                    //console.log(product);
                    var datePlannedStart = gantt.date.parseDate(product.products[0].ongoings.plannedStart, "xml_date");
                    var datePlannedEnd = gantt.date.parseDate(product.products[0].ongoings.plannedEnd, "xml_date");
                    //gantt.date.parseDate(product.products[0].ongoings.startDate, "xml_date")
                    var group = gantt.addTask({
                        id: product.ID,
                        text: product.products[0].typeName + "(ID: " + product.ID + ")",
                        start_date: product.products[0].ongoings.startDate,
                        end_date: product.products[0].ongoings.endDate,
                        //progress: 0.5,
                        //planned_time: ongoing.estimatedTime,
                        //planned_start: gantt.date.parseDate(ongoing.planned_start, "xml_date"),
                        //planned_end: gantt.date.parseDate(ongoing.planned_end, "xml_date"),
                        planned_start: datePlannedStart,
                        planned_end: datePlannedEnd,
                        //deadline: ongoing.deadline,
                        state: product.products[0].ongoings.endProduction,
                        nodeLevel: 1
                    });
                    _.each(product.products, function (product) {
                        //console.log(product);
                        _.each(product.ongoings.list, function (ongoing) {
                            //console.log(ongoing);
                            if (ongoing.startLog && ongoing.endLog) {
                                gantt.addTask({
                                    id: ongoing.ID + 10000,
                                    text: ongoing.operationName,
                                    start_date: ongoing.startLog.date,
                                    end_date: ongoing.endLog.date,
                                    planned_start: gantt.date.parseDate(ongoing.plannedStart, "xml_date"),
                                    planned_end: gantt.date.parseDate(ongoing.plannedEnd, "xml_date"),
                                    parent: group,
                                    state: ongoing.state,
                                    nodeLevel: 2
                                });
                            } else {
                                gantt.addTask({
                                    id: ongoing.ID + 10000,
                                    text: ongoing.operationName,
                                    parent: group,
                                    state: ongoing.state,
                                    nodeLevel: 2
                                });
                            }
                        });
                    });
                } else {
                    Notification.error("Produkt ID: " + product.ID + " nie posiada daty startu/konca");
                }
            });


        }



    });