const dateFormat = require("dateformat");

module.exports = function (data) {
    const date = dateFormat(new Date(), "yyyy-mm-dd H:M:s");
    log_stdout.write(util.format('%s %s', date, data) + '\n');
};
