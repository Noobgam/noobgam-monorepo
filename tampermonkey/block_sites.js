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
    let elements = $(query).get();
    if (elements.length > 0) {
        for (let element of elements) {
            element.remove();
        }
    }
}

function deleteShorts() {
    removeElementByQuery(`[title='Shorts']`);
    removeElementByQuery(`[tab-title='Shorts']`);
    // youtube does not care about W3C
    removeElementByQuery(`[id='shorts-container']`);
    removeElementByQuery(`[id='reply-button-end']`);
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
