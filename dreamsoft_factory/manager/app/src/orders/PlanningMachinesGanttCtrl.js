angular.module('digitalprint.app')
    .controller('orders.PlanningMachinesGanttCtrl', function ($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService, DepartmentService,
        OngoingService, ProductCardService, ApiCollection, ScheduleService, $timeout,
        $window, $q) {

        var scopeGlobal = $scope;
        var allowAlert = true;
        $scope.chartHeight = 20;

        $scope.showRows = 50;
        $scope.planningConfig = {
            count: 'planning/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.planningData.items = data;
                console.log(data);
                $timeout(function () {
                    drawChart($scope, data);
                }, 500);
            }
        };

        $scope.changesMade = true;
        $scope.changedMachines = [];
        $scope.changedOrderOnMachines = [];

        $scope.planningData = new ApiCollection('planning', $scope.planningConfig);
        $scope.planningData.get();

        $scope.searchOrderID = "";

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.planningData.get();
            }, 1000);
        };

        var updateChangeOrderID;
        $scope.changeOrderID = function () {
            $timeout.cancel(updateChangeOrderID);
            updateChangeOrderID = $timeout(function () {
                highlightOrderID($scope.searchOrderID);
            }, 2000);
        };

        $scope.saveChanges = function () {
            console.log($scope.changedMachines);
            var dataArray = [];
            var dataArrayOrder = [];
            gantt.eachTask(function (task) {
                var deviceID = task.parentOfDevice;
                if ($scope.changedMachines.includes(deviceID)) {
                    var ongoingData = {};
                    ongoingData.ongoingID = task.ongoingID;
                    ongoingData.plannedStart = displayMySQLFormatDate(task.start_date);
                    ongoingData.estimatedTime = Math.round(((task.end_date.getTime() - task.start_date.getTime()) / 1000));
                    dataArray.push(ongoingData);
                }

                if (task.nodeLevel == 4 && $scope.changedOrderOnMachines.includes(deviceID)) {
                    dataArrayOrder.push(task.ongoingID);
                }
            });
            console.log('dataArray '+dataArray);
            console.log('dataArrayOrder '+dataArrayOrder);

            //saving logic
            if (dataArray.length > 0) {
                ScheduleService.updateOngoings(dataArray).then(function (data) {
                    console.log(data);
                    if (data.response == true) {
                        Notification.success($filter('translate')('updated_ongoings'));
                        $scope.changesMade = true;
                        $scope.changedMachines = [];
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                });
            }

            if (dataArrayOrder.length > 0) {
                OngoingService.sortOrderOnDevice(dataArrayOrder).then(function (dataOngoingSort) {
                    if (dataOngoingSort.response == true) {
                        Notification.success($filter('translate')('updated_order_of_ongoings'));
                        $scope.changesMade = true;
                        $scope.changedOrderOnMachines = [];
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                }, function (dataOngoingSort) {
                    Notification.error($filter('translate')('error'));
                });
            }
        };

        $scope.cancelChanges = function () {

        };

        $scope.toggleGanttFullscreen = function () {
            gantt.ext.fullscreen.toggle();
        };

        function highlightOrderID(orderID) {
            console.log(orderID);
            var orderFound = false;
            gantt.eachTask(function (task) {
                if (task && task.orderID && task.productID && task.productName && task.clientName && task.nodeLevel == 4) {
                    task.isHighlighted = false;
                    if (task.orderID.toString().includes(orderID) || task.productID.toString().includes(orderID) || task.productName.toString().includes(orderID) || task.clientName.toString().includes(orderID)) {
                        orderFound = true;
                        task.isHighlighted = true;
                    }
                }
            });

            if (orderFound == true) {
                Notification.success($filter('translate')('result_found_and_highlighted_red'));
                gantt.refreshData();
            } else {
                Notification.error($filter('translate')('result_not_found'));
            }
        }


        function init() {
            //$scope.planningData.clearCache();
        }

        init();

        function drawChart($scope, chartData) {

            gantt.clearAll();
            gantt.resetLayout();

            var zoomConfig = {
                levels: [
                    {
                        name: "minute",
                        scale_height: 50,
                        min_column_width: 80,
                        scales: [
                            { unit: "minute", step: 1, format: "%d %M" },
                            { unit: "minute", step: 1, format: "%H:%i" }
                        ]
                    },
                    {
                        name: "hour",
                        scale_height: 27,
                        min_column_width: 80,
                        scales: [
                            { unit: "hour", step: 1, format: "%d %M" },
                            { unit: "hour", step: 1, format: "%H:%i" }
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
            gantt.config.round_dnd_dates = false;
            gantt.config.time_step = 1;
            gantt.config.min_duration = 60*1000;
            gantt.config.drag_links = false;

            gantt.config.columns = [
                {
                    name: "overdue", label: "", width: 38, template: function (obj) {
                        if (obj.isTaskLate) {
                                return '<div class="overdue-indicator">!</div>';
                        }
                        return '<div></div>';
                    }
                },
                { name: "text", label: "Nazwa", width: 300, tree: true },
                //{ name: "start_date", label: "Rozpoczecie", align: "center" },
                //{ name: "end_date", label: "Zakonczenie", align: "center" },
                { name: "duration", label: "Czas trwania [m]", width: 100, align: "left", template: function (obj) {
                    if (obj.duration == 1) {
                        return '<div>0</div>';
                    }
                    return '<div>' + formatTime(obj.duration * 60) + '</div>';
                }},
                //{ name: "planned_time", label: "Czas planowany [s]", align: "center" },
            ];

            gantt.config.date_grid = "%Y-%m-%d %H:%i:%s";
            gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";

            // gantt.config.min_duration = 1000; // (1 second)

            //gantt.config.scale_unit = "hour";
            gantt.config.duration_unit = "minute";
            //gantt.config.date_scale = "%d %H:%i:%s";

            gantt.config.drag_progress = false;

            gantt.plugins({
                tooltip: true,
                marker: true,
                fullscreen: true
            });

            var format = gantt.date.date_to_str("%Y-%m-%d %H:%i");
            gantt.templates.tooltip_text = function (start, end, event) {
                if(event.nodeLevel == 4){
                    return "<b>Operacja:</b> " + event.text + 
                    "<br/><b>Start:</b> " +  format(start) + 
                    "<br/><b>Koniec:</b> " + format(end) + 
                    "<br/><b>Postep:</b> " + Math.round(event.progress*100) + "%" + 
                    "<br/><b>OrderID:</b> " + event.orderID +  
                    "<br/><b>Produkt:</b> " + event.productName +  
                    "<br/><b>Klient:</b> " + event.clientName;
                }else if (event.nodeLevel == 1){
                    if(event.duration == 1){
                        return "<b>Dzial:</b> " + event.departmentName;
                    }else{
                        return "<b>Dzial:</b> " + event.departmentName + 
                        "<br/><b>Start:</b> " +  format(start) + 
                        "<br/><b>Koniec:</b> " + format(end);
                    }
                }else if (event.nodeLevel == 2){
                    if(event.duration == 1){
                        return "<b>Maszyna:</b> " + event.deviceName;
                    }else{
                        return "<b>Maszyna:</b> " + event.deviceName + 
                        "<br/><b>Start:</b> " +  format(start) + 
                        "<br/><b>Koniec:</b> " + format(end);
                    }
                }else{
                    return "";
                }
            };

            gantt.templates.grid_row_class = function (start_date, end_date, item) {
                //if (item.state == 1) return "blue";
                //if (item.state == 2) return "yellow";
                //if (item.state == 3) return "green";
                //if (item.state == true) return "green";
                if (item.notEstimated == 1) return "notEstimatedRow";
                if (item.isTaskMoved == true) return "taskMoved";
                if (item.isHighlighted == true) return "isHighlighted";
            };
            gantt.templates.task_row_class = function (start_date, end_date, item) {
                //if (item.state == 1) return "blue";
                //if (item.state == 2) return "yellow";
                //if (item.state == 3) return "green";
                //if (item.state == true) return "green";
                if (item.notEstimated == 1) return "notEstimatedRow";
                if (item.isTaskMoved == true) return "taskMoved";
                if (item.isHighlighted == true) return "isHighlighted";
            };

            //baseline config
            gantt.config.bar_height = 30;
            gantt.config.row_height = 40;

            gantt.templates.task_class = function (start, end, task) {
                if (task.planned_end) {
                    var classes = ['has-baseline'];
                    if (end.getTime() > task.planned_end.getTime()) {
                        classes.push('overdue');
                    }
                    return classes.join(' ');
                }
            };

            //weekends
            gantt.templates.scale_cell_class = function (date) {
                if (date.getDay() == 0 || date.getDay() == 6) {
                    return "weekend";
                }
            };
            gantt.templates.timeline_cell_class = function (item, date) {
                if (date.getDay() == 0 || date.getDay() == 6) {
                    return "weekend"
                }
            };
            //notEstimated tasks
            gantt.templates.task_class = function (start, end, task) {
                if (task.notEstimated == 1) {
                    return "notEstimated"
                }
                if (task.isHighlighted == true) {
                    return "isHighlightedTask"
                }
                if (task.nodeLevel == 1) {
                    return "departmentColor"
                } else if (task.nodeLevel == 2) {
                    return "deviceColor"
                } else if (task.nodeLevel == 3) {
                    return "operationColor"
                }
            };

            gantt.templates.rightside_text = function (start, end, task) {
                return "";
            };
            

            //=================================================================================
            //daging tasks row
            gantt.config.order_branch = true;
           


            gantt.config.show_unscheduled = true;

            gantt.i18n.setLocale("pl");
            gantt.init("gantt_here");

            var startWorkingDay = "";
            var endWorkingDay = "";

            _.each(chartData, function (department) {
                startWorkingDay = department.startDay;
                endWorkingDay = department.finishDay;
                // var departmentGroup = gantt.addTask({
                //     id: department.ID,
                //     text: department.name + "(ID: " + department.ID + ")",
                //     nodeLevel: 1,
                //     departmentID: department.ID,
                //     departmentName: department.name
                // });
                if (department.devices.length > 0) {
                    _.each(department.devices, function (device) {
                        var operatorsIcon = "<i class='fa fa-user'></i>";
                        var processIcon = "<i class='fa fa-cog'></i>";
                        if (device.multiOperator == 1) {
                            operatorsIcon = "<i class='fa fa-users'></i>";
                        }
                        if (device.multiProcess == 1) {
                            processIcon = "<i class='fa fa-cogs'></i>";
                        }
                        var isMultiProcessActive = false;
                        if(device.multiProcess == 1){
                            isMultiProcessActive = true;
                        }
                        var deviceGroup = gantt.addTask({
                            id: device.ID + 1000,
                            text: device.name + "(ID: " + device.ID + ") " + operatorsIcon + " " + processIcon,
                            nodeLevel: 2,
                            deviceID: device.ID,
                            deviceName: device.name,
                            isMultiProcessActive: isMultiProcessActive,
                            type: "project",
                            render:"split"
                        });
                        var timeStart = new Date(department.generationDate);
                        var lastNullOperationEndTime = new Date();
                        var lastTask = null;
                        _.each(device.ongoings, function (ongoing) {
                            if (ongoing.plannedStart && ongoing.plannedStart != null){
                                timeStart = new Date(ongoing.plannedStart);
                            }else{
                                if(timeStart.getTime() < new Date().getTime()){
                                    timeStart = new Date(lastNullOperationEndTime.getTime()+1000);
                                }
                            }                                
                            //========================================================================================================
                            var plannedTime = ongoing.estimatedTime;
                            var plannedTimeForZeroTasks = 1200;
                            var estimationStatus = 0;
                            var taskNote = "";
                            if (plannedTime <= 0 || plannedTime == null) {
                                plannedTime = plannedTimeForZeroTasks;
                                estimationStatus = 1;
                                taskNote = "Czas szacowany"
                            }
                            var endTime = new Date(timeStart.getTime() + plannedTime * 1000);
                            //check iftask will fit before closing
                            var isTaskMoved = false;
                            var closingHour = department.finishDay.split(':')[0];
                            var closingMinute = department.finishDay.split(':')[1];
                            var checkTime = new Date(timeStart.getTime());
                            checkTime.setHours(closingHour);
                            checkTime.setMinutes(closingMinute);
                            checkTime.setSeconds(0);
                            //console.log("===============");
                            //console.log(timeStart);
                            //console.log(endTime);
                            //console.log(checkTime);
                            var statusIcon = "";
                            if (ongoing.state == 0) {
                                statusIcon = "<i class='fa fa-circle'></i>";
                            } else if (ongoing.state == 1) {
                                statusIcon = "<i class='fa fa-play-circle'></i>";
                            } else if (ongoing.state == 2) {
                                statusIcon = "<i class='fa fa-pause-circle'></i>";
                            }
                            //task progress
                            var taskProgress = 0;
                            if(ongoing.sumTime && ongoing.sumTime != null && ongoing.sumTime > 0){
                                var taskTime = (endTime.getTime() - timeStart.getTime())/1000;
                                taskProgress = ongoing.sumTime / taskTime;
                                taskProgress = Math.round(taskProgress * 100) / 100;
                                endTime.setTime(endTime.getTime() - (ongoing.sumTime*1000));
                                //substract sumTime from estimatedTime
                            }
                            //isTaskLate
                            var isTaskLate = new Date() > endTime ? true : false;
                            if(isTaskLate) 
                                taskNote = taskNote+ " | <b style=\"color: red\">Operacja spozniona</b>";
                            //processSideType
                            var processSideType = 1;
                            var processSideTypeIcon = "<i class='fa fa-square'></i>";
                            if(ongoing.processSideType == 2){
                                processSideType = 2;
                                processSideTypeIcon = "<i class='fa fa-clone'></i>";
                            }
                            //client name
                            var clientName = "";
                            if(ongoing.clientAddress[0] && ongoing.clientAddress[0].name && ongoing.clientAddress[0].lastname){
                                clientName = ongoing.clientAddress[0].name+" "+ongoing.clientAddress[0].lastname;
                            }
                            if(ongoing.clientAddress[0] && ongoing.clientAddress[0].companyName){
                                clientName = ongoing.clientAddress[0].companyName+" "+clientName;
                            }
                            
                            if (endTime.getTime() > checkTime.getTime()) {
                                taskNote = taskNote + " | Operacja rozdzielona (ID: " + ongoing.ID + ")";
                                var timeLeft = endTime.getTime() - checkTime.getTime();
                                //task from now to finish workday
                                //timeStart = timeStart;
                                endTime = new Date(checkTime.getTime());
                                gantt.addTask({
                                    id: ongoing.ID + 1000000,
                                    ongoingID: ongoing.ID,
                                    text: ongoing.productName+"(JOB ID: " + ongoing.ID + ") " + statusIcon + " " + processSideTypeIcon,
                                    start_date: displayFormatDate(timeStart),
                                    end_date: displayFormatDate(endTime),
                                    state: ongoing.state,
                                    nodeLevel: 4,
                                    parent: deviceGroup,
                                    notEstimated: estimationStatus,
                                    note: taskNote,
                                    isTaskMoved: true,
                                    orderID: ongoing.orderID,
                                    isHighlighted: false,
                                    parentOfDevice: device.ID,
                                    progress: taskProgress,
                                    processSideType: processSideType,
                                    productName: ongoing.productName,
                                    clientName: clientName,
                                    productID: ongoing.productID
                                });

                                timeStart.setDate(timeStart.getDate() + 1);
                                timeStart.setHours(department.startDay.split(':')[0]);
                                timeStart.setMinutes(department.startDay.split(':')[1]);
                                timeStart.setSeconds(0);
                                endTime = new Date(timeStart.getTime() + timeLeft);
                                isTaskMoved = true;
                                lastTask = ongoing.ID + 1000000;
                            }
                            var displayDeviceID = false;
                            if (!isTaskMoved) displayDeviceID = device.ID;
                            var ongoingGroup = gantt.addTask({
                                id: ongoing.ID + 100000,
                                ongoingID: ongoing.ID,
                                text: ongoing.productName+"(JOB ID: " + ongoing.ID + ") " + statusIcon + " " + processSideTypeIcon,
                                start_date: displayFormatDate(timeStart),
                                end_date: displayFormatDate(endTime),
                                //planned_time: ongoing.estimatedTime,
                                //planned_start: gantt.date.parseDate(ongoing.plannedStart, "xml_date"),
                                //planned_end: gantt.date.parseDate(ongoing.plannedEnd, "xml_date"),
                                //deadline: ongoing.deadline,
                                state: ongoing.state,
                                nodeLevel: 4,
                                parent: deviceGroup,
                                notEstimated: estimationStatus,
                                note: taskNote,
                                isTaskMoved: isTaskMoved,
                                orderID: ongoing.orderID,
                                isHighlighted: false,
                                parentOfDevice: displayDeviceID,
                                progress: taskProgress,
                                isTaskLate: isTaskLate,
                                processSideType: ongoing.processSideType,
                                productName: ongoing.productName,
                                clientName: clientName,
                                productID: ongoing.productID
                            });
                            $scope.chartHeight += 40;
                            if (isTaskMoved && lastTask !== null) {
                                console.log("add link" + lastTask + "" + (ongoing.ID + 100000) + "");
                                var linkId = gantt.addLink({
                                    id: lastTask,
                                    source: lastTask,
                                    target: ongoing.ID + 100000,
                                    type: gantt.config.links.finish_to_start
                                });
                            }
                            lastTask = ongoing.ID + 100000;
                            timeStart = new Date(endTime.getTime());
                            if (!ongoing.plannedStart && ongoing.plannedStart == null){
                                lastNullOperationEndTime = new Date(endTime.getTime());
                            }   
                            //========================================================================================================                     
                        });
                        var taskCheck = gantt.getTask(deviceGroup);
                        if(taskCheck.duration == 1){
                            taskCheck.start_date = new Date();
                            taskCheck.end_date = new Date(taskCheck.start_date.getTime());
                            gantt.updateTask(taskCheck.id);
                            // gantt.deleteTask(taskCheck.id);
                        }
                    });
                }
            });


            //=================================================================================
            //add todays marker 
            var dateToStr = gantt.date.date_to_str(gantt.config.task_date);
            var markerId = gantt.addMarker({
                start_date: new Date(),
                css: "today", 
                text: "Teraz", 
                title: dateToStr( new Date()) 
            });
            //=================================================================================
            //=================================================================================

        }

        function displayFormatDate(date) {
            return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
        }

        function displayMySQLFormatDate(date) {
            return date.getFullYear() + "-" + ('0' + (date.getMonth() + 1)).slice(-2) + "-" + ('0' + date.getDate()).slice(-2) + " " + ('0' + date.getHours()).slice(-2) + ":" + ('0' + date.getMinutes()).slice(-2) + ":" + ('0' + date.getSeconds()).slice(-2);
        }

        function formatTime(timeInSeconds) {
            var sign = "";
            if(timeInSeconds < 0){
                sign = "-";
                timeInSeconds = timeInSeconds*(-1);
            }
            var minutes = pad(Math.floor(timeInSeconds / 60) % 60);
            var hours = pad(Math.floor(timeInSeconds / 3600));

            return sign+""+hours + ':' + minutes;
        }

        function pad(n) {
            return (n < 10) ? ("0" + n) : n;
        }



    });