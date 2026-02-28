javascript
function write(value) {
  return encodeURIComponent(value)
    .replace(/%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g, decodeURIComponent);
}

window.cookieManager = {
  get: function (name) {
    if (typeof document === 'undefined' || arguments.length && !name) {
      return;
    }

    var cookies = document.cookie ? document.cookie.split('; ') : [];
    var jar = {};

    for (var i = 0; i < cookies.length; i++) {
      var parts = cookies[i].split('=');
      var value = parts.slice(1).join('=');

      try {
        var found = decodeURIComponent(parts[0]);
        jar[found] = value;
      } catch (e) {
        continue;
      }
    }

    return name ? jar[name] : jar;
  }
};
