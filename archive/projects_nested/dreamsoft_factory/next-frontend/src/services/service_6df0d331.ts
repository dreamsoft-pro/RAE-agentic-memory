import api from "@/lib/api";

class DatePickerComponent {
    private _get: (inst: any, settingName: string) => any;
    private _getDefaultDate: (inst: any) => Date | null;
    private _daylightSavingAdjust: (date: Date) => Date;
    private _generateMonthYearHeader: (inst: any, drawMonth: number, drawYear: number, minDate: Date, maxDate: Date, isMultipleMonths: boolean, monthNames: string[], shortMonthNames: string[]) => string;
    private _dayOverClass: string;
    private _unselectableClass: string;
    private _currentClass: string;

    constructor(
        getFunc: (inst: any, settingName: string) => any,
        getDefaultDateFunc: (inst: any) => Date | null,
        daylightSavingAdjustFunc: (date: Date) => Date,
        generateMonthYearHeaderFunc: (inst: any, drawMonth: number, drawYear: number, minDate: Date, maxDate: Date, isMultipleMonths: boolean, monthNames: string[], shortMonthNames: string[]) => string
    ) {
        this._get = getFunc;
        this._getDefaultDate = getDefaultDateFunc;
        this._daylightSavingAdjust = daylightSavingAdjustFunc;
        this._generateMonthYearHeader = generateMonthYearHeaderFunc;
        this._dayOverClass = "ui-datepicker-over";
        this._unselectableClass = "ui-unselectable";
        this._currentClass = "ui-datepicker-current-day";
    }

    private _getFirstDayOfMonth(year: number, month: number): number {
        return new Date(year, month, 1).getDay();
    }

    private _getDaysInMonth(year: number, month: number): number {
        return new Date(year, month + 1, 0).getDate();
    }

    public renderDatePickerHtml(inst: any, numMonths: [number, number], drawYear: number, drawMonth: number, minDate?: Date, maxDate?: Date, isRTL?: boolean, buttonPanel?: string): string {
        const showWeek = this._get(inst, "showWeek");
        let dayNames = this._get(inst, "dayNames") as string[];
        let dayNamesMin = this._get(inst, "dayNamesMin") as string[];
        let monthNames = this._get(inst, "monthNames") as string[];
        let monthNamesShort = this._get(inst, "monthNamesShort") as string[];
        const beforeShowDay = this._get(inst, "beforeShowDay");
        const showOtherMonths = this._get(inst, "showOtherMonths");
        const selectOtherMonths = this._get(inst, "selectOtherMonths");
        let defaultDate = this._getDefaultDate(inst);
        let html = "";
        let dow;
        
        for (let row = 0; row < numMonths[0]; row++) {
            let group = "";
            
            for (let col = 0; col < numMonths[1]; col++) {
                const selectedDate = this._daylightSavingAdjust(new Date(drawYear, drawMonth, inst.selectedDay));
                let cornerClass = " ui-corner-all";
                let calender = "";

                if (numMonths[1] > 1) {
                    switch (col) {
                        case 0: 
                            cornerClass = " ui-corner-" + (isRTL ? "right" : "left");
                            break;
                        case numMonths[1] - 1:
                            cornerClass = " ui-corner-" + (isRTL ? "left" : "right");
                            break;
                        default:
                            calender += "<div class='ui-datepicker-group-middle'>";
                    }
                }

                calender += this._generateMonthYearHeader(inst, drawMonth, drawYear, minDate, maxDate, row > 0 || col > 0, monthNames, monthNamesShort);

                let thead = (showWeek ? "<th class='ui-datepicker-week-col'>" + this._get(inst, "weekHeader") + "</th>" : "");
                
                for (dow = 0; dow < 7; dow++) {
                    const day = (dow + this._get(inst, "firstDay")) % 7;
                    thead += "<th scope='col'" + ((dow + this._get(inst, "firstDay") + 6) % 7 >= 5 ? " class='ui-datepicker-week-end'" : "") + ">" +
                        "<span title='" + dayNames[day] + "'>" + dayNamesMin[day] + "</span></th>";
                }

                const daysInMonth = this._getDaysInMonth(drawYear, drawMonth);
                
                if (drawYear === inst.selectedYear && drawMonth === inst.selectedMonth) {
                    inst.selectedDay = Math.min(inst.selectedDay, daysInMonth);
                }
                
                const leadDays = (this._getFirstDayOfMonth(drawYear, drawMonth) - this._get(inst, "firstDay") + 7) % 7;
                let printDate = this._daylightSavingAdjust(new Date(drawYear, drawMonth, 1 - leadDays));
                for (let dRow = 0; dRow < Math.ceil((leadDays + daysInMonth) / 7); dRow++) {
                    calender += "<tr>";
                    
                    const tbody = (!showWeek ? "" : "<td class='ui-datepicker-week-col'>" +
                        this._get(inst, "calculateWeek")(printDate) + "</td>");
                    
                    for (let dow = 0; dow < 7; dow++) {
                        const daySettings = beforeShowDay?.apply((inst.input ? inst.input[0] : null), [printDate]);
                        
                        const otherMonth = printDate.getMonth() !== drawMonth;
                        const unselectable = (otherMonth && !selectOtherMonths) || !daySettings[0] ||
                            (!minDate ? false : printDate < minDate) || (!maxDate ? false : printDate > maxDate);
                        
                        tbody += "<td class='" +
                            ((dow + this._get(inst, "firstDay") + 6) % 7 >= 5 ? " ui-datepicker-week-end" : "") +
                            (otherMonth ? " ui-datepicker-other-month" : "") +
                            ((printDate.getTime() === selectedDate.getTime() && drawMonth === inst.selectedMonth && inst._keyEvent) || 
                            (defaultDate?.getTime() === printDate.getTime() && defaultDate.getTime() === selectedDate.getTime()) ?
                                this._dayOverClass + " " + this._currentClass : "") +
                            (!unselectable ? " data-handler='selectDay' data-event='click' data-month='" + printDate.getMonth() + "' data-year='" + printDate.getFullYear() + "'" : "") +
                            (otherMonth && !showOtherMonths ? "" : daySettings[1] ?
                                " title='" + daySettings[2].replace(/'/g, "&#39;") + "'" : "") +
                            ((!otherMonth || showOtherMonths) && daySettings[2] ? " data-title='" + daySettings[2].replace(/'/g, "&#39;") + "'" : "") +
                            (unselectable ? "" : otherMonth ?
                                "<span class='ui-state-default'>" + printDate.getDate() + "</span>" :
                                `<a class='ui-state-default${printDate.getTime() === new Date().getTime() ? " ui-state-highlight" : ""}${printDate.getTime() === inst.selectedDay.getTime() && drawMonth === inst.selectedMonth ? " ui-state-active" : ""}${otherMonth ? " ui-priority-secondary" : ""}' href='#'>` +
                                printDate.getDate() + "</a>") +
                            (unselectable || otherMonth ? "&#xa0;" : "") + "</td>";

                        printDate.setDate(printDate.getDate() + 1);
                    }

                    calender += tbody + "</tr>";
                }
                
                drawMonth++;
                if (drawMonth > 11) {
                    drawMonth = 0;
                    drawYear++;
                }

                group += calender;
            }
            
            html += group;
        }
        
        return buttonPanel ? html + buttonPanel : html;
    }
}