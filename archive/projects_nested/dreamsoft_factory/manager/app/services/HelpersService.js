angular.module('digitalprint.services')
    .factory('HelpersService', function (Notification) {

        var HelpersService = {};
        HelpersService.formatTimePeriod = function (timePeriod, unit) {

            if (timePeriod) {
                if (unit) {
                    switch (unit) {
                        case 'minutes':
                            timePeriod *= 60;
                            break;
                        default:
                            break;
                    }
                }
                var d = Math.floor(timePeriod / 86400);
                timePeriod -= d * 86400;
                var h = Math.floor(timePeriod / 3600);
                timePeriod -= h * 3600;
                var m = Math.floor(timePeriod / 60);
                var formated = '';
                if (d > 0) {
                    formated = d;
                    formated += 'd';
                }
                if (h > 0) {
                    if (d > 0) {
                        formated += ' ';
                    }
                    formated += h;
                }
                if (m > 0) {
                    if (h > 0) {
                        formated += ':';
                    }
                    formated += m
                }
                if (formated) {
                    if (h > 0) {
                        formated += ' h';
                    } else if (m > 0) {
                        formated += ' m';
                    }
                }
                return formated;
            }
            return '';
        };

        HelpersService.showStandardMessages = function (response) {
            if (response.error) {
                Notification.error(response.error);
            }
            if (response.warnings) {
                _.each(response.warnings, function (warning) {
                    Notification.warning(warning);
                });
            }
        };

        HelpersService.showImposition = function (workspace, formatWidth, formatHeight, targetID) {
            formatWidth=parseInt(formatWidth)
            formatHeight=parseInt(formatHeight)
            var canvasSize = 600;
            var c = document.getElementById('canva-' + targetID);
            c.width=c.height=canvasSize ;
            c.style.display = c.style.display == 'none' ? 'block' : 'none';
            var drawing = c.style.display == 'block';
            if (drawing) {
                var scale = 1 / Math.max(workspace.width / canvasSize, workspace.height / canvasSize);
                var aResult = workspace.areaPerSheetForStandardResult;

                var ctx = c.getContext("2d", {alpha: true});
                ctx.translate(0.5, 0.5);//trick
                ctx.fillStyle = '#ffffff';
                ctx.strokeStyle = '#c8c8c8';
                ctx.lineWidth = 1;
                ctx.miterLimit = 'round';
                ctx.lineJoin = 'round';
                ctx.globalAlpha = 1;
                ctx.fillRect(0, 0, workspace.width * scale, workspace.height * scale);
                function putLabel(text,x,y,rotation, color){
                    x=parseInt(x);y=parseInt(y)
                    ctx.save();
                    ctx.fillStyle = color;
                    ctx.font = '12px Arial';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    if(rotation){
                        ctx.translate(x, y)
                        ctx.rotate(rotation);
                        ctx.fillText(text, 0,0);
                    }else{
                        ctx.fillText(text, x, y);
                    }
                    ctx.restore();
                }

                var x = workspace.width >= workspace.height ? aResult.longSide : aResult.shortSide;
                var y = workspace.width >= workspace.height ? aResult.shortSide : aResult.longSide;
                var hor = aResult.isHorizontalWidth ? formatWidth : formatHeight;
                var vert = aResult.isHorizontalWidth ? formatHeight : formatWidth;
                for (var i = 0; i < x; i++) {
                    for (var j = 0; j < y; j++) {
                        ctx.rect(hor * i * scale, vert * j * scale, hor * scale, vert * scale);
                        ctx.stroke();
                        if(aResult.isDoubledPages){
                            ctx.save()
                            ctx.beginPath();

                            if (aResult.isHorizontalWidth) {
                                ctx.moveTo(hor * i * scale + hor / 2 * scale, vert * j * scale);
                                ctx.lineTo(hor * i * scale + hor / 2 * scale, vert * j * scale + vert * scale);
                            } else {
                                ctx.moveTo(hor * i * scale, vert * j * scale + vert * scale / 2+0.5);
                                ctx.lineTo(hor * i * scale + hor * scale, vert * j * scale + vert * scale / 2+0.5);
                            }

                            ctx.setLineDash([8, 8]);
                            ctx.strokeStyle = '#216BC9';
                            ctx.stroke()
                            ctx.restore()
                             }
                        if(i===0 && j===0){
                            putLabel(hor, hor * scale / 2, vert * scale - 10,0,'#000000')
                            putLabel(vert, 10, vert * scale/2, Math.PI/2,'#000000')
                        }
                    }
                }
                putLabel(workspace.width, workspace.width * scale / 2, workspace.height * scale - 10,0,'#20A9DA')
                putLabel(workspace.height, 10, workspace.height * scale/2, Math.PI/2,'#20A9DA')
            }

        };

        HelpersService.formatNumber = function (theNumber, precision) {
            return theNumber.toFixed(precision)
        }
        return HelpersService;
    });
