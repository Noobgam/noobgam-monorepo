// ==UserScript==
// @name         Block sites
// @namespace    http://tampermonkey.net/
// @version      0.4
// @description  Block sites
// @author       Noobgam
// @match        http*://www.youtube.com/*
// @match        http*://www.youtu.be/*
// @grant        GM_addStyle
// @require      https://code.jquery.com/jquery-3.7.1.min.js
// @run-at       document-start
// ==/UserScript==

function stopYoutubeWindow() {
    let dt = new Date();
    if (dt.getHours() > 0 && dt.getHours() < 12) {
        window.stop();
    }
}

function removeElementByQuery(query) {
    // requires jquery
    const element = $(query);
    if (element) {
        element.remove()
    }
}

function deleteShorts() {
    removeElementByQuery(`[title='Shorts']`);
    removeElementByQuery(`[tab-title='Shorts']`);
    removeElementByQuery(`#shorts-container`);
}

function handleYoutube() {
    deleteShorts();
    stopYoutubeWindow();
}

function youtubeInject() {
    setInterval(handleYoutube, 200)
}

(function() {
    'use strict';
    handleYoutube();
    youtubeInject();
})();
