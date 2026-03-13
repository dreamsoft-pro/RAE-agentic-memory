angular.module('digitalprint.app')
    .controller('orders.PlanningGanttCtrl', function ($state, $rootScope, $filter, $scope, Notification, DeviceService,
        OperationService, $modal, OrderService, OperatorService, PauseService, DepartmentService,
        OngoingService, ProductCardService, ApiCollection, ScheduleService, $timeout,
        $window, $q) {

        var scopeGlobal = $scope;
        var allowAlert = true;

        $scope.defaultZoom = 'hour';

        $scope.taskData = [];

        $scope.showRows = 50;
        $scope.chartHeight = 0;
        $scope.planningConfig = {
            count: 'planning/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.planningData.items = data;
                console.log(data);
                $timeout(function () {
                    $scope.taskData = data;
                    drawChart($scope, $scope.taskData, [], null);
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
            var dataArrayProducts = [];
            var dataArrayOngoings = [];
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
                    dataArrayOngoings.push(task.ongoingID);
                    dataArrayProducts.push(task.productID);
                }
            });
            console.log('dataArray ' + dataArray);
            console.log('dataArrayOngoings ' + dataArrayOngoings);

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

            if (dataArrayOngoings.length > 0) {
                ScheduleService.sort(dataArrayProducts).then(function (data) {
                    $scope.sortChange = false;
                    OngoingService.sort(dataArrayOngoings).then(function (dataOngoingSort) {
                        if (dataOngoingSort.response == true) {
                            Notification.success($filter('translate')('updated_order_of_ongoings'));
                            $scope.changesMade = true;
                            $scope.changedOrderOnMachines = [];
                        } else {
                            Notification.error($filter('translate')('error'));
                        }
                    }, function (dataOngoingSort) {
                        Notification.error($filter('translate')('error'));
                        $scope.sortCancel();
                    });
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                    $scope.sortCancel();
                });
            }
        };

        $scope.cancelChanges = function () {

        };

        $scope.toggleGanttFullscreen = function () {
            gantt.ext.fullscreen.toggle();
        };

        $scope.autoScheduleTasks = function () {
            var selectedID = gantt.getSelectedId();
            if (selectedID != null) {
                var taskNode = gantt.getTask(selectedID);
                if (taskNode.nodeLevel == 4) {
                    var deviceTaskID = taskNode.parent;
                    var parentTaskNode = gantt.getTask(deviceTaskID);
                    var deviceDepID = parentTaskNode.parent;
                    var sizes = gantt.getTaskPosition(taskNode);
                    var newLineTimeStart = taskNode.start_date;
                    gantt.confirm({
                        text: $filter('translate')('are_you_sure') + " " + $filter('translate')('ongoing_id') + ": " + taskNode.ongoingID,
                        ok: $filter('translate')('Yes'),
                        cancel: $filter('translate')('No'),
                        callback: function (result) {
                            if (result === true) {
                                var ongoingIDs = [];
                                var newTaskData = $scope.taskData;
                                var deviceID = taskNode.parentOfDevice;
                                console.log("Device: " + deviceID);
                                gantt.eachTask(function (task) {
                                    if (task.parentOfDevice == deviceID) {
                                        var ongoingID = task.ongoingID;
                                        ongoingIDs.push(ongoingID);
                                    }
                                });
                                console.log(ongoingIDs);
                                newTaskData.forEach(function (department) {
                                    if (department.devices.length > 0) {
                                        department.devices.forEach(function (device) {
                                            if (device.ongoings.length > 0) {
                                                device.ongoings.forEach(function (ongoing) {
                                                    var ongoingID = ongoing.ID;
                                                    if (ongoingIDs.includes(ongoingID)) {
                                                        console.log(ongoing);
                                                        ongoing.plannedStart = null;
                                                        ongoing.plannedEnd = null;
                                                    }
                                                });
                                            }
                                        });
                                    }
                                });
                                console.log("newdata");
                                console.log(newTaskData);
                                drawChart($scope, newTaskData, [deviceTaskID, deviceDepID], newLineTimeStart);
                                setTimeout(function () {
                                    gantt.scrollTo(sizes.left - 200, sizes.top);
                                    gantt.selectTask(selectedID);
                                }, 2000);
                            }
                        }
                    });
                } else {
                    gantt.message({ type: "warning", text: $filter('translate')('invalid_task_selected') });
                }
            }
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

        function drawChart($scope, chartData, openProjects, newLineTimeStart) {
            gantt.clearAll();
            gantt.resetLayout();

            var defaultScale = chartData[0].defaultGanttScale;
            var holidays = chartData[0].holidays;

            ganttConfig(defaultScale, holidays);
            ganttMoveTaskBehavior();
            ganttDragTaskBehavior();

            gantt.init("gantt_here");

            var chartMinDate = null;
            var chartMaxDate = null;

            _.each(chartData, function (department) {
                var departmentGroup = gantt.addTask({
                    id: department.ID,
                    text: department.name + "(ID: " + department.ID + ")",
                    nodeLevel: 1,
                    departmentID: department.ID,
                    departmentName: department.name
                });
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
                        if (device.multiProcess == 1) {
                            isMultiProcessActive = true;
                        }
                        var deviceGroup = gantt.addTask({
                            id: device.ID + 1000,
                            text: device.name + "(ID: " + device.ID + ") " + operatorsIcon + " " + processIcon,
                            nodeLevel: 2,
                            parent: departmentGroup,
                            deviceID: device.ID,
                            deviceName: device.name,
                            isMultiProcessActive: isMultiProcessActive,
                            deviceShifts: device.shifts
                            //unscheduled: true
                        });
                        var timeStart = new Date(department.generationDate);
                        var lastNullOperationEndTime = new Date();
                        var lastTask = null;
                        _.each(device.ongoings, function (ongoing) {
                            //===============================================================================================================
                            //===============================================================================================================
                            //===============================================================================================================
                            //===============================================================================================================
                            if (ongoing.plannedStart && ongoing.plannedStart != null) {
                                timeStart = new Date(ongoing.plannedStart);
                            } else {
                                if (timeStart.getTime() < new Date().getTime()) {
                                    timeStart = new Date(lastNullOperationEndTime.getTime() + 1000);
                                }
                            }
                            var lastTask = null;
                            var plannedTime = ongoing.estimatedTime;
                            var plannedTimeForZeroTasks = 1200;
                            if (device.defaultOperationTime !== null)
                                plannedTimeForZeroTasks = device.defaultOperationTime * 60;
                            var estimationStatus = 0;
                            var taskNote = "";
                            if (plannedTime <= 0 || plannedTime == null) {
                                plannedTime = plannedTimeForZeroTasks;
                                estimationStatus = 1;
                                taskNote = "Czas szacowany"
                            }

                            var timeEnd = new Date(timeStart.getTime() + plannedTime * 1000);

                            //check iftask will fit before closing
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
                            if (ongoing.sumTime && ongoing.sumTime != null && ongoing.sumTime > 0) {
                                var taskTime = (timeEnd.getTime() - timeStart.getTime()) / 1000;
                                taskProgress = ongoing.sumTime / taskTime;
                                taskProgress = Math.round(taskProgress * 100) / 100;
                                timeEnd.setTime(timeEnd.getTime() - (ongoing.sumTime * 1000));
                                //substract sumTime from estimatedTime
                            }
                            //isTaskLate
                            var isTaskLate = new Date() > timeEnd ? true : false;
                            if (isTaskLate)
                                taskNote = taskNote + " | <b style=\"color: red\">Operacja spozniona</b>";
                            //processSideType
                            var processSideType = 1;
                            var processSideTypeIcon = "<i class='fa fa-square'></i>";
                            if (ongoing.processSideType == 2) {
                                processSideType = 2;
                                processSideTypeIcon = "<i class='fa fa-clone'></i>";
                            }
                            //client name
                            var clientName = "";
                            if (ongoing.clientAddress[0] && ongoing.clientAddress[0].name && ongoing.clientAddress[0].lastname) {
                                clientName = ongoing.clientAddress[0].name + " " + ongoing.clientAddress[0].lastname;
                            }
                            if (ongoing.clientAddress[0] && ongoing.clientAddress[0].companyName) {
                                clientName = ongoing.clientAddress[0].companyName + " " + clientName;
                            }
                            //for calculation 
                            //timestart

                            var isTaskMoved = false;
                            if (device.shifts.length > 0 && isDateInWorkingHours(timeStart, device, department.holidays) === false) {
                                var nextShiftID = getNextStartShiftID(timeStart, device.shifts);
                                // start operation on next day fisrt shift
                                if (nextShiftID == -1) {
                                    nextShiftID = 0;
                                    timeStart.setHours(timeStart.getHours() + 24);
                                    var shiftHourStart = device.shifts[nextShiftID].start.split(":")[0];
                                    var shiftMinuteStart = device.shifts[nextShiftID].start.split(":")[1];
                                    timeStart.setHours(shiftHourStart, shiftMinuteStart, 0);
                                    while (isDateInWorkingHours(timeStart, device, department.holidays) === false) {
                                        timeStart.setHours(timeStart.getHours() + 24);
                                    }
                                } else {
                                    var shiftHourStart = device.shifts[nextShiftID].start.split(":")[0];
                                    var shiftMinuteStart = device.shifts[nextShiftID].start.split(":")[1];
                                    timeStart.setHours(shiftHourStart, shiftMinuteStart, 0);
                                }
                                timeEnd.setTime(timeStart.getTime() + plannedTime * 1000);
                            }

                            // check if task ends before end of current shift
                            if (device.shifts.length > 0) {
                                var currentShiftID = isDateInWorkingHours(timeStart, device, department.holidays);
                                var shiftEndTime = new Date(timeStart.getTime());
                                shiftEndTime.setHours(device.shifts[currentShiftID].stop.split(":")[0], device.shifts[currentShiftID].stop.split(":")[1], device.shifts[currentShiftID].stop.split(":")[2]);
                                var tmpStop = new Date(shiftEndTime.getTime());
                                var plannedTimeLeft = timeEnd - tmpStop;
                                var lastTaskID = 0;

                                if (timeEnd > shiftEndTime) {
                                    // WHILE LOOP
                                    while (timeEnd > shiftEndTime) {
                                        tmpStop = new Date(shiftEndTime.getTime());
                                        plannedTimeLeft = timeEnd - tmpStop;
                                        // split task
                                        var taskID = gantt.addTask({
                                            id: ongoing.ID + 100000000 + Math.floor(Math.random() * 10000),
                                            ongoingID: ongoing.ID,
                                            text: ongoing.productName + "(JOB ID: " + ongoing.ID + ") " + statusIcon + " " + processSideTypeIcon,
                                            start_date: displayFormatDate(timeStart),
                                            end_date: displayFormatDate(tmpStop),
                                            state: ongoing.state,
                                            nodeLevel: 4,
                                            deviceWorksInSaturday: device.worksInSaturday,
                                            deviceWorksInSunday: device.worksInSunday,
                                            parent: deviceGroup,
                                            notEstimated: estimationStatus,
                                            note: taskNote,
                                            isTaskMoved: true,
                                            orderID: ongoing.orderID,
                                            isHighlighted: false,
                                            parentOfDevice: device.ID,
                                            progress: taskProgress,
                                            isTaskLate: isTaskLate,
                                            processSideType: ongoing.processSideType,
                                            productName: ongoing.productName,
                                            clientName: clientName,
                                            productID: ongoing.productID
                                        });

                                        var wasServiceObject = checkForServiceDuringOperation(timeStart, tmpStop, device.services);
                                        if (wasServiceObject.wasService === true) {
                                            tmpStop.setTime(tmpStop.getTime() + (1000 * 60 * wasServiceObject.timeOfService));
                                        }

                                        if (lastTaskID == 0) {
                                            lastTaskID = taskID;
                                        } else {
                                            var linkId = gantt.addLink({
                                                id: lastTaskID,
                                                source: lastTaskID,
                                                target: taskID,
                                                type: gantt.config.links.finish_to_start
                                            });
                                            lastTaskID = taskID;
                                        }

                                        timeStart.setTime(tmpStop.getTime() + (1000 * 60));
                                        timeEnd.setTime(timeStart.getTime() + plannedTimeLeft);
                                        // check if task will manage to finish before end of shift
                                        currentShiftID = isDateInWorkingHours(timeStart, device, department.holidays);
                                        if (currentShiftID === false) {
                                            currentShiftID = getNextStartShiftID(timeStart, device.shifts);
                                            // start operation on next day fisrt shift
                                            if (currentShiftID == -1) {
                                                currentShiftID = 0;
                                                timeStart.setHours(timeStart.getHours() + 24);
                                                var shiftHourStart = device.shifts[currentShiftID].start.split(":")[0];
                                                var shiftMinuteStart = device.shifts[currentShiftID].start.split(":")[1];
                                                timeStart.setHours(shiftHourStart, shiftMinuteStart, 0);
                                                while (isDateInWorkingHours(timeStart, device, department.holidays) === false) {
                                                    timeStart.setHours(timeStart.getHours() + 24);
                                                }
                                                if (wasServiceObject.wasService === true) {
                                                    timeStart.setTime(timeStart.getTime() + (1000 * 60 * wasServiceObject.timeOfService));
                                                }
                                                timeEnd.setTime(timeStart.getTime() + plannedTimeLeft);
                                            } else {
                                                var shiftHourStart = device.shifts[currentShiftID].start.split(":")[0];
                                                var shiftMinuteStart = device.shifts[currentShiftID].start.split(":")[1];
                                                timeStart.setHours(shiftHourStart, shiftMinuteStart, 0);
                                                timeEnd.setTime(timeStart.getTime() + plannedTimeLeft);
                                            }
                                        }
                                        shiftEndTime = new Date(timeStart.getTime());
                                        shiftEndTime.setHours(device.shifts[currentShiftID].stop.split(":")[0], device.shifts[currentShiftID].stop.split(":")[1], device.shifts[currentShiftID].stop.split(":")[2]);
                                    }
                                    // END OF WHILE LOOP
                                    var taskID = gantt.addTask({
                                        id: ongoing.ID + 100000,
                                        ongoingID: ongoing.ID,
                                        text: ongoing.productName + "(JOB ID: " + ongoing.ID + ") " + statusIcon + " " + processSideTypeIcon,
                                        start_date: displayFormatDate(timeStart),
                                        end_date: displayFormatDate(timeEnd),
                                        state: ongoing.state,
                                        nodeLevel: 4,
                                        deviceWorksInSaturday: device.worksInSaturday,
                                        deviceWorksInSunday: device.worksInSunday,
                                        parent: deviceGroup,
                                        notEstimated: estimationStatus,
                                        note: taskNote,
                                        isTaskMoved: true,
                                        orderID: ongoing.orderID,
                                        isHighlighted: false,
                                        parentOfDevice: device.ID,
                                        progress: taskProgress,
                                        isTaskLate: isTaskLate,
                                        processSideType: ongoing.processSideType,
                                        productName: ongoing.productName,
                                        clientName: clientName,
                                        productID: ongoing.productID
                                    });
                                    var wasServiceObject = checkForServiceDuringOperation(timeStart, timeEnd, device.services);
                                    if (wasServiceObject.wasService === true) {
                                        timeEnd.setTime(timeEnd.getTime() + (1000 * 60 * wasServiceObject.timeOfService));
                                    }
                                    var linkId = gantt.addLink({
                                        id: lastTaskID,
                                        source: lastTaskID,
                                        target: taskID,
                                        type: gantt.config.links.finish_to_start
                                    });
                                } else {
                                    var ongoingGroup = gantt.addTask({
                                        id: ongoing.ID + 100000,
                                        ongoingID: ongoing.ID,
                                        text: ongoing.productName + "(JOB ID: " + ongoing.ID + ") " + statusIcon + " " + processSideTypeIcon,
                                        start_date: displayFormatDate(timeStart),
                                        end_date: displayFormatDate(timeEnd),
                                        state: ongoing.state,
                                        nodeLevel: 4,
                                        deviceWorksInSaturday: device.worksInSaturday,
                                        deviceWorksInSunday: device.worksInSunday,
                                        parent: deviceGroup,
                                        notEstimated: estimationStatus,
                                        note: taskNote,
                                        isTaskMoved: isTaskMoved,
                                        orderID: ongoing.orderID,
                                        isHighlighted: false,
                                        parentOfDevice: device.ID,
                                        progress: taskProgress,
                                        isTaskLate: isTaskLate,
                                        processSideType: ongoing.processSideType,
                                        productName: ongoing.productName,
                                        clientName: clientName,
                                        productID: ongoing.productID
                                    });
                                    var wasServiceObject = checkForServiceDuringOperation(timeStart, timeEnd, device.services);
                                    if (wasServiceObject.wasService === true) {
                                        timeEnd.setTime(timeEnd.getTime() + (1000 * 60 * wasServiceObject.timeOfService));
                                    }
                                }
                            } else {
                                var ongoingGroup = gantt.addTask({
                                    id: ongoing.ID + 100000,
                                    ongoingID: ongoing.ID,
                                    text: ongoing.productName + "(JOB ID: " + ongoing.ID + ") " + statusIcon + " " + processSideTypeIcon,
                                    start_date: displayFormatDate(timeStart),
                                    end_date: displayFormatDate(timeEnd),
                                    state: ongoing.state,
                                    nodeLevel: 4,
                                    deviceWorksInSaturday: device.worksInSaturday,
                                    deviceWorksInSunday: device.worksInSunday,
                                    parent: deviceGroup,
                                    notEstimated: estimationStatus,
                                    note: taskNote,
                                    isTaskMoved: isTaskMoved,
                                    orderID: ongoing.orderID,
                                    isHighlighted: false,
                                    parentOfDevice: device.ID,
                                    progress: taskProgress,
                                    isTaskLate: isTaskLate,
                                    processSideType: ongoing.processSideType,
                                    productName: ongoing.productName,
                                    clientName: clientName,
                                    productID: ongoing.productID
                                });
                                var wasServiceObject = checkForServiceDuringOperation(timeStart, timeEnd, device.services);
                                if (wasServiceObject.wasService === true) {
                                    timeEnd.setTime(timeEnd.getTime() + (1000 * 60 * wasServiceObject.timeOfService));
                                }
                            }

                            //chart max/min time calc
                            if (chartMinDate == null || (chartMinDate != null && chartMinDate > timeStart.getTime())) chartMinDate = timeStart.getTime();
                            if (chartMaxDate == null || (chartMaxDate != null && chartMaxDate < timeEnd.getTime())) chartMaxDate = timeEnd.getTime();

                            //$scope.chartHeight += 50;
                            if (isTaskMoved && lastTask !== null) {
                                var linkId = gantt.addLink({
                                    id: lastTask,
                                    source: lastTask,
                                    target: ongoing.ID + 100000,
                                    type: gantt.config.links.finish_to_start
                                });
                            }

                            timeStart = new Date(timeEnd.getTime());
                            if (!ongoing.plannedStart && ongoing.plannedStart == null) {
                                lastNullOperationEndTime = new Date(timeEnd.getTime());
                            }
                            //========================================================================================================  
                            //===============================================================================================================
                            //===============================================================================================================
                            //===============================================================================================================
                            //===============================================================================================================                   
                        });
                    });
                }
            });

            //=================================================================================
            //mark services times 
            _.each(chartData, function (department) {
                _.each(department.devices, function (device) {
                    if (device.services.length > 0) {
                        var servicesGroup = gantt.addTask({
                            id: device.ID + 10000000,
                            text: "Serwis Maszyny",
                            nodeLevel: 5,
                            render: "split",
                            parent: device.ID + 1000
                        });
                        _.each(device.services, function (service) {
                            var dayOfWeek = null;
                            if (service.cycleID == 2) {
                                if (service.dayOfWeek == 7) {
                                    dayOfWeek = 0;
                                } else {
                                    dayOfWeek = service.dayOfWeek;
                                }
                            }
                            var date = new Date(chartMinDate);
                            date.setHours(service.hourOfBeginning, 0, 0);
                            while (date.getTime() < chartMaxDate) {
                                var startTime = new Date(date.getTime());
                                var endTime = new Date(startTime.getTime() + (service.timeDuration * 60 * 1000));
                                if ((service.cycleID == 4 && (service.dayOfMonth != date.getDate() || service.month != (date.getMonth() + 1))) ||
                                    (service.cycleID == 3 && service.dayOfMonth != date.getDate()) ||
                                    (service.cycleID == 2 && dayOfWeek != date.getDay())) {

                                } else {
                                    gantt.addTask({
                                        id: new Date().getTime(),
                                        text: service.name,
                                        nodeLevel: 5,
                                        start_date: startTime,
                                        end_date: endTime,
                                        parent: servicesGroup
                                    });
                                }

                                date.setHours(date.getHours() + 24);
                            }
                        });
                    }
                });
            });
            //=================================================================================
            //=================================================================================

            //=================================================================================
            //add todays marker 
            var dateToStr = gantt.date.date_to_str(gantt.config.task_date);
            var markerId = gantt.addMarker({
                start_date: new Date(),
                css: "today",
                text: "Teraz",
                title: dateToStr(new Date())
            });
            //=================================================================================
            //=================================================================================
            setTimeout(function () {
                if (openProjects.length > 0) {
                    openProjects.forEach(function (tab) {
                        gantt.open(tab);
                        console.log("open: " + tab);
                        console.log(gantt.getTask(tab));
                    });
                }
            }, 500);

        }

        function ganttConfig(defaultScale, holidays) {
            // gant main config
            var format = gantt.date.date_to_str("%Y-%m-%d %H:%i");
            gantt.config.round_dnd_dates = false;
            gantt.config.time_step = 1;
            gantt.config.drag_links = false;
            gantt.config.date_grid = "%Y-%m-%d %H:%i:%s";
            gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";
            gantt.config.duration_unit = "minute";
            gantt.config.min_duration = 60 * 1000;
            gantt.config.drag_progress = false;
            gantt.config.bar_height = 30;
            gantt.config.row_height = 40;
            gantt.config.order_branch = true;
            gantt.config.show_unscheduled = true;
            gantt.i18n.setLocale("pl");
            //=================================================================================
            //=================================================================================
            // plugins
            gantt.plugins({
                tooltip: true,
                marker: true,
                fullscreen: true
            });
            //=================================================================================
            //=================================================================================
            // plugin tooltip config
            gantt.templates.tooltip_text = function (start, end, event) {
                if (event.nodeLevel == 5) {
                    return "<b>Serwis:</b> " + event.text +
                        "<br/><b>Start:</b> " + format(start) +
                        "<br/><b>Koniec:</b> " + format(end);
                } else if (event.nodeLevel == 4) {
                    return "<b>Operacja:</b> " + event.text +
                        "<br/><b>Start:</b> " + format(start) +
                        "<br/><b>Koniec:</b> " + format(end) +
                        "<br/><b>Postep:</b> " + Math.round(event.progress * 100) + "%" +
                        "<br/><b>OrderID:</b> " + event.orderID +
                        "<br/><b>Produkt:</b> " + event.productName +
                        "<br/><b>Klient:</b> " + event.clientName;
                } else if (event.nodeLevel == 1) {
                    if (event.duration == 1) {
                        return "<b>Dzial:</b> " + event.departmentName;
                    } else {
                        return "<b>Dzial:</b> " + event.departmentName +
                            "<br/><b>Start:</b> " + format(start) +
                            "<br/><b>Koniec:</b> " + format(end);
                    }
                } else if (event.nodeLevel == 2) {
                    if (event.duration == 1) {
                        return "<b>Maszyna:</b> " + event.deviceName;
                    } else {
                        return "<b>Maszyna:</b> " + event.deviceName +
                            "<br/><b>Start:</b> " + format(start) +
                            "<br/><b>Koniec:</b> " + format(end);
                    }
                } else {
                    return "";
                }
            };
            //=================================================================================
            //=================================================================================
            // zoom config
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
            if (defaultScale && defaultScale != "") {
                gantt.ext.zoom.setLevel(defaultScale);
                $scope.defaultZoom = defaultScale;
                var zoomLevel = gantt.ext.zoom.getCurrentLevel();
                changeStyleForZoomLevel(zoomLevel);
            } else {
                gantt.ext.zoom.setLevel("hour");
                $scope.defaultZoom = "hour";
            }
            gantt.ext.zoom.attachEvent("onAfterZoom", function(level, config){ 
                var zoomLevel = gantt.ext.zoom.getCurrentLevel();
                changeStyleForZoomLevel(zoomLevel);
            });

            function changeStyleForZoomLevel(zoomLevel){
                console.log(zoomLevel);
                var color = 'white !important';
                if(zoomLevel === 1){
                   color = '#f9dfdf';
                }
                var elements = document.getElementsByClassName("gantt_task_cell");
                Array.prototype.forEach.call(elements, function(element) {
                    element.style.background = color+"";
                });
            }
            //=================================================================================
            //=================================================================================
            // left column config
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
                {
                    name: "duration", label: "Czas trwania [m]", width: 100, align: "left", template: function (obj) {
                        if (obj.duration == 1) {
                            return '<div>0</div>';
                        }
                        return '<div>' + formatTime(obj.duration * 60) + '</div>';
                    }
                },
                //{ name: "planned_time", label: "Czas planowany [s]", align: "center" },
            ];
            //=================================================================================
            //=================================================================================
            // styles config
            gantt.templates.grid_row_class = function (start_date, end_date, item) {
                if (item.nodeLevel == 1) return "departmentRow";
                if (item.nodeLevel == 2) return "deviceRow";
                if (item.notEstimated == 1) return "notEstimatedRow";
                if (item.isTaskMoved == true) return "taskMoved";
                if (item.isHighlighted == true) return "isHighlighted";
            };
            gantt.templates.task_row_class = function (start_date, end_date, item) {
                if (item.nodeLevel == 1) return "departmentRow";
                if (item.nodeLevel == 2) return "deviceRow";
                if (item.notEstimated == 1) return "notEstimatedRow";
                if (item.isTaskMoved == true) return "taskMoved";
                if (item.isHighlighted == true) return "isHighlighted";
            };
            gantt.templates.task_class = function (start, end, task) {
                // var classes = ['has-baseline'];
                var classes = [];
                if (task.planned_end) {
                    if (end.getTime() > task.planned_end.getTime()) {
                        classes.push('overdue');
                    }
                }
                if (task.notEstimated == 1) {
                    classes.push("notEstimated");
                }
                if (task.nodeLevel == 1) {
                    classes.push("departmentColor");
                } else if (task.nodeLevel == 2) {
                    classes.push("deviceColor");
                }

                return classes.join(' ');
            };
            gantt.templates.rightside_text = function (start, end, task) {
                var returnText = "";
                if (task.planned_end) {
                    if (end.getTime() > task.planned_end.getTime()) {
                        var overdue = Math.ceil(Math.abs((end.getTime() - task.planned_end.getTime()) / (24 * 60 * 60 * 1000)));
                        var text = "<b>Spoznienie: " + overdue + " dni</b>";
                        returnText = returnText + " " + text;
                    }
                }
                if (task.note && task.note.length > 0) {
                    returnText = returnText + " " + task.note;
                }

                return returnText;
            };
            gantt.templates.timeline_cell_class = function (item, date) {
                var css = "";
                var isInHolidays = false;
                if (item.nodeLevel == 4 || item.nodeLevel == 5) {

                    holidays.forEach(function (holiday) {
                        if (date.getDate() == holiday.day && (date.getMonth() + 1) == holiday.month) {
                            isInHolidays = true;
                        }
                    });
                    if (item.deviceWorksInSaturday != 1 && date.getDay() == 6) {
                        isInHolidays = true;
                    }
                    if (item.deviceWorksInSunday != 1 && date.getDay() == 0) {
                        isInHolidays = true;
                    }
                    if (isInHolidays == false) {
                        var deviceNode = gantt.getTask(item.parent);
                        if (deviceNode.deviceShifts) {
                            deviceNode.deviceShifts.forEach(function (shift) {
                                var shiftHourStart = shift.start.split(":")[0];
                                var shiftMinuteStart = shift.start.split(":")[1];
                                var shiftHourStop = shift.stop.split(":")[0];
                                var shiftMinuteStop = shift.stop.split(":")[1];
                                if (date.getHours() >= shiftHourStart && date.getMinutes() >= shiftMinuteStart && date.getHours() <= (parseInt(shiftHourStop) - 1) && date.getMinutes() <= shiftMinuteStop) {
                                    css = "work_hour";
                                }
                            });
                        }
                    }
                }
                return css;
            };
            //=================================================================================
            //=================================================================================
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

        }

        function ganttMoveTaskBehavior() {
            gantt.attachEvent("onTaskDrag", function (id, mode, task, original) {
                var deviceID = gantt.getTask(task.parent).deviceID;
                var deviceNode = gantt.getTask(task.parent);
                if ($scope.changedMachines.indexOf(deviceID) === -1) {
                    $scope.changedMachines.push(deviceID);
                }
                $scope.changesMade = true;
                if (deviceNode.isMultiProcessActive == false) {
                    //move tasks
                    if ((task.start_date == original.start_date && task.end_date != original.end_date) || (task.start_date != original.start_date && task.end_date != original.end_date)) {
                        var startMoving = false;
                        var prevEndTime = new Date(task.end_date.getTime());
                        gantt.eachTask(function (singleTask) {
                            if ((singleTask.parentOfDevice == deviceID) && startMoving == true) {
                                if (singleTask.start_date.getTime() < prevEndTime.getTime()) {
                                    var duration = singleTask.end_date.getTime() - singleTask.start_date.getTime();
                                    singleTask.start_date = new Date(prevEndTime.getTime() + 1000);
                                    singleTask.end_date = new Date(singleTask.start_date.getTime() + duration);
                                    gantt.updateTask(singleTask.id);
                                }
                                prevEndTime = new Date(singleTask.end_date.getTime());
                            }
                            if (singleTask.id == task.id) {
                                startMoving = true;
                            }
                        });
                    }
                    if ((task.start_date != original.start_date && task.end_date == original.end_date) || (task.start_date != original.start_date && task.end_date != original.end_date)) {
                        var startMoving = true;
                        var tasksArray = [];
                        gantt.eachTask(function (singleTask) {
                            if (singleTask.id == task.id) {
                                startMoving = false;
                            }
                            if ((singleTask.parentOfDevice == deviceID) && startMoving == true) {
                                tasksArray.push(singleTask.id);
                            }
                        });

                        tasksArray.reverse();
                        var prevStartTime = new Date(task.start_date.getTime());
                        _.each(tasksArray, function (singleTaskID) {
                            var currentTask = gantt.getTask(singleTaskID);
                            if (currentTask.end_date.getTime() > prevStartTime.getTime()) {
                                var duration = currentTask.end_date.getTime() - currentTask.start_date.getTime();
                                currentTask.start_date = new Date(prevStartTime.getTime() - duration - 1000);
                                currentTask.end_date = new Date(currentTask.start_date.getTime() + duration);
                                gantt.updateTask(currentTask.id);
                            }
                            prevStartTime = new Date(currentTask.start_date.getTime());
                        });
                    }
                } else {
                    //checking conflicts
                    var tasks = gantt.getTaskByTime(task.start_date, task.end_date);
                    var conflictArray = [];
                    _.each(tasks, function (singleTask) {
                        var parentOfDevice = singleTask.parentOfDevice;
                        if ((parentOfDevice == deviceID) && singleTask.id != task.id) {
                            conflictArray.push(singleTask);
                        }
                    });
                    if (conflictArray.length > 0 && allowAlert) {
                        // var box = gantt.alert({
                        //     title: "Uwaga",
                        //     type: "alert-error",
                        //     text: "Wystapil konflikt operacji"
                        // });
                        // allowAlert = false;
                        // $timeout(function () {
                        //     allowAlert = true;
                        // }, 3000);
                    }
                }

            });
        }

        function ganttDragTaskBehavior() {
            gantt.attachEvent("onRowDragEnd", function (id, target) {
                var deviceID = gantt.getTask(id).parentOfDevice;
                if ($scope.changedOrderOnMachines.indexOf(deviceID) === -1) {
                    $scope.changedOrderOnMachines.push(deviceID);
                }
                $scope.changesMade = true;
            });
        }

        function displayFormatDate(date) {
            return date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
        }

        function displayMySQLFormatDate(date) {
            return date.getFullYear() + "-" + ('0' + (date.getMonth() + 1)).slice(-2) + "-" + ('0' + date.getDate()).slice(-2) + " " + ('0' + date.getHours()).slice(-2) + ":" + ('0' + date.getMinutes()).slice(-2) + ":" + ('0' + date.getSeconds()).slice(-2);
        }

        function formatTime(timeInSeconds) {
            var sign = "";
            if (timeInSeconds < 0) {
                sign = "-";
                timeInSeconds = timeInSeconds * (-1);
            }
            var minutes = pad(Math.floor(timeInSeconds / 60) % 60);
            var hours = pad(Math.floor(timeInSeconds / 3600));

            return sign + "" + hours + ':' + minutes;
        }

        function pad(n) {
            return (n < 10) ? ("0" + n) : n;
        }

        function isDateInWorkingHours(date, item, holidays) {
            var isInWorkingHours = false;
            var isInHolidays = false;
            var shiftID = 0;
            var shifts = item.shifts;

            holidays.forEach(function (holiday) {
                if (date.getDate() == holiday.day && (date.getMonth() + 1) == holiday.month) {
                    isInHolidays = true;
                }
            });
            if (item.worksInSaturday != 1 && date.getDay() == 6) {
                isInHolidays = true;
            }
            if (item.worksInSunday != 1 && date.getDay() == 0) {
                isInHolidays = true;
            }
            if (isInHolidays == false) {
                shifts.forEach(function (shift) {
                    var shiftHourStart = shift.start.split(":")[0];
                    var shiftMinuteStart = shift.start.split(":")[1];
                    var shiftHourStop = shift.stop.split(":")[0];
                    var shiftMinuteStop = shift.stop.split(":")[1];
                    var dateShiftStart = new Date(date.getTime()).setHours(shiftHourStart, shiftMinuteStart, 0);
                    var dateShiftEnd = new Date(date.getTime()).setHours(shiftHourStop, shiftMinuteStop, 0);
                    if (date >= dateShiftStart && date <= dateShiftEnd) {
                        isInWorkingHours = shiftID;
                    }
                    shiftID++;
                });
            }
            return isInWorkingHours;
        }

        function getNextStartShiftID(date, shifts) {
            var shiftID = -1;
            var lowestDifference = null;
            var currentID = 0;
            shifts.forEach(function (shift) {
                var shiftHourStart = shift.start.split(":")[0];
                var shiftMinuteStart = shift.start.split(":")[1];
                var dateShiftStart = new Date(date.getTime());
                dateShiftStart.setHours(shiftHourStart, shiftMinuteStart, 0);
                var difference = dateShiftStart - date;
                if (lowestDifference == null && date < dateShiftStart) lowestDifference = difference + 1;
                if (difference < lowestDifference && date < dateShiftStart) {
                    shiftID = currentID;
                    lowestDifference = difference;
                }


                currentID++;
            });

            return shiftID;
        }


        function getClosestStopShiftID(date, shifts) {
            var shiftID = -1;
            var lowestDifference = null;
            var currentID = 0;
            shifts.forEach(function (shift) {
                var shiftHourStop = shift.stop.split(":")[0];
                var shiftMinuteStop = shift.stop.split(":")[1];
                var dateShiftStop = new Date(date.getTime()).setHours(shiftHourStop, shiftMinuteStop, 0);
                var difference = date - dateShiftStop;
                if (difference > 0 && lowestDifference == null)
                    lowestDifference = difference + 1;
                if (difference > 0 && difference < lowestDifference && date > dateShiftStop) {
                    shiftID = currentID;
                    lowestDifference = difference;
                }


                currentID++;
            });

            return shiftID;
        }

        function checkForServiceDuringOperation(timeStart, timeEnd, services) {
            var wasService = false;
            var timeOfService = 0;
            services.forEach(function (service) {
                var dayOfWeek = null;
                if (service.cycleID == 2) {
                    if (service.dayOfWeek == 7) {
                        dayOfWeek = 0;
                    } else {
                        dayOfWeek = service.dayOfWeek;
                    }
                }
                if (service.cycleID == 1 && service.hourOfBeginning >= timeStart.getHours() && service.hourOfBeginning <= timeEnd.getHours()) {
                    wasService = true;
                    timeOfService += service.timeDuration;
                }
                if (service.cycleID == 2 && dayOfWeek === timeStart.getDay() && service.hourOfBeginning >= timeStart.getHours() && service.hourOfBeginning <= timeEnd.getHours()) {
                    wasService = true;
                    timeOfService += service.timeDuration;
                }
                if (service.cycleID == 3 && service.dayOfMonth === timeStart.getDate() && service.hourOfBeginning >= timeStart.getHours() && service.hourOfBeginning <= timeEnd.getHours()) {
                    wasService = true;
                    timeOfService += service.timeDuration;
                }
                if (service.cycleID == 4 && service.month === (timeStart.getMonth() + 1) && service.dayOfMonth === timeStart.getDate() && service.hourOfBeginning >= timeStart.getHours() && service.hourOfBeginning <= timeEnd.getHours()) {
                    wasService = true;
                    timeOfService += service.timeDuration;
                }

            });

            return { wasService: wasService, timeOfService: timeOfService };
        }

    });