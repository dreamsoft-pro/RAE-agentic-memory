/* global angular */
'use strict';

angular.module('dpClient.helpers')
.directive('ngCookieInformation', function () {
      return {
          restrict: 'A',
          controller: function ($scope) {

          function assign (target) {
                    for (var i = 1; i < arguments.length; i++) {
                      var source = arguments[i];
                      for (var key in source) {
                        target[key] = source[key];
                      }
                    }
                    return target;
            }

            var converter = {
              read: function (value) {
                if (value[0] === '"') {
                  value = value.slice(1, -1);
                }
                return value.replace(/(%[\dA-F]{2})+/gi, decodeURIComponent);
              },

              write: function (value) {
                return encodeURIComponent(value).replace(
                  /%(2[346BF]|3[AC-F]|40|5[BDE]|60|7[BCD])/g,
                  decodeURIComponent
                );
              }
            };

          window.cookieMenager = {
                get: function (name) {
                  if (typeof document === 'undefined' || (arguments.length && !name)) {
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

                      if (name === found) {
                        break;
                      }
                    } catch (e) {}
                  }

                  return name ? jar[name] : jar;
                },

              set: function (name, value, attributes) {
                if (typeof document === 'undefined') {
                  return;
                }

                var now = new Date();
                var time = now.getTime();
                var expireTime = time + 1000*36000;
                attributes = assign({
                  Domain: window.location.hostname,
                  Path: '/',
                  SameSite: 'Lax',
                  Secure: window.location.protocol === 'https',
                  expires: now.setTime(expireTime)
                }, attributes);

                window.test = now;

                if (typeof attributes.expires === 'number') {
                  attributes.expires = new Date(Date.now() + attributes.expires * 864e5);
                }

                if (attributes.expires) {
                  attributes.expires = attributes.expires.toUTCString();
                }

                name = encodeURIComponent(name)
                  .replace(/%(2[346B]|5E|60|7C)/g, decodeURIComponent)
                  .replace(/[()]/g, encodeURIComponent);

                var stringifiedAttributes = '';

                for (var attributeName in attributes) {
                  if (Object.prototype.hasOwnProperty.call(attributes, attributeName)) {
                    if (!attributes[attributeName]) {
                      continue;
                    }

                    stringifiedAttributes += '; ' + attributeName;

                    if (attributes[attributeName] === true) {
                      continue;
                    }
                    stringifiedAttributes += '=' + attributes[attributeName].split(';')[0];
                  }
                }

                return (document.cookie =
                  name + '=' + converter.write(value, name) + stringifiedAttributes);
              }
          };

          var klaro = window.klaro;
          klaro.setup({
              languages: ['pl', 'en', 'ge', 'ru'],
              cookieExpiresAfterDays: 30,
              hideDeclineAll: true,
              services: [
                  {
                      name: 'Google tag manager',
                      required: true,
                      purposes: ['analytics'],
                      cookies: [/^_gtm(_.*)?/],
                      onAccept: "for(var k of Object.keys(opts.consents)){if(opts.consents[k]){var eventName='klaro-'+k+'-accepted';dataLayer.push({'event':eventName});}}",
                      onInit: "window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('consent','default',{'ad_storage':'denied','analytics_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','wait_for_update':500});gtag('set','ads_data_redaction',true);"
                  },
                  {
                      name: 'Session cookies',
                      purposes: ['functional'],
                      required: true,
                      onAccept: "window.cookieMenager.set('cookieAccepted', true, {expires: 30 * 24 * 60 * 60 * 1000})"
                  },
                  {
                      name: 'Facebook login',
                      purposes: ['functional'],
                      default: true,
                      onAccept: "window.cookieMenager.set('facebook-login', true, {expires: 30 * 24 * 60 * 60 * 1000})",
                      onDecline: "window.cookieMenager.set('facebook-login', false, {expires: 30 * 24 * 60 * 60 * 1000})"
                  },
                  {
                      name: 'Google login',
                      purposes: ['functional'],
                      default: true,
                      onAccept: "window.cookieMenager.set('google-login', true, {expires: 30 * 24 * 60 * 60 * 1000})",
                      onDecline: "window.cookieMenager.set('google-login', false, {expires: 30 * 24 * 60 * 60 * 1000})"
                  },
                  {
                      name: 'Google analytics',
                      cookies: [/^_ga(_.*)?/],
                      purposes: ['analytics'],
                      default: true,
                      onAccept: "gtag('consent', 'update', {'analytics_storage': 'granted'})",
                      onDecline: "gtag('consent', 'update', {'analytics_storage': 'denied'})"
                  },
                  {
                      name: 'Google ads',
                      cookies: [],
                      purposes: ['marketing'],
                      default: true,
                      onAccept: "gtag('consent', 'update', {'ad_storage': 'granted','ad_user_data': 'granted','ad_personalization': 'granted','wait_for_update': 500})",
                      onDecline: "gtag('consent', 'update', {'ad_storage': 'denied','ad_user_data': 'denied','ad_personalization': 'denied'})"
                  }
              ]
          });
          }
      };
  });
