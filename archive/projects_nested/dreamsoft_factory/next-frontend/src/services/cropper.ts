javascript
var jt = h.Cropper;

function It() {
    function i(t) {
        var e = 1 < arguments.length && void 0 !== arguments[1] ? arguments[1] : {};
        if (!(this instanceof i)) throw new TypeError("Cannot call a class as a function");
        this.element = t, this.options = rt({}, G, it(e) && e), this.cropped = !1, this.disabled = !1, this.pointers = {}, this.ready = !1, this.reloading = !1, this.replaced = !1, this.sized = !1, this.sizing = !1, this.init();
    }
    
    var t = i;
    
    return [
        { key: "noConflict", value: function() { return window.Cropper = jt, i } },
        { key: "setDefaults", value: function(t) { rt(G, it(t) && t) } }
    ].forEach(function(e) {
        Object.defineProperty(i.prototype, e.key, { value: e.value });
    }),
    
    [
        { key: "init", value: function() { var t = this.element, e = t.tagName.toLowerCase(); if (!t[c]) (t[c] = this), "img" === e ? (this.isImg = !0, (e = t.getAttribute("src") || "") && this.load(e)) : "canvas" === e && window.HTMLCanvasElement && this.clone() } },
        { key: "load", value: function(t) { var e, i = this.element, a = this.options, n = this.imageData; if (t) return this.url = t, a.rotatable || a.scalable || (a.checkOrientation = !1), a.checkOrientation && window.ArrayBuffer ? Q.test(t) ? K.test(t) ? this.read((e = t.replace(Yt, "")).replace(Ut, ""), atob(e)) : this.clone() : this.clone(); } },
        { key: "read", value: function(t) { var e = this.options, i = this.imageData, a = Xt(t), n = 0, o = 1, h = 1; 1 < a && (this.url = function(t, e) { for (var i = [], a = new Uint8Array(t); 0 < a.length;) i.push(zt.apply(null, ot(a.subarray(0, 8192)))), a = a.subarray(8192); return "data:".concat(e, ";base64,").concat(btoa(i.join(""))) }(t, q), n = (a = function(t) { switch (t) { case 2: o = -1; break; case 3: n = -180; break; case 4: h = -1; break; case 5: n = 90, h = -1; break; case 6: n = 90; break; case 7: n = 90, o = -1; break; case 8: n = -90 } return { rotate: n, scaleX: o, scaleY: h } }(a)).rotate, o = a.scaleX, h = a.scaleY), e.rotatable && (i.rotate = n), e.scalable && (i.scaleX = o, i.scaleY = h), this.clone(); } },
        { key: "clone", value: function() { var t = this.element, e = this.url, i = t.crossOrigin, a = e; this.options.checkCrossOrigin && Et(e) && (i = i || "anonymous", a = Wt(e)), this.crossOrigin = i, this.crossOriginUrl = a, document.createElement("img").src = a }, },
        { key: "start", value: function() { var t = this.image; t.onload = null, t.onerror = null, this.sizing = !0, (this.sized = !1), (this.sizingImage = document.createElement("img")).onload = e.bind(this), this.sizingImage.src = t.src },
        { key: "stop", value: function() { var t = this.image; t.onload = null, t.onerror = null, t.parentNode.removeChild(t), this.image = null } },
        { key: "build", value: function() { if (!this.ready) { var t = this.element, e = this.options, i = this.image, a = t.parentNode; (s = document.createElement("div")).innerHTML = '<div class="cropper-container" touch-action="none"><div class="cropper-wrap-box"><div class="cropper-canvas"></div></div><div class="cropper-drag-box"></div><div class="cropper-crop-box"><span class="cropper-view-box"></span><span class="cropper-dashed dashed-h"></span><span class="cropper-dashed dashed-v"></span><span class="cropper-center"></span><span class="cropper-face"></span><span class="cropper-line line-e" data-cropper-action="e"></span><span class="cropper-line line-n" data-cropper-action="n"></span><span class="cropper-line line-w" data-cropper-action="w"></span><span class="cropper-line line-s" data-cropper-action="s"></span><span class="cropper-point point-e" data-cropper-action="e"></span><span class="cropper-point point-n" data-cropper-action="n"></span><span class="cropper-point point-w" data-cropper-action="w"></span><span class="cropper-point point-s" data-cropper-action="s"></span><span class="cropper-point point-ne" data-cropper-action="ne"></span><span class="cropper-point point-nw" data-cropper-action="nw"></span><span class="cropper-point point-sw" data-cropper-action="sw"></span><span class="cropper-point point-se" data-cropper-action="se"></span></div></div>', o = (n = s.querySelector("." + c + "-container")).querySelector("." + c + "-canvas"), h = n.querySelector("." + c + "-drag-box"), r = n.querySelector("." + c + "-crop-box"); this.container = a, this.cropper = n, this.canvas = o, this.dragBox = h, this.cropBox = r, (s = this.viewBox = n.querySelector("." + c + "-view-box")).appendChild(i), mt(t, "img"), a.insertBefore(n, t.nextSibling); } },
        { key: "unbuild", value: function() { if (!this.ready) return; this.ready = !1, this.unbind(), this.resetPreview(), this.cropper.parentNode.removeChild(this.cropper), mt(this.element, "img"); }
    ].forEach(function(e) {
        Object.defineProperty(i.prototype, e.key, { value: e.value });
    }),
    
    i;
}
