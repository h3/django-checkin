/* jQuery.checkin.js
 * (c) 2011 Motion Média
 * author: Maxime Haineault
 *
 *
 * User-Agent:*
 * X-Requested-With:XMLHttpRequest
 *
 * */


// Enhanced browser/device detection
$.browser.userAgent = navigator.userAgent || navigator.vendor || window.opera
$.browser.mobile = (function(a){
    return /android.+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)
           ||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))
            && true || false
})($.browser.userAgent)

$.device = { 
    desktop: !$.browser.mobile, 
    gps: false,
    iphone: false, ipad: false, android: false, blackberry: false
}

if ($.browser.mobile) {
    $.extend($.device, {
        iphone:     /iphone/i.test(navigator.userAgent),
        ipad:       /ipad/i.test(navigator.userAgent),
        android:    /android/i.test(navigator.userAgent),
        blackberry: /blackberry/i.test(navigator.userAgent)
    });
}

$.checkin = function() {
    $self = this;

    $self.last_checkin  = false;
    $self._watchId      = false;
    $self._interval     = false;

    $self.buffer  = [];
    $self.options = {
        debug: false,
        api_url: false,
        campaign: [],
        // Anything less accurate than 1000 wont be sent to buffer
        minAccuracy: 1000,
        // Requires 3 readings before submiting the most accurate
        bufferLength: 3, 
        // Ignore readings at shorter interval than 3s
        // (flood protection & not statistically significant)
        minInterval: 3000,
        // If 10s elapse between to readings, send the
        // result anyway (less accurate positioning)
        maxInterval: 10000
    };

    $self.timestamp = function(i){
        return i || new Date().getTime();
    }

    $self.getMostAccurateReading = function() {
        if ($self.buffer.length > 0) {
            $self.buffer.sort(function(a, b){ 
                return a.coords.accuracy < b.coords.accuracy
            });
            return $self.buffer.shift()
        }
        return false;
    };

    $self.options.onerror = function(noservice) {
        if (noservice) {
            alert("Geolocation service failed.");
        } 
        else {
            alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
        }
    };

    $self.log = function() {
        if ($self.options.debug) {
            console.log.apply(console, Array.prototype.slice.call(arguments))
        }
    };

    $self.watch = function(callback, onerror, options) {
        $self._watchId = navigator.geolocation.watchPosition(
                            callback, onerror, options);
    };

    $self.url = function(path) {
        return [$self.options.api_url,path].join('');
    };

    $self.send_checkin = function(pos, callback) {
        var data = $self.getMostAccurateReading();
        data.cid = $self.options.campaign[0];
        data.useragent = navigator && navigator.userAgent || "";
        $.post($self.url('checkin'), data, function(data){
            $self.buffer = [];
            callback(data);
        });
    }

    return {
        init: function(options) {
            $self.options = $.extend($self.options, options);
            return this;
        },

        submit: function(pos, callback) {
            var checkinobj = $.extend({}, pos);
            // hack to work around strange serialization problem with firefox ..
            checkinobj = jQuery.extend(checkinobj, pos.coords);

            var ci = function() {
                $self.send_checkin(checkinobj, callback)
                    /*
                try {
                    $self.send_checkin(checkinobj, callback)
                } catch(e) {
                    $self.log("Error: Checkin failed");
                }
                */
            };

            if ($self.last_checkin && ($self.timestamp() - $self.last_checkin) < $self.options.minInterval) {
                $self.log("Ignoring checkin because the time interval since the last checkin wasn't long enough (%s < %s).", 
                    ($self.timestamp() - $self.last_checkin), $self.options.minInterval)
                return false;
            }

            if (checkinobj.coords.accuracy <= $self.options.minAccuracy) {
                $self.buffer.push(checkinobj);
                clearInterval($self._interval);
                $self.last_checkin = $self.timestamp();
                if ($self.buffer.length >= $self.options.bufferLength) {
                    $self.log("Collected enough positional data, now sending most accurate checkin.")
                    ci.call();
                    return true;
                }
                else {
                    $self.log("Checkin at lat: %s, lng: %s buffered but not sent. Waiting for %s more checkin.", 
                              checkinobj.coords.latitude, checkinobj.coords.longitude, $self.options.bufferLength - $self.buffer.length)
                     
                    $self._interval = setTimeout(function(){
                        $self.log("Timeout expired, waited %s seconds for a new checkin. Sending data (%s sample in buffer)",
                                  $self.options.maxInterval/1000, $self.buffer.length)
                        ci.call();
                    }, $self.options.maxInterval);
                }
            }
            else {
                $self.log("Ignoring checkin from lat: %s, lng: %s because the positioning is not accurate enough (%sm > %sm)",
                      checkinobj.coords.latitude, checkinobj.coords.longitude, checkinobj.coords.accuracy, $self.options.minAccuracy)
            }
            return false;
        },

        watch: function(callback, onerror, options) {
            // TODO: first call the getPosition with maximumAge set to Infinity with a timeout of 0
            // to get the last cached position, inject it in the buffer to be more error resilient
            // (ie: if the client has fired the site within the store.
            // http://dev.w3.org/geo/api/spec-source.html
            // "Forcing the user agent to return a fresh cached position."
            // "Forcing the user agent to return any available cached position."
            //
            var opts  = $.extend({ maximumAge: 0, enableHighAccuracy: true }, options);
            var onerr = onerror || $self.options.onerror;

            if (navigator.geolocation) {
                $.device.gps = true;
                if ($self._watchId) {
                    $self.clearWatch($self._watchId);
                }
                $self.watch(callback, onerr, opts);
            }

            else {
                onerr.call()
            }
        }
    };
}();
