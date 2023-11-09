// ==UserScript==
// @name         Block sites
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  Block sites
// @author       Noobgam
// @match        http*://www.youtube.com/*
// @match        http*://www.youtu.be/*
// @grant        GM_addStyle
// @run-at       document-start
// @require      http://code.jquery.com/jquery-2.2.4.js
// ==/UserScript==

(function() {
    'use strict';
    let dt = new Date();
    if (dt.getHours() > 0 && dt.getHours() < 12) {
        window.stop();
        return;
    }
})();
