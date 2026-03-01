javascript
!function() {
    var n, t;
    const e = {};

    (e[5132] = function(n) {
        return require('@/lib/api').use(require(5086));
    }).call(this);

    (e[4214] = function(n, t, e) {
        const r = require(5672);
        n.exports = function(n, t, e) {
            return n.mods.reduce(function(n, e) {
                if (Array.isArray(n) && t in e) {
                    n.push(e[t]);
                } else {
                    r(n, e[t]);
                }
                return n;
            }, e), e;
        };
    }).call(this);

    // More code conversion according to RAE-FIRST protocol rules

    function require(moduleId) {
        if (moduleId === 5132 || moduleId === 4214) {
            return e[moduleId];
        }
        throw new Error(`Module ${moduleId} not found`);
    }

    // Additional functions and logic as per the rules and context
}.call(this);
