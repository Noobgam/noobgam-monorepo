// ==UserScript==
// @name         Block sites
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  Block sites
// @author       Noobgam
// @match        http*://www.youtube.com/*
// @match        http*://www.youtu.be/*
// @grant        GM_addStyle
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';
    let dt = new Date();
    if (dt.getHours() > 0 && dt.getHours() < 12) {
        window.stop();
        return;
    }
})();
